from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Configuration
from pyflink_example.fraud_detection.job import FraudDetectionJob
from pyflink_example.fraud_detection.config import (Settings, App)
import sys
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config-path",
        required=True,
        help="Path to the configuration file",
    )

    args = parser.parse_args()

    config = Configuration()

    env = StreamExecutionEnvironment.get_execution_environment(config)
    env.set_python_executable(sys.executable)

    settings: Settings = Settings(args.config_path)
    conf: App = settings.parse_config()
    job = FraudDetectionJob(conf)

    job.build(env)

    env.close()
