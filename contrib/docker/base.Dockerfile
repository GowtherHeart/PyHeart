FROM python:3.13-bookworm

ENV POETRY_VERSION=2.1.2

RUN apt-get update && \
    apt-get install -y \
		build-essential \
		gettext \
		netcat-traditional \
		util-linux \
		libmount-dev \
		libblkid-dev \
		curl \
		git \
		make \
		gcc \
		postgresql-client \
		vim \
		uuid-runtime \
		ca-certificates && \
	update-ca-certificates && \
	curl -sSL https://install.python-poetry.org | python3 - && ln -s /root/.local/bin/poetry /usr/local/bin/poetry


# GOOSE DEPEND
ENV GO_BOOTSTRAP_VERSION=1.21.9
ENV GO_VERSION=1.22.2

RUN curl -LO https://go.dev/dl/go${GO_BOOTSTRAP_VERSION}.linux-amd64.tar.gz && \
    mkdir /usr/local/go-bootstrap && \
    tar -C /usr/local/go-bootstrap --strip-components=1 -xzf go${GO_BOOTSTRAP_VERSION}.linux-amd64.tar.gz && \
    rm go${GO_BOOTSTRAP_VERSION}.linux-amd64.tar.gz

ENV GOROOT_BOOTSTRAP=/usr/local/go-bootstrap

RUN curl -LO https://go.dev/dl/go${GO_VERSION}.src.tar.gz && \
    tar -C /usr/local -xzf go${GO_VERSION}.src.tar.gz && \
    rm go${GO_VERSION}.src.tar.gz && \
	cd /usr/local/go/src && ./make.bash

ENV GOROOT=/usr/local/go
ENV GOPATH=/go
ENV PATH=$GOROOT/bin:$GOPATH/bin:$PATH
RUN rm -rf /usr/local/go-bootstrap && go install github.com/pressly/goose/v3/cmd/goose@latest
