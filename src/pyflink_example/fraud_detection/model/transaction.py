from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    timestamp: int

    @staticmethod
    def from_dict(data: dict) -> "Transaction":
        return Transaction(
            transaction_id=str(data["transaction_id"]),
            user_id=str(data["user_id"]),
            amount=float(data["amount"]),
            timestamp=int(data["timestamp"]),
        )

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }