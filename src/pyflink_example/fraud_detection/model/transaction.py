from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class Transaction(BaseModel):
    user_id: str
    amount: float
    timestamp: int

    @staticmethod
    def from_dict(data: dict) -> "Transaction":
        return Transaction(
            user_id=str(data["user_id"]),
            amount=float(data["amount"]),
            timestamp=int(data["timestamp"]),
        )

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }