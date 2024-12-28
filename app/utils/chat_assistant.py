from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() # 讀取 .env檔案

client = OpenAI(
  api_key= os.getenv('API_KEY')
)

# Retrieve assistant 
assistant = client.beta.assistants.retrieve(assistant_id=os.getenv('ASSISTANT_ID'))

# Create a Thread
thread = client.beta.threads.create()
token_usage = 0
TOKEN_LIMIT = 3000

def current_total_token():
    global token_usage
    # Monitor token usage
    for run in client.beta.threads.runs.list(thread_id = thread.id).data:
        token_usage += run.usage.total_tokens

    return token_usage

def summarize_conversation():

    # Add a user message requesting a summary
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Summarize the conversation so far"
    )

    # Create a run to process the summarization request
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Provide a 40 words summary of the previous talk."
    )

    # get the summary from the assistant
    responses = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    summary = responses.data[0].content[0].text.value

    return summary

def recreate_thread(summary):

    global thread, token_usage

    # create new thread
    thread = client.beta.threads.create()

    # Add the summary as the initial message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Continue the chat based on the following summary:"+summary
    )

    token_usage = 0

def chat(new_content):

    global token_usage

    # Add a message object to the thread
    new_message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role='user',
        content=new_content
    )

    # Create a Run
    new_run = client.beta.threads.runs.create_and_poll(
        thread_id = thread.id,
        assistant_id=assistant.id,
        instructions='keep the conversation going with short reply.'
    )

    # Check the history conversation
    responses = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    last_message = responses.data[0].content[0].text.value
    # print(last_message)

    token_usage += new_run.usage.total_tokens
    print(f'current token usage:{token_usage}')

    # Check current token usage
    if token_usage > TOKEN_LIMIT:
        print('The conversation is too long, summarizing and recreating are executing')
        summary = summarize_conversation()
        recreate_thread(summary=summary)

    return last_message

def suggest(message):

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
    
        messages=[
            {"role": "system", "content": "You are a native speaker making user's sentences more fluent and natural, and tell the reason why. Spelling error is uneccessary to be mentioned in the reason."},
            {"role": "user", "content": message}
        ],
    )

    return completion.choices[0].message.content