FROM python:3.9.7-slim-bullseye

RUN adduser -D app
USER app
WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt --disable-pip-version-check

COPY . /home/app

CMD ["uvicorn", "src.app:app"]
