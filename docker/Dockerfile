FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_DIR /usr/src/app
RUN mkdir $APP_DIR
RUN chmod +x $APP_DIR

WORKDIR $APP_DIR

COPY ./requirements.txt ./requirements.txt
COPY ./.env ./.env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD python -m src