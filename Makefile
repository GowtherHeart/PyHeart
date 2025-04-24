# enumeration of * .py files storage or folders is required.
files_to_fmt 	?= src tests main.py
files_to_check 	?= src tests main.py


## Format all
fmt: format
format: remove_imports isort black


## Check code quality
lint: check
# check: flake8 mypy
check: mypy

## Remove unused imports
remove_imports:
	autoflake -ir --remove-unused-variables \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		${files_to_fmt}


## Sort imports
isort:
	isort ${files_to_fmt}


## Format code
black:
	black ${files_to_fmt}


## Check pep8
flake8:
	flake8 ${files_to_check}


## Check typing
mypy:
	mypy ${files_to_check}


## BUILD IMAGES
build_base_img:
	docker build -f contrib/docker/base.Dockerfile -t pyheart-base .

build_app_img:
	docker build -f contrib/docker/app.Dockerfile -t pyheart-app .

build_pytest_img:
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
