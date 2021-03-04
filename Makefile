db-name=postgres


recreate-db:
	docker-compose stop backend
	docker-compose exec db bash -c "su postgres -c 'dropdb $(db-name); createdb $(db-name);'"
	docker-compose up -d backend
	make migrations

migrations:
	docker-compose exec backend bash -c "./manage.py makemigrations && \
	./manage.py migrate"

build-dev:
	docker-compose build

up-dev:
	docker-compose run --rm backend python manage.py migrate
	docker-compose up

backend-bash:
	docker-compose exec backend bash

shell:
	docker-compose exec backend bash -c "./manage.py shell_plus --ipython"

format:
	docker-compose exec backend bash -c "black ."
