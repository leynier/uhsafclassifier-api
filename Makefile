HOST = localhost
PORT = 8000

install:
	poetry install

tests: install
	poetry run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	poetry run black . --check
	poetry run isort . --profile=black
	poetry run pytest --cov=./ --cov-report=xml

export:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

run: install
	poetry run uvicorn uhsafclassifier.main:app --reload --host ${HOST} --port ${PORT}

build:
	docker build -t uhsafclassifier:latest .

deploy:
	docker run -d -p ${PORT}:80 --name uhsafclassifier-container --env-file .env uhsafclassifier:latest

rmcontainer:
	docker container rm uhsafclassifier-container --force

rmimage:
	docker image rm uhsafclassifier:latest

build_deploy: build deploy

rmall: rmcontainer rmimage

redeploy: rmall build_deploy

logs:
	docker logs uhsafclassifier-container
