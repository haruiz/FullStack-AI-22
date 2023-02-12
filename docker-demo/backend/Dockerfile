FROM python:3.10 as build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10 as production-stage
RUN apt-get update \
    && apt-get -y install libpq-dev gcc uvicorn \
    && pip install psycopg2

WORKDIR /code
COPY --from=build-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# copy code files to container
COPY ./app /code/app
COPY ./service-account.json /opt/service-account.json
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8000