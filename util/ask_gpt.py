import openai

key="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"
openai.organization = "org-XaIRMUIT9Nc2W5prV7JxAZr3"

openai.api_key = key
models = openai.Model.list()

def ask_GPT(question: str):
    try:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])
        chat_response = chat_completion.choices[0].message.content
    except Exception as e:
        print("error in ask_GPT: ", e )
        return ask_GPT(question)
    if "As an AI language model" in chat_response or "As a language model AI" in chat_response:
        return ask_GPT(question)
    return chat_response