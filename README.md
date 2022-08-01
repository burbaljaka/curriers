# Curriers


## Local deployment

- First make sure you have installed docker+docker-compose and it is up and running
- execute command git clone https://github.com/burbaljaka/curriers to a desired location
- create .env file and copy data from example_env to it
- execute docker-compose build
- execute docker-compose up db
- execute docker exec -it curriers_app_1 alembic upgrade head
- enjoy server on http://127.0.0.1:8099/docs!


- to stop - press CTRL+C

## Usage

Additionally you can seed the db by hitting POST /seed_db/ url to place 3 initial zones to the db

