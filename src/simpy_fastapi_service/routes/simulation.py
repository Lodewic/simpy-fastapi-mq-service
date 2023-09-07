from typing import Any

from fastapi import APIRouter, Depends
from simulation_core.simulation_carwash import CarwashParameters, run_carwash_example

from simpy_fastapi_service.celery_tasks.simulation import get_carwash_simulation_task
from simpy_fastapi_service.config.celery_utils import get_task_info

router = APIRouter()


@router.get("/carwash")
def get_carwash_example(
    parameters: CarwashParameters = Depends(),
) -> list[dict[str, Any]]:
    result_env = run_carwash_example(**parameters.dict())
    return result_env.events


@router.post("/carwashTask")
async def start_carwash_example_task(parameters: CarwashParameters = Depends()):
    """
    Return the List of universities for the countries for e.g ["turkey","india","australia"] provided
    in input in a async way. It just returns the task id, which can later be used to get the result.
    """
    task = get_carwash_simulation_task.delay(parameters)
    return {"task_id": task.id}


#
# @router.get("/carwash/task")
# def start_carwash_example_task(parameters: CarwashParameters = Depends()) -> list[dict[str, Any]]:
#     task = carwash_example_task.delay(parameters)
#
#     return task


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)


# @celery.task
# def carwash_example_task(parameters: CarwashParameters):
#     result_env = run_carwash_example(**parameters.dict())
#     return result_env.events
