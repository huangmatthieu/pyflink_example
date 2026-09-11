from pyflink_example.models.user import User


class KafkaUserRepository:
    def __init__(self, kafka_producer):
        self.kafka_producer = kafka_producer

    def save(self, user: User) -> None:
        message = f"{user.id},{user.name},{user.email}"
        self.kafka_producer.send("users-topic", message)
