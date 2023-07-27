.PHONY: install test typecheck lint docker all logs help, logs-follow

all: install test typecheck lint docker

help:
	@echo "------------------"
	@echo "Makefile commands:"
	@echo "------------------"
	@echo "install: Install Python dependencies."
	@echo "test: Run Python unittest."
	@echo "typecheck: Typecheck Python files with mypy."
	@echo "lint: Lint Python files with flake8."
	@echo "docker: Stop, remove, build, and start docker services."
	@echo "logs: Show docker logs."
	@echo "logs-follow: Show docker logs and follow."
	@echo "all: Run install, test, typecheck, lint and docker."

install:
	pip install -r requirements.txt

test:
	python -m unittest discover -p '*_test.py'

typecheck:
	@which mypy > /dev/null || pip install mypy
	@mypy --explicit-package-bases --install-types .

lint:
	@which flake8 > /dev/null || pip install flake8
	@flake8 .

docker:
	docker-compose stop && docker-compose rm -f && docker-compose build && docker-compose up -d

logs:
	docker-compose logs

logs-follow:
	docker-compose logs --follow

