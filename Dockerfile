FROM ubuntu:latest

MAINTAINER speedy

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && \
    pip install numpy scikit-learn pandas numpy datetime pyarrow boto3 nltk xlrd flask gevent gunicorn modin && \
        rm -rf /root/.cache

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY Linear_Regx /opt/program
RUN chmod +x /opt/program/serve
WORKDIR /opt/code
