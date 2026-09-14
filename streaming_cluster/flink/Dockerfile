FROM flink:1.20-scala_2.12-java17

USER root

# Python and build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        build-essential \
        curl \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Make python available as "python"
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade pip

# PyFlink
RUN python3 -m pip install --no-cache-dir \
    apache-flink==1.20.5

ENV PYTHON_EXEC=/usr/bin/python

RUN wget -P /opt/flink/lib/ \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.3.0-1.20/flink-connector-kafka-3.3.0-1.20.jar \
    && wget -P /opt/flink/lib/ \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.3.0-1.20/flink-connector-kafka-3.3.0-1.20.jar \
    && wget -P /opt/flink/lib/ \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.9.1/kafka-clients-3.9.1.jar

USER flink