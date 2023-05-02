# Tasker

Tasker is a simple task management system built using Python and Redis. It allows you to create tasks, manage them, and assign workers to complete them. This README will provide a brief overview of the project, how to use it, and how to deploy it.



## Architecture 

### Services and Structure
The project is structured in a way that separates the different components of the service into different folders. 

The `tasker` folder contains the `creator` and `manager` components, responsible for creating and managing tasks, respectively. 

The `workers` folder contains the different worker components, each with their own subfolder. 

- The `sum` worker generates the sum of two numbers.
- The `chat` worker generates ChatGPT query based on a question and API Key.
- The `sequence` worker calculates the sum of the sequence `1 + 2 + 3 + ... + n` without using the known formula (using `sum` worker).
- The `conversation` worker generates conversation of ChatGPT with itself (using `chat` worker) based on a topic and the number of iterations.

Each worker has its own `Dockerfile`, `requirements.txt` file, and Python file for the worker logic.


### Database
The project uses Redis as the database. Redis is an open-source, in-memory data structure store, used as a database, cache, and message broker. In this project, Redis is used to store task queues and task results.

Specifically, the project uses Redis to store the following:

- `sum_task_queue` a task queue for the summation worker to process.
- `sequence_task_queue` a task queue for the sequence worker to process.
- `chat_task_queue` a task queue for the chat worker to process.
- `tasks` a hash map to store the results of the tasks. The task results are stored with their corresponding task IDs.

Redis provides a fast and efficient way to store and retrieve data. It also supports atomic operations, making it a good fit for managing the task queues and results in this project.

## Decisions and Thoughts

### Microservices

While it is more intuitive to understand the need for microservices for `workers` services, as they use different external resources and have significant runtime difference, the separation of task handler into `manager` and `creator` may not seem as necessary at first glance.

However, I chose to separate these operations mainly because it is easier to ensure that the `creator`, which takes O(1), does not lose new tasks, compared to the `manager` that accesses the databases and takes O(1) on average. This is particularly important during loads or when there are a lot of tasks in the database.

### New supported tasks

I chose to add two tasks but they are very similar in concept and implementation. (ChatGPT key are blocked very quickly)
The main goal was to demonstrate how microservices can be reused within the system, without using information-heavy protocols, enabling easier scalability, resulting in efficient running times, and easy maintenance over time.



## Deployment

The `docker-compose.yml` file is provided to allow for easy deployment of the service. 
Use Docker Compose to easily deploy the service by running `docker-compose up -d` in the root directory of the project.
Use the API to create and manage tasks, it can be accessed at:
- `http://localhost:5000/` for task creation
- `http://localhost:5001/` for task manging results (get, delete)



## API Description

### Endpoints

#### POST /sum
This endpoint accepts a JSON payload with two numbers to be summed. It generates a task and returns a task ID that can be used to retrieve the result of the task.
- Payload example: `{"num1": 3, "num2": 5}`

#### POST /chat
This endpoint accepts a JSON payload with an API key and a question to ask the language model. It generates a task and returns a task ID that can be used to retrieve the result of the task later.
- Payload example: `{"api_key": "YOUR_API_KEY", "question": "What is the meaning of life?"}`

#### POST /sequence
This endpoint accepts a JSON payload with a number `n`. It generates `n` tasks for adding consecutive integers and returns the sum of all the numbers in a sequence.
- Payload example: `{"n": 4}`

#### POST /conversation
This endpoint accepts a JSON payload with a topic, an API key, and a number `n`. It generates `n` tasks for generating short responses and follow-up questions related to the given topic.
- Payload example: `{"topic": "artificial intelligence", "api_key": "YOUR_API_KEY", "n": 5}`

#### GET /task/{task_id}
This endpoint accepts a task ID and returns the result of the corresponding task if it has completed.

#### DELETE /task/{task_id}
This endpoint accepts a task ID and deletes the corresponding task.


### Example Queries Using Curl

#### Sum task:
```
curl -s -X POST http://localhost:5000/sum \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": {
        "num1": 5,
        "num2": 7
    }
}'
```

#### Chat task:
```
curl -s -X POST http://localhost:5000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": {
        "question": "Tell us an interesting fact on a topic of your choice, keep it short",
        "api_key": "YOUR_SECRET_API_KEY"
    }
}'
```

#### Sequence task:
```
curl -s -X POST http://localhost:5000/sequence \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": {
        "n": 5
    }
}'
```

#### Conversation task:
```
curl -s -X POST http://localhost:5000/conversation \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": {
        "topic": "AI",
        "n": 4,
        "api_key": "YOUR_SECRET_API_KEY"
    }
}'
```

#### Get task result:
```
curl -s http://localhost:5001/task/TASK_ID
```

#### Delete task result:
```
curl -s -X DELETE http://localhost:5001/task/TASK_ID
```
