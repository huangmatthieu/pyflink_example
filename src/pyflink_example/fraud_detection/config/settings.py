from dataclasses import dataclass
from pydantic import BaseModel
from pyhocon import ConfigFactory


@dataclass(frozen=True)
class Producer(BaseModel):
    topic: str


@dataclass(frozen=True)
class Consumer(BaseModel):
    topic: str
    group_id: str
    auto_offset_reset: str


@dataclass(frozen=True)
class Kafka(BaseModel):
    bootstrap_servers: str
    consumer: Consumer
    producer: Producer


@dataclass(frozen=True)
class Flink(BaseModel):
    amount_threshold: int
    time_window_seconds: int


@dataclass(frozen=True)
class Config(BaseModel):
    name: str
    flink: Flink
    kafka: Kafka


class Settings:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_config(self) -> Config:
        raw_config = ConfigFactory.parse_file(self.file_path)
        return Config.model_validate(raw_config)

