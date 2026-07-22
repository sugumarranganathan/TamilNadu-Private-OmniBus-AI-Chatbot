
"""
search_engine.py
Version 6.0
"""

import pickle
from datetime import datetime

import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import BUS_CSV,DOCUMENTS_FILE,FAISS_INDEX,EMBEDDING_MODEL,TOP_K,MIN_CONFIDENCE,validate_project
from utils.intent import analyze_query

TIME_RANGES={
    "morning":(5,12),
    "afternoon":(12,17),
    "evening":(17,21),
    "night":None,
}

class BusSearchEngine:

    def __init__(self):
        validate_project()
        self.df=pd.read_csv(BUS_CSV)
        with open(DOCUMENTS_FILE,"rb") as f:
            self.documents=pickle.load(f)
        self.index=faiss.read_index(str(FAISS_INDEX))
        self.model=SentenceTransformer(EMBEDDING_MODEL)

    def semantic_search(self,query,top_k=TOP_K):
        emb=self.model.encode([query],convert_to_numpy=True)
        distances,ids=self.index.search(emb,top_k)
        results=[]
        for dist,idx in zip(distances[0],ids[0]):
            if idx<0 or idx>=len(self.df):
                continue
            row=self.df.iloc[int(idx)].to_dict()
            row["_score"]=float(dist)
            results.append(row)
        return results

    def _hour(self,value):
        try:
            return datetime.strptime(str(value).strip(),"%H:%M").hour
        except:
            return None

    def _time_match(self,slot,time_text):
        if not slot:
            return True
        h=self._hour(time_text)
        if h is None:
            return True
        if slot=="night":
            return h>=21 or h<5
        start,end=TIME_RANGES[slot]
        return start<=h<end

    def filter_results(self,results,intent):
        out=[]
        for bus in results:
            if intent["from_city"] and str(bus["From_City"]).lower()!=intent["from_city"].lower():
                continue
            if intent["to_city"] and str(bus["To_City"]).lower()!=intent["to_city"].lower():
                continue
            if intent["bus_type"] and intent["bus_type"].lower() not in str(bus["Bus_Type"]).lower():
                continue
            if intent["operator"] and intent["operator"].lower() not in str(bus["Operator"]).lower():
                continue
            fare=float(bus["Fare"])
            if intent.get("min_price") is not None and fare<intent["min_price"]:
                continue
            if intent.get("max_price") is not None and fare>intent["max_price"]:
                continue
            if not self._time_match(intent.get("time"),bus["Departure_Time"]):
                continue
            amenities=[a.strip().lower() for a in str(bus["Amenities"]).split(",")]
            ok=True
            for req in intent["amenities"]:
                if req.lower() not in amenities:
                    ok=False
                    break
            if not ok:
                continue
            out.append(bus)

        sort=intent.get("sort")
        if sort=="cheapest":
            out.sort(key=lambda x:float(x["Fare"]))
        elif sort=="rating":
            out.sort(key=lambda x:float(x["Rating"]),reverse=True)
        elif sort=="departure":
            out.sort(key=lambda x:self._hour(x["Departure_Time"]) or 99)
        elif sort=="duration":
            out.sort(key=lambda x:str(x["Duration"]))
        return out

    def search(self,query):
        intent=analyze_query(query)
        results=self.semantic_search(query,TOP_K)
        return self.filter_results(results,intent)

if __name__=="__main__":
    engine=BusSearchEngine()
    while True:
        q=input("Query: ")
        if q=="exit":
            break
        r=engine.search(q)
        print(f"{len(r)} result(s)")
        for b in r[:5]:
            print(f"{b['Operator']} | {b['From_City']}->{b['To_City']} | ₹{b['Fare']} | {b['Departure_Time']}")
