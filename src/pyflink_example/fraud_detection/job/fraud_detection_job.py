from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink_example.fraud_detection.utils import JsonParser
from pyflink_example.fraud_detection.source import KafkaSource
from pyflink_example.fraud_detection.sink import KafkaSink
from pyflink_example.fraud_detection.service import FraudDetector
from pyflink_example.fraud_detection.model import Transaction
from pyflink_example.fraud_detection.config import Config
from typing import Optional
from pydantic import ValidationError


def valid_json(json_str: str) -> Optional[Transaction]:
    try:
        return JsonParser.deserialize(json_str, Transaction)
    except ValidationError:
        return None


class FraudDetectionJob:

    def __init__(self, conf: Config):
        self.conf = conf

    def build(
            self,
            env: StreamExecutionEnvironment,
    ) -> None:
        source = KafkaSource(
            bootstrap_servers=(
                self.conf.kafka.bootstrap_servers
            ),
            topic=self.conf.kafka.consumer.topic,
            group_id=self.conf.kafka.consumer.group_id,
        )

        raw_transactions = source.create(env)

        transactions = raw_transactions \
            .flat_map(
                lambda msg: [valid_json(msg)]
            )

        alerts = transactions \
            .key_by(
                lambda transaction: transaction.user_id
            ) \
            .process(
                FraudDetector(
                    amount_threshold=(
                        self.conf.flink.amount_threshold
                    ),
                    time_window_seconds=(
                        self.conf.flink.time_window_seconds
                    ),
                ),
                output_type=Types.PICKLED_BYTE_ARRAY()
            )

        alert_json = alerts \
            .map(
                JsonParser.serialize,
                output_type=Types.STRING(),
            )

        sink = KafkaSink(
            bootstrap_servers=(
                self.conf.kafka.bootstrap_servers
            ),
            topic=self.conf.kafka.producer.topic,
        )

        alert_json.sink_to(sink.create())

        env.execute("FraudDetectionJob")
