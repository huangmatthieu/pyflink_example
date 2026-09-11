from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class Alert(BaseModel):
    user_id: str
    amount: float
    timestamp: int
    reason: str

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "reason": self.reason,
        }