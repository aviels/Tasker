import os
from redis import Redis
import json
from uuid import uuid4
import time


redis_conn = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))

OK = 200


def generate_sequence_task(n):
    result = 0
    for i in range(1, n+1):
        sum_task_id = str(uuid4())
        payload = {"num1": result, "num2": i}
        redis_conn.lpush('sum_task_queue', json.dumps({'task_id': sum_task_id, 'payload': payload}))
        while True:
            task_result = redis_conn.hget('tasks', sum_task_id)
            if task_result:
                task_data = json.loads(task_result)
                status_code = task_data['status_code']
                result = float(task_data['result'])
                break
            time.sleep(0.1)

    result = str(result)
    result_str = json.dumps({'result': result, 'status_code': status_code})
    redis_conn.hset('tasks', task_id, result_str)


if __name__ == '__main__':
    while True:
        task_data_json = redis_conn.brpop('sequence_task_queue')[1]
        task_data = json.loads(task_data_json)

        task_id = task_data['task_id']
        payload = task_data['payload']
        n = int(payload["n"])

        generate_sequence_task(n)
