class EvaluationTool:
    def evaluate(self, query, history):
        # Very simplified example – in practice, will use llm logic
        if "team" in query.lower():
            return "Good response, shows teamwork."
        elif "challenge" in query.lower():
            return "Nice example of problem-solving."
        else:
            return "Response noted. Needs more detail."
