FROM flink:1.20-scala_2.12-java17

USER root

# Install utilities
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        build-essential \
        curl \
        wget \
    && apt-get install -y --no-install-recommends zip \
    && rm -rf /var/lib/apt/lists/*

# Make python available as "python"
RUN ln -sf /usr/bin/python3 /usr/bin/python

# ------------------------------------------------------------
# Kafka CLI
# ------------------------------------------------------------

ARG KAFKA_VERSION=3.9.0
ARG SCALA_VERSION=2.13

RUN wget -q https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && tar -xzf kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -C /opt \
    && mv /opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION} /opt/kafka \
    && rm kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz

# Upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade pip

# PyFlink
RUN python3 -m pip install --no-cache-dir \
    apache-flink==1.20.5

ENV PYTHON_EXEC=/usr/bin/python

ENV PATH="/opt/kafka/bin:/opt/flink/bin:${PATH}"


WORKDIR /opt/jobs

COPY ../../src /opt/jobs/src
COPY ../../config /opt/jobs/config
COPY ../../requirements.txt /opt/jobs/requirements.txt
RUN cd src && zip -r ../src.zip pyflink_example
RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN wget -P /opt/flink/lib/ \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.3.0-1.20/flink-connector-kafka-3.3.0-1.20.jar \
    && wget -P /opt/flink/lib/ \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.3.0-1.20/flink-connector-kafka-3.3.0-1.20.jar \
    && wget -P /opt/flink/lib/ \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.9.1/kafka-clients-3.9.1.jar

# flink run -m flink-jobmanager:8081 --pyFiles src.zip --pyRequirements requirements.txt --pyExecutable /usr/bin/python3 --python src/pyflink_example/fraud_detection/main.py --config-path ./config/application.conf

CMD ["sleep", "infinity"]