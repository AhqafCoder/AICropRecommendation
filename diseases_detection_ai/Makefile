# Makefile for Crop Disease Detection AI

.PHONY: help install install-dev test clean run-api run-gui docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests"
	@echo "  clean        Clean cache files"
	@echo "  run-api      Start the API server"
	@echo "  run-gui      Start the GUI application"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker Compose"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

run-api:
	python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

run-gui:
	python crop_disease_gui.py

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

format:
	black src/ api/ tests/ *.py

lint:
	flake8 src/ api/ tests/ *.py

train:
	python src/train.py

evaluate:
	python src/evaluate.py
