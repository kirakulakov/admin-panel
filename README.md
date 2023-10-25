# Admin Panel

```mermaid
sequenceDiagram
    actor Client
    participant Proxy-server
    participant FastAPI-server
    participant Psql-server

    autonumber

    Client->>Proxy-server: Request
    Proxy-server->>FastAPI-server: Проксирование запроса к FastAPI-серверу
    FastAPI-server->>Psql-server: Запрос данных из базы
    activate Psql-server
    Psql-server-->>FastAPI-server: Возврат результата
    deactivate Psql-server
    FastAPI-server-->>Proxy-server: Возврат результата
    Proxy-server-->>Client: Response


```

# Run in Docker
```
git clone git@github.com:kirakulakov/admin-panel.git \
&& cd admin-panel \
&& cp .env_example .env \
&& docker build -t admin_panel -f ./docker/Dockerfile . \
&& cd docker \
&& docker compose up --build -d \
&& cd ..
```
### And go `127.0.0.1/docs` to see the docs!

<br>


# Local

### Run server
[Require `Python 3.10+` and `PSQL-client 13+` on your local machine]

1. Create virtual env
```shell
python3.10 -m venv venv
```
2. Activate virtual env and install deps from requirements.txt
```shell
. ./venv/bin/activate && pip install -r requirements.txt
```
3. Create `.env` file or clone it from .env_example
```shell
cp .env_example .env
```
4. Run server
```shell
python -m src
```

# swagger-docs

![openapi-docs](./doc/images/swagger_apis.png)

![openapi-docs](./doc/images/swagger_password_hash.png)

![openapi-docs](./doc/images/swagger_auth.png)
