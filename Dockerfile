# Download a stable version of docking software
FROM ubuntu:22.04 AS docking_tools

WORKDIR /tool_downloads

RUN apt-get update \
    && apt-get install -y wget

RUN wget -O smina https://sourceforge.net/projects/smina/files/smina.static/download \
    && chmod +x smina


# Build the wheel containing needed dependencies
FROM python:3.10 AS base

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /build

COPY pyproject.toml poetry.lock README.md ./

COPY moldock/ ./moldock

RUN /root/.local/bin/poetry build


# Move software / wheels from previous layers and install
FROM python:3.10 AS service

WORKDIR /app

COPY --from=base /build/dist/*.whl .
COPY --from=docking_tools /tool_downloads/smina /bin/

RUN pip install *.whl && rm *.whl


# env runs fine / install things, but cant get app to run locally... worry about that once everything is set up and spoken with faiz
# CMD ["uvicorn", "moldock.main:app", "--host", "0.0.0.0", "--port", "8000"]