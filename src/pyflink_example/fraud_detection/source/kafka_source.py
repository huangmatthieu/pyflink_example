from pyflink.common import SimpleStringSchema, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    KafkaSource,
)


class KafkaSource:

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id

    def create(self, env: StreamExecutionEnvironment):

        source = (
            KafkaSource.builder()
            .set_bootstrap_servers(self.bootstrap_servers)
            .set_topics(self.topic)
            .set_group_id(self.group_id)
            .set_starting_offsets(
                KafkaOffsetsInitializer.earliest()
            )
            .set_value_only_deserializer(
                SimpleStringSchema()
            )
            .build()
        )

        return env.from_source(
            source,
            WatermarkStrategy.no_watermarks(),
            "Kafka Transaction Source",
        )