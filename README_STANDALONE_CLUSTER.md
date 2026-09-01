# PyFlink Application with Docker Compose

This project runs a **PyFlink application on a Flink standalone cluster** using Docker Compose.

The architecture separates the Flink cluster infrastructure from the application that submits the job.

## Architecture

```text
                         Docker Compose Network
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
      │ JobManager  │      │ TaskManager │      │     Job     │
      │             │      │             │      │             │
      │ REST :8081  │◄─────│ Python      │      │ PyFlink     │
      │ RPC  :6123  │      │ workers     │      │ application │
      └─────────────┘      └─────────────┘      └──────┬──────┘
             ▲                                         │
             │                                         │
             └──────────── jobmanager:8081 ────────────┘
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
jobmanager:8081
````
instead of **localhost:8081** or **0.0.0.0:8081**

## Running the Project
### 1. Start the Flink Cluster

Start only the Flink infrastructure:
```text
docker compose up -d jobmanager taskmanager
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

When the application or dependencies change, rebuild the custom image:

```text
docker compose build job
````
For a completely clean rebuild:
```text
docker compose build --no-cache job
````

### 4. Submit the PyFlink Job

Submit the application to the running Flink cluster
```text
docker compose run --rm job
````
Visualize the output: 
```text
docker compose logs -f taskmanager
````
Stop and remove the **JobManager** and **TaskManager** containers and the Compose network:
```text
docker compose down
````