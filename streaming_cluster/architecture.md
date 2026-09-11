# Flink Architecture with Docker Compose

The architecture is composed of **a Flink standalone cluster** and **a kafka cluster** using Docker Compose.

The architecture separates the Flink cluster infrastructure from the edge node where the application submits the job.

## Architecture
````commandline
                         Docker Host
                              |
                      streaming-network
                              |
        +---------------------+---------------------+
        |                     |                     |
        ▼                     ▼                     ▼
   +---------+           +---------+           +---------+
   | Kafka 1 |           | Kafka 2 |           | Kafka 3 |
   | :9092   |           | :9092   |           | :9092   |
   +---------+           +---------+           +---------+
        |                     |                     |
        +---------------------+---------------------+
                              ▲
                              |
                              |
                              |
                    +-------------------+
                    |       EDGE        |
                    |                   |
                    | Kafka CLI         |
                    | Flink CLI         |
                    | Java              |
                    +---------+---------+
                              |
                              |
                              ▼
                    +-------------------+
                    | Flink JobManager  |
                    |      :8081        |
                    +---------+---------+
                              |
                    +---------+---------+
                    |                   |
                    ▼                   ▼
              +------------+      +------------+
              | TaskManager|      | TaskManager|
              |     1      |      |     2      |
              +------------+      +------------+
````

## Components

- **JobManager**
  - Coordinates the Flink cluster.
  - Exposes the Flink REST API on port 8081.
  - Exposes the RPC endpoint on port 6123.
  
- **TaskManager**
  - Executes the actual Flink tasks.
  - Runs the Python workers required by the PyFlink application.
  - Uses the Python environment included in the custom Docker image.

- **Job**
  - Contains the Python application and its dependencies.
  - Runs the Flink CLI. 
  - Submits the application to jobmanager:8081. 
  - The job container is only a client; it does not run a Flink cluster itself. 

All three containers are connected to the same Docker Compose network.

Therefore, the job container can reach the JobManager using:
```text
flink-jobmanager:8081
````
instead of **localhost:8081** or **0.0.0.0:8081**

## Running the Project
### 1. Start the Flink Cluster

Start only the Flink infrastructure:
```text
docker compose up -d
````
This starts **JobManager** and **TaskManager**

Check that both containers are running:
```text
docker compose ps
````

### 2. Check the Flink Web UI

Open :
```text
http://localhost:8081
````
The Flink dashboard should be displayed.

You should see the JobManager and at least one connected TaskManager.

### 3. Build the Application Image
