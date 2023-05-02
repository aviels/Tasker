import os
import json
import time
from redis import Redis
from uuid import uuid4


redis_conn = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))

OK = 200


def generate_conversation_task(topic, n, api_key):
    prefix = "Answer in one short sentence and add a short follow-up question at the end: "
    question = f"What interesting about {topic}?"
    result = question + '\n'
    question = prefix + question
    for i in range(n):
        chat_task_id = str(uuid4())
        if i >= n-2:
            prefix = "Give an answer in one sentence and without a follow-up question: "

        payload = {"question": question, "api_key": api_key}
        redis_conn.lpush('chat_task_queue', json.dumps({'task_id': chat_task_id, 'payload': payload}))

        while True:
            task_result = redis_conn.hget('tasks', chat_task_id)
            if task_result:
                task_data = json.loads(task_result)
                status_code = task_data['status_code']
                answer = task_data['result']
                result = result + answer + '\n'
                question = prefix + answer
                break
            time.sleep(0.1)

    result_str = json.dumps({'result': result, 'status_code': status_code})
    redis_conn.hset('tasks', task_id, result_str)


if __name__ == '__main__':
    while True:
        task_data_json = redis_conn.brpop('conversation_task_queue')[1]
        task_data = json.loads(task_data_json)

        task_id = task_data['task_id']
        payload = task_data['payload']
        topic = payload["topic"]
        n = int(payload["n"])
        api_key = payload["api_key"]

        generate_conversation_task(topic, n, api_key)
