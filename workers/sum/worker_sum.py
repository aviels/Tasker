import os
from redis import Redis
import json


redis_conn = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))

OK = 200


def process_sum_task(num1, num2):
    result = str(num1 + num2)
    status_code = OK
    result_str = json.dumps({'result': result, 'status_code': status_code})
    redis_conn.hset('tasks', task_id, result_str)


if __name__ == '__main__':
    while True:
        task_data_json = redis_conn.brpop('sum_task_queue')[1]
        task_data = json.loads(task_data_json)

        task_id = task_data['task_id']
        payload = task_data['payload']
        num1 = payload["num1"]
        num2 = payload["num2"]

        process_sum_task(float(num1), float(num2))
