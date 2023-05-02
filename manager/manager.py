import os
from redis import Redis
import json
from flask import Flask, Response


app = Flask(__name__)
redis_conn = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))

OK = 200
NOT_FOUND = 404


@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id):
    result = redis_conn.hget('tasks', task_id)
    if not result:
        return Response(status=NOT_FOUND)
    else:
        result_data = json.loads(result)
        return Response(response=result_data['result'], status=result_data['status_code'])


@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = redis_conn.hdel('tasks', task_id)
    if result == 1:
        return Response(status=OK)
    else:
        return Response(status=NOT_FOUND)


if __name__ == '__main__':
    app.run(host='0.0.0.0')