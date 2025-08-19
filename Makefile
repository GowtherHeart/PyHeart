# enumeration of * .py files storage or folders is required.
files_to_fmt 	?= src tests main.py
files_to_check 	?= src tests main.py


## Format all
fmt: format
format: ruff_format


## Check code quality
lint: check
check: ruff_check mypy



## Run ruff linter
ruff_check:
	ruff check ${files_to_check}

## Run ruff formatter
ruff_format:
	ruff format ${files_to_fmt}

## Run ruff linter with fixes
ruff_fix:
	ruff check --fix ${files_to_check}

## Check typing
mypy:
	mypy ${files_to_check}


## BUILD IMAGES
build_app_img:
	docker build -f contrib/docker/app.Dockerfile -t pyheart-app .

build_pytest_img: build_app_img
	docker build -f contrib/docker/pytest.Dockerfile -t pyheart-pytest .


## COMPOSE
compose_up_db:
	docker compose --profile db up -d --build

compose_down_db:
	docker compose --profile db down

compose_up_app:
	docker compose --profile app up -d --build

compose_down_app:
	docker compose --profile app down

compose_up_pytest:
	docker compose --profile pytest up --build

compose_down_pytest:
	docker compose --profile pytest down
