FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_DIR /usr/src/app
RUN mkdir $APP_DIR
RUN chmod +x $APP_DIR

ENV wbmp_redis_stat_host 0.0.0.0
ENV wbmp_redis_stat_port 8080

EXPOSE $prefix_web_port

WORKDIR $APP_DIR

COPY ./requirements ./requirements
COPY ./.env ./.env

RUN pip install --upgrade pip
RUN pip install pip-compile-multi
RUN pip-compile-multi
RUN pip install -r requirements/base.txt

COPY ./src ./src

COPY docker/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]