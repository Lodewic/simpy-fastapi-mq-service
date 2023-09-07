##### MAIN API BUILDER #####
FROM python:3.10 AS base

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip

# add required files from repo as long as package is not on jfrog.
ENV LANG=C.UTF-8

COPY src/requirements/ /app/src/requirements/
COPY src/setup.py /app/src/setup.py
COPY ./src/simpy_fastapi_service/__init__.py /app/src/simpy_fastapi_service/__init__.py
COPY README.md /app/README.md
RUN pip install ./src/
COPY ./ /app/
COPY ./run.sh /app/run.sh
RUN chmod +x ./run.sh
FROM base as dev
RUN pip install .
EXPOSE 80

ENTRYPOINT bash ./run.sh
#CMD ["uvicorn", "src.simpy_fastapi_service.main:app", "--host", "0.0.0.0", "--port", "80"]
