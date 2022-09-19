FROM python:3.10

ENV PYTHONPATH /code/app

WORKDIR /code

EXPOSE 8000

COPY ./requirements.txt /code/requirements.txt

COPY ./app/alembic.ini /code/alembic.ini

COPY ./app/alembic /code/alembic

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN rm -r /code/app/alembic && rm -r /code/app/alembic.ini

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
