class RAGPrompt:
    simpleQAPrompt = '''### Context:
{context}

### previous conversation summary
{prev_conversation}

### Instruction:
Please say your response in Korean.
Keep your answer as short as possible

### Spec:
{question}

### Response:
'''