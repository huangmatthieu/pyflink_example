from pyflink.common import Types
from pyflink.datastream import DataStream, StreamExecutionEnvironment
from pyflink_example.fraud_detection.utils import JsonParser
from pyflink_example.fraud_detection.source import KafkaIn
from pyflink_example.fraud_detection.sink import KafkaOut
from pyflink_example.fraud_detection.service import FraudDetector
from pyflink_example.fraud_detection.model import Transaction
from pyflink_example.fraud_detection.config import App
from typing import Iterable


def valid_json(json_str: str) -> Iterable[Transaction]:
    try:
        return [JsonParser.deserialize(json_str, Transaction)]
    except Exception as e:
        print(f"Failed to parse JSON: {json_str!r}")
        print(f"Exception: {type(e).__name__}: {e}")
        return []


def detect_fraud(
        raw_transactions: DataStream,
        amount_threshold: float,
        time_window_seconds: int,
) -> DataStream:
    transactions = raw_transactions.flat_map(valid_json)

    alerts = transactions \
        .key_by(lambda transaction: transaction.user_id) \
        .process(
            FraudDetector(
                amount_threshold=amount_threshold,
                time_window_seconds=time_window_seconds,
            ),
            output_type=Types.PICKLED_BYTE_ARRAY(),
        )

    return alerts.map(
        JsonParser.serialize,
        output_type=Types.STRING(),
    )


class FraudDetectionJob:

    def __init__(self, conf: App):
        self.conf = conf

    def build(self, env: StreamExecutionEnvironment) -> None:
        source = KafkaIn(
            bootstrap_servers=(
                self.conf.app.kafka.bootstrap_servers
            ),
            topic=self.conf.app.kafka.consumer.topic,
            group_id=self.conf.app.kafka.consumer.group_id,
        )

        raw_transactions = source.create(env)
        alert_json = detect_fraud(
            raw_transactions,
            amount_threshold=self.conf.app.flink.amount_threshold,
            time_window_seconds=self.conf.app.flink.time_window_seconds,
        )

        sink = KafkaOut(
            bootstrap_servers=self.conf.app.kafka.bootstrap_servers,
            topic=self.conf.app.kafka.producer.topic
        )

        alert_json.sink_to(sink.create())

        env.execute("FraudDetectionJob")
