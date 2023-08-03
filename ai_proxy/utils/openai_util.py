import os
import json
import requests
import openai

openai.api_base = "https://api.app4gpt.com/v1"
openai.api_key = "sk-ilvleyujXnlgzMV8K66dssh2y3BZFt5QGe+kbferrPMNAQAA"

def get_completion(messages, model="gpt-3.5-turbo", temperature=0):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content


if __name__ == '__main__':
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "can you tell me who are you and who's your father"}
    ]

    res = get_completion(messages=messages)
    print(res)

