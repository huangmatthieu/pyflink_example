FROM flink:1.20.3

USER root

RUN apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    apt-get install -y --no-install-recommends zip && \
    rm -rf /var/lib/apt/lists/*

# Install uv globally
RUN curl -LsSf https://astral.sh/uv/install.sh | \
    UV_INSTALL_DIR=/usr/local/bin sh

WORKDIR /workspace

# Copy dependency files
COPY pyproject.toml ./

# Create .venv and install dependencies
RUN uv lock && uv sync

# Copy source code
COPY src ./src

# Make src available for Python imports
ENV PYTHONPATH=/workspace/src

# Use the virtual environment by default
ENV PATH="/workspace/.venv/bin:$PATH"

RUN zip src.zip src/pyflink_example

USER flink

# if run inside the container, wihout sending app to standalone cluster
#CMD ["python", "-m", "pyflink_example.main"]