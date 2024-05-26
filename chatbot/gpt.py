import openai

openai.api_key = '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'

def get_response(user_input):
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0125:personal::9PXUZAMc",
        messages=[
            {"role": "system", "content": "You are an entrepreneurship advisor who provides consultancy on starting and running a business."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=250
    )
    return response['choices'][0]['message']['content']
