from pyflink_example.repository.kafka_user_repository import KafkaUserRepository


def build_repository() -> KafkaUserRepository:
    kafka_producer = create_fake_kafka()  # or real one
    return KafkaUserRepository(kafka_producer)


def create_fake_kafka():
    class FakeKafka:
        def send(self, topic, message):
            print(f"[KAFKA:{topic}] {message}")

    return FakeKafka()
