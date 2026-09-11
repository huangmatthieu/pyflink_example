from typing import Optional
from pyflink.common import Types
from pyflink.datastream import RuntimeContext
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor, ValueState
from pyflink_example.fraud_detection.model import Alert
from pyflink_example.fraud_detection.model import Transaction


class FraudDetector(KeyedProcessFunction):

    def __init__(
            self,
            amount_threshold: float = 1000.0,
            time_window_seconds: int = 60,
    ):
        self.amount_threshold = amount_threshold
        self.time_window_ms = time_window_seconds * 1000

        self.previous_transaction_state: ValueState[Optional[dict]] = None

    def open(self, runtime_context: RuntimeContext):
        descriptor = ValueStateDescriptor(
            "previous_transaction",
            Types.PICKLED_BYTE_ARRAY()
        )

        self.previous_transaction_state = (
            runtime_context.get_state(descriptor)
        )

    def process_element(
            self,
            transaction: Transaction,
            ctx: KeyedProcessFunction.Context,
    ):
        previous = self.previous_transaction_state.value()

        if previous is not None:

            time_difference = transaction.timestamp - previous["timestamp"]

            both_are_large = (
                    previous["amount"] >= self.amount_threshold
                    and transaction.amount >= self.amount_threshold
            )

            within_time_window = (
                    0 <= time_difference <= self.time_window_ms
            )

            if both_are_large and within_time_window:
                yield Alert(
                    user_id=transaction.user_id,
                    amount=transaction.amount,
                    timestamp=transaction.timestamp,
                    reason=(
                        "Two high-value transactions detected "
                        f"within {self.time_window_ms // 1000} seconds"
                    )
                )

        self.previous_transaction_state.update(transaction.to_dict())


