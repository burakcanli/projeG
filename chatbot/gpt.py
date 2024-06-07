import openai

openai.api_key = 'openai_api_key'

def get_response(user_input):
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0125:personal::......",
        messages=[
            {"role": "system", "content": "You are an entrepreneurship advisor who provides consultancy on starting and running a business."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=250
    )
    return response['choices'][0]['message']['content']
