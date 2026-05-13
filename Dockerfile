FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir requests

WORKDIR /app

COPY scripts/http_check.py .

CMD [ "python3", "http_check.py" ]