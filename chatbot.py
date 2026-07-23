results = self.engine.search(query)

context = format_bus_list(results)

answer = generate_answer(query, context)

return answer
