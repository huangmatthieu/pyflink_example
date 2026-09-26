from unittest import TestCase, main
from pyflink_example.fraud_detection.model import Alert, Transaction
from pyflink_example.fraud_detection.service import FraudDetector


class InMemoryValueState:
    def __init__(self):
        self._value = None

    def value(self):
        return self._value

    def update(self, value):
        self._value = value


class TestRuntimeContext:
    def __init__(self):
        self.state = InMemoryValueState()

    def get_state(self, descriptor):
        return self.state


class FraudDetectorTests(TestCase):
    def setUp(self):
        self.detector = FraudDetector(
            amount_threshold=1000.0,
            time_window_seconds=60,
        )
        self.detector.open(TestRuntimeContext())

    def process(self, amount, timestamp, user_id="user-1"):
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            timestamp=timestamp,
        )
        return list(self.detector.process_element(transaction, None))

    def test_first_transaction_does_not_create_alert(self):
        self.assertEqual(self.process(1500.0, 1000), [])

    def test_two_high_value_transactions_at_window_boundary_create_alert(self):
        self.assertEqual(self.process(1000.0, 1000), [])

        alerts = self.process(1200.0, 61000)

        self.assertEqual(
            alerts,
            [
                Alert(
                    user_id="user-1",
                    amount=1200.0,
                    timestamp=61000,
                    reason="Two high-value transactions detected within 60 seconds",
                )
            ],
        )

    def test_transactions_outside_window_do_not_create_alert(self):
        self.process(1500.0, 1000)

        self.assertEqual(self.process(1600.0, 61001), [])

    def test_low_value_transaction_replaces_previous_transaction(self):
        self.process(1500.0, 1000)

        self.assertEqual(self.process(500.0, 2000), [])
        self.assertEqual(self.process(1600.0, 3000), [])

        self.assertEqual(len(self.process(1700.0, 4000)), 1)

    def test_out_of_order_transaction_does_not_create_alert(self):
        self.process(1500.0, 2000)

        self.assertEqual(self.process(1600.0, 1000), [])


if __name__ == "__main__":
    main()
