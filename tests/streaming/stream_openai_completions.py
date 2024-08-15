

from openai import OpenAI

openai_api_key = 'sk-bloom-app-CAjHDM4W0FXLZlP5yVvgT3BlbkFJGeSaluzHcPr20animZV0'

client = OpenAI(api_key=openai_api_key)


# send a ChatCompletion request to count to 100
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'user', 'content': "Count to 100."},
    ],
    temperature=0,
    stream=True  # this time, we set stream=True
)


for chunk in response:
    choices = chunk.choices
    choice = choices[0]
    delta = choice.delta
    content = delta.content
    if content is not None:
        print(content, end='')
    else:
        continue
