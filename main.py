#!/bin/python3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import config
from openai import OpenAI
import os
api_key = os.environ['OPENAI_API']
client = OpenAI(api_key=api_key)
assistant_id = config.assistant_id

app = FastAPI(
    title="ChatGPT Powered Assistant",
    description = "An App to help the people on Website",
    version='1.0'
)

class Body(BaseModel):
    text: str


@app.get('/')
def index():
    return HTMLResponse("<h1>Welcome to ChatGPT Powered Assistant</h1>")


@app.post('/generate')
def predict(body: Body):
    prompt = body.text
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id=assistant_id,
        instructions="Help the user on the event query"
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            break;
    return text

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0",port=80)