FROM flink:1.20-scala_2.12-java17

USER root

# Install utilities
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       wget \
       netcat-openbsd \
       procps \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Kafka CLI
# ------------------------------------------------------------

ARG KAFKA_VERSION=3.9.0
ARG SCALA_VERSION=2.13

RUN wget -q https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && tar -xzf kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -C /opt \
    && mv /opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION} /opt/kafka \
    && rm kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz

ENV PATH="/opt/kafka/bin:/opt/flink/bin:${PATH}"

WORKDIR /opt/jobs

COPY src ./src
COPY config ./config
RUN zip src.zip src/pyflink_example

# flink run -m flink-jobmanager:8081 --pyFiles src.zip --py-requirements requirements.txt src/pyflink_example/fraud_detection/main.py --config-path ./config/

CMD ["sleep", "infinity"]