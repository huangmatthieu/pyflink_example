from pyflink.datastream import StreamExecutionEnvironment
from pyflink_example.services.user_service import UserService
from pyflink.common import Configuration
import sys


def build_job(repo) -> None:
    config = Configuration()

    env = StreamExecutionEnvironment.get_execution_environment(config)
    env.set_python_executable(sys.executable)

    service = UserService(repo)

    (
        env.from_collection([
            {"id": "1", "name": "Alice", "email": "a@a.com"},
            {"id": "2", "name": "Bob", "email": "bexample.com"},
            {"id": "3", "name": "Charlie", "email": "c@c.com"}
        ])
        .flat_map(service.process)
        .print()
    )

    env.execute("user-job")
