start:
	@echo "Starting discord bot..."
	@echo
	python main.py

dev:
	@echo "Starting discord bot in dev mode..."
	@echo
	python -m jurigged -v main.py

setup:
	pipenv install
