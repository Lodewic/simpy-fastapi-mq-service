# Fastapi service for SimPy as Background tasks

The goal here is to create a FastAPI service that can execute long-running SimPy simulations.

The simulations are executed using Celery workers, therefore not blocking the API itself
and set up to be scalable in the future. Initiating a simulating through the API service
will start a task on the worker, and return the `task_id` to the user. When the Task is finished,
it can be collected through the `task_id`.

Additionally, while the Task is running, we will want to publish simulation events to
a pub/sub stream. Currently, this example can publish the events during simulation but
has not been tested with a consumer.

Next steps are to think about how to publish simulation events properly and persistent.

## Setup

Create a virtual environment with conda and activate it:

```bash
conda env create -f environment.yml
conda activate simpy-fastapi-service

uvicorn src.simpy_fastapi_service.main:app
```

## Docker compose

Deploy the whole stack with docker-compose.

```bash
docker-compose up
```

Then access the components through these links:

- **API docs** Swagger UI to execute endpoints: http://127.0.0.1:8080/docs
- **RabbitMQ** to view all message queues: http://127.0.0.1:15672
  - user/password = `guest`/`guest`
- **Flower UI** to track tasks: http://127.0.0.1:5555

## Development

### Install pre-commit

Using [pre-commit](https://pre-commit.com/) we make sure to always apply checks locally before commits can be pushed to git.
Check the `.pre-commit-config.yml` for details.

Run `pre-commit install` to register the configuration with your local repository.

We always apply at least

- `ruff` to lint and autofix our code
- `mypy` to statically check type-hints
