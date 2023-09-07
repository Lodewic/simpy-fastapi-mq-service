import random

import simpy
from pydantic import BaseModel


class CarwashParameters(BaseModel):
    NUM_MACHINES: int = 2
    WASHTIME: int = 5
    T_INTER: int = 7
    SIM_TIME: int = 20


class LoggingEnvironment(simpy.Environment):
    def __init__(self, initial_time: int = 0, channel=None):
        super().__init__(initial_time=initial_time)
        self.channel = channel

    @property
    def events(self):
        if not hasattr(self, "_events"):
            self._events = []
        return self._events

    def log_event(self, event_message):
        """Append event to list of events and optionally publish to message queue channel."""
        event = dict(timestep=self.now, message=event_message)

        # Works for no meter because I don't understand publishing to queues:)
        if self.channel is not None:
            self.channel.basic_publish(
                exchange="topic_simulation", routing_key="", body=str(event)
            )
            print(f"Sent {event} to {self.channel}")

        # add message to state
        self.events.append(event)


class Carwash:
    """A carwash has a limited number of machines (``NUM_MACHINES``) to
    clean cars in parallel.

    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """

    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(self.washtime)
        self.env.log_event(
            event_message=dict(
                name=car, event="removed dirt", dirt_removed=random.randint(50, 99)
            )
        )


def car(env, name, cw):
    """The car process (each car has a ``name``) arrives at the carwash
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    env.log_event(event_message=dict(name=name, event="arrives at carwash"))
    with cw.machine.request() as request:
        yield request

        env.log_event(event_message=dict(name=name, event="enters carwash"))
        yield env.process(cw.wash(name))

        env.log_event(event_message=dict(name=name, event="leaves carwash"))


def run_carwash_example(
    NUM_MACHINES: int = 2,  # Number of machines in the carwash
    WASHTIME: int = 5,  # Minutes it takes to clean a car
    T_INTER: int = 7,  # Create a car every ~7 minutes
    SIM_TIME: int = 20,  # Simulation time in minutes
    channel=None,
):
    """
    Carwash example.

    Covers:

    - Waiting for other processes
    - Resources: Resource

    Scenario:
      A carwash has a limited number of washing machines and defines
      a washing processes that takes some (random) time.

      Car processes arrive at the carwash at a random time. If one washing
      machine is available, they start the washing process and wait for it
      to finish. If not, they wait until they can use one.

    """

    def setup(env, num_machines, washtime, t_inter):
        """Create a carwash, a number of initial cars and keep creating cars
        approx. every ``t_inter`` minutes."""
        # Create the carwash
        carwash = Carwash(env, num_machines, washtime)

        # Create 4 initial cars
        for i in range(4):
            env.process(car(env, "Car %d" % i, carwash))

        # Create more cars while the simulation is running

        while True:
            yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
            i += 1
            env.process(car(env, "Car %d" % i, carwash))

    # Create an environment and start the setup process
    env = LoggingEnvironment(channel=channel)
    env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER))

    # Execute!
    env.run(until=SIM_TIME)
    return env
