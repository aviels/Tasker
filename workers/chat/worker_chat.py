import os
from redis import Redis
import json
import openai
import requests


redis_conn = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))

OK = 200
BAD_REQUEST = 400 


def is_valid_api_key(api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.openai.com/v1/engines", headers=headers)
    return response.status_code == OK


def process_chat_task(task_id, api_key, question):
    if not is_valid_api_key(api_key):
        result = 'Invalid API key'
        status_code = BAD_REQUEST  
    else:
        openai.api_key = api_key
        prompt = "{}".format(question)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        result = completion.choices[0].message.content
        status_code = OK

    result_str = json.dumps({'result': result, 'status_code': status_code})
    redis_conn.hset('tasks', task_id, result_str)


if __name__ == '__main__':
    while True:
        task_data_json = redis_conn.brpop('chat_task_queue')[1]
        task_data = json.loads(task_data_json)

        task_id = task_data['task_id']
        payload = task_data['payload']
        question = payload['question']
        api_key = payload['api_key']
    
        process_chat_task(task_id, api_key, question)
