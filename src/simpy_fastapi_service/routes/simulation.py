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
    """Run simulation normally and synchronously."""
    result_env = run_carwash_example(**parameters.dict())
    return result_env.events


@router.post("/carwashTask")
async def start_carwash_example_task(parameters: CarwashParameters = Depends()):
    """Trigger a task to run the simulation with a Celery worker."""
    task = get_carwash_simulation_task.delay(parameters)
    return {"task_id": task.id}


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)
