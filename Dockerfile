FROM python:3.11-slim

# Set UTF-8 locale to avoid encoding issues
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir .

# Install pytest for testing
RUN pip install --no-cache-dir pytest

EXPOSE 8000

CMD ["gcc-server"]
