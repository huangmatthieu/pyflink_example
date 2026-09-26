import json
import sys
from unittest import TestCase

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink_example.fraud_detection.job.fraud_detection_job import detect_fraud


class FraudDetectionPipelineIntegrationTests(TestCase):
    def test_local_flink_pipeline_parses_keys_detects_and_serializes_alerts(self):
        env = StreamExecutionEnvironment.get_execution_environment()
        env.set_parallelism(1)
        env.set_python_executable(sys.executable)
        raw_transactions = env.from_collection(
            [
                '{"user_id":"user-1","amount":1000.0,"timestamp":1000}',
                '{"user_id":"user-2","amount":1800.0,"timestamp":2000}',
                '{"user_id":"user-1","amount":1200.0,"timestamp":61000}',
                '{"user_id":"user-2","amount":1600.0,"timestamp":63001}',
                "not valid json",
            ],
            type_info=Types.STRING(),
        )
        alert_json = detect_fraud(
            raw_transactions,
            amount_threshold=1000.0,
            time_window_seconds=60,
        )

        with alert_json.execute_and_collect() as results:
            alerts = [json.loads(result) for result in results]

        self.assertEqual(
            alerts,
            [
                {
                    "user_id": "user-1",
                    "amount": 1200.0,
                    "timestamp": 61000,
                    "reason": "Two high-value transactions detected within 60 seconds",
                }
            ],
        )
