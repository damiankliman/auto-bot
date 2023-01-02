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

db_upgrade:
	alembic upgrade head

deploy:
	@echo "Starting deployment..."
	@echo
	@echo "Upgrading database..."
	@echo
	alembic upgrade head
	@echo
	@echo "Starting discord bot..."
	@echo
	python main.py
