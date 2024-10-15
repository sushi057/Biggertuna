FROM python:3.12.3-slim 

WORKDIR /app

RUN apt-get update && apt-get install -y git

ENV HOST=0.0.0.0 \
   LISTEN_PORT=8000

EXPOSE 8000

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000", "--headless"]
