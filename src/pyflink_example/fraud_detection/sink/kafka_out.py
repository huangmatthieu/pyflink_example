from pyflink.common import SimpleStringSchema
from pyflink.datastream.connectors.kafka import KafkaRecordSerializationSchema, KafkaSink
from pyflink.datastream.connectors.base import DeliveryGuarantee


class KafkaOut:

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

    def create(self):

        serialization_schema = (
            KafkaRecordSerializationSchema.builder()
            .set_topic(self.topic)
            .set_value_serialization_schema(
                SimpleStringSchema()
            )
            .build()
        )

        return (
            KafkaSink.builder()
            .set_bootstrap_servers(
                self.bootstrap_servers
            )
            .set_record_serializer(
                serialization_schema
            )
            .set_delivery_guarantee(
                DeliveryGuarantee.AT_LEAST_ONCE
            )
            .build()
        )
