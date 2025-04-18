FROM golang:1.24.2

# Install goose
RUN go install github.com/pressly/goose/v3/cmd/goose@latest

# Install psql
RUN apt-get update && \
    apt-get install -y \
		postgresql-client \
		uuid-runtime && \
    rm -rf /var/lib/apt/lists/*

CMD ["./bin/bash"]
