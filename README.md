# Open Market API
### API Restful with all  "open market" of São Paulo.

### Instruções:


    Environment de variables required:

        DATABASE_URL(required) - Postgres String "postgres://user:pass@host:port/database"
        SECRET_KEY(required) - Manager by Django(Session, csrf, etc)
        WORKERS(required) - Number of workers for gunicorn
        DEBUG(optional, default 0) - 1 ou 0
        LOG_LEVEL(optional, default INFO) - log level

the logs will be direct  to stdout e /var/log/app/gunicorn.log e /var/log/app/app.log

- [Python 3.6 +](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker-Compose](https://docs.docker.com/compose/)

- Documentação:
    - [swagger](./swagger/)
    - [redcos](./redoc/)

  
- Local Environment:
        openmarket:/$ sudo docker-compose up -d
        openmarket:/$ firefox localhost:8000/api

- Dev Environment
  ```
  # generate .env file 
  openmarket:/$ python contrib/get_dot_env.py
  
  # install package
  openmarket:/$ poetry install
  
  # active virtual environment
  openmarket:/$ poetry shell 
  
  # run test
  openmarket:/$ make test
  
  # active database for developemnt
  openmarket:/$ make run-postgres 
  
  # migrate database for developemnt and load data
  openmarket:/$ make migrate
  
  # run applicatuion
  openmarket:/$ make run
  
  # for more information:
  openmarket:/$ make help
  
   
  
  ```

- Load fixtures:
        openmarket:/$ docker-compose run --entrypoint=make api dump_data

- Testes:

        openmarkets:/$ docker-compose run --entrypoint=make api test
        openmarkets:/$ docker-compose run --entrypoint=pytest api -k ".*textpattern" <- roda test específico

- Fromat, lint:

        openmarkets:/$ docker-compose run --entrypoint=make api lint
        openmarkets:/$ docker-compose run --entrypoint=make api format
        openmarkets:/$ docker-compose run --entrypoint=make api sort

- Bash:

        openmarkets:/$ docker-compose exec api bash

