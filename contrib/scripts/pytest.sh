#!/bin/bash

./contrib/scripts/db.sh

TESTING=true pytest --disable-pytest-warnings tests/
