celery -A src.simpy_fastapi_service.main.celery worker -l info --concurrency=2 &
celery -A src.simpy_fastapi_service.main.celery flower -l info &
celery -A src.simpy_fastapi_service.main.celery beat -l INFO &
uvicorn src.simpy_fastapi_service.main:app --host 0.0.0.0 --reload --workers 2 --port 8080
