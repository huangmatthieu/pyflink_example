from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Configuration
import sys
from pyflink_example.fraud_detection.model import Transaction
from typing import Iterable
from pyflink_example.fraud_detection.service import FraudDetector
from pyflink_example.fraud_detection.utils import JsonParser
from pyflink.common import Types


def valid_json(json_str: str) -> Iterable[Transaction]:
    try:
        return [JsonParser.deserialize(json_str, Transaction)]
    except Exception as e:
        print(f"Failed to parse JSON: {json_str!r}", flush=True)
        print(f"Exception: {type(e).__name__}: {e}", flush=True)
        return []


if __name__ == "__main__":

    config = Configuration()

    env = StreamExecutionEnvironment.get_execution_environment(config)
    env.set_python_executable(sys.executable)

    alert = (  # source.create(env)
        env.from_collection([
            '{"user_id":"user1","amount":1200.0,"timestamp":1000}',
            '{"user_id":"user1","amount":1300.0,"timestamp":5000}',
            '{"user_id":"user2","amount":200.0,"timestamp":2000}',
            '{"user_id":"user2","amount":5000.0,"timestamp":9000000}',
            '{"user_id":"user1","amount":1500.0,"timestamp":200000}'
        ])
            .flat_map(valid_json)
            .key_by(
                lambda transaction: transaction.user_id
            )
            .process(
                FraudDetector(
                    amount_threshold=1000,
                    time_window_seconds=60
                )
            )
    )

    alert \
        .print()

    env.execute("toto")
    env.close()
