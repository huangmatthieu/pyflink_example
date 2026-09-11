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
    apache-flink==1.20.1

ENV PYTHON_EXEC=/usr/bin/python3

USER flink