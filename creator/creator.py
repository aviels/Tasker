import os
from redis import Redis
import json
from flask import Flask, request, Response
from uuid import uuid4


app = Flask(__name__)
redis_conn = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))


CREATED = 201
NOT_FOUND = 404


def create_task(task_queue):
    task_id = str(uuid4())
    task_data = request.get_json()
    payload = task_data['payload']
    redis_conn.lpush(task_queue, json.dumps({'task_id': task_id, 'payload': payload}))
   
    return Response(response=task_id, status=CREATED)


@app.route('/sum', methods=['POST'])
def create_sum_task():
    return create_task('sum_task_queue')


@app.route('/chat', methods=['POST'])
def create_chat_task():
    return create_task('chat_task_queue')
    

@app.route('/sequence', methods=['POST'])
def create_sequence_task():
    return create_task('sequence_task_queue')


@app.route('/conversation', methods=['POST'])
def create_conversation_task():
    return create_task('conversation_task_queue')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
