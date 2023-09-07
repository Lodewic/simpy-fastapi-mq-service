import pika
from celery import shared_task
from simulation_core import simulation_carwash


@shared_task
def get_carwash_simulation_task(parameters: simulation_carwash.CarwashParameters):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange="topic_simulation", exchange_type="topic")
    env_result = simulation_carwash.run_carwash_example(
        channel=channel, **parameters.model_dump()
    )

    connection.close()
    return env_result.events
