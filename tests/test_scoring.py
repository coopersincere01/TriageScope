import unittest
from scoring import calculate_priority


class PriorityScoringTests(unittest.TestCase):

    def test_low_priority(self):
        incident = {
            "incident_type": "phishing",
            "system_importance": "low",
            "affected_users": "one",
            "sensitive_data": "no",
        }

        result = calculate_priority(incident)

        self.assertEqual(result["priority"], "Low")
        self.assertEqual(result["score"], 0)

    def test_medium_priority(self):
        incident = {
            "incident_type": "malware",
            "system_importance": "medium",
            "affected_users": "multiple",
            "sensitive_data": "no",
        }

        result = calculate_priority(incident)

        self.assertEqual(result["priority"], "Medium")
        self.assertEqual(result["score"], 5)

    def test_high_priority(self):
        incident = {
            "incident_type": "unauthorized_access",
            "system_importance": "high",
            "affected_users": "multiple",
            "sensitive_data": "yes",
        }

        result = calculate_priority(incident)

        self.assertEqual(result["priority"], "High")
        self.assertEqual(result["score"], 12)

    def test_consistent_results(self):
        incident = {
            "incident_type": "phishing",
            "system_importance": "high",
            "affected_users": "one",
            "sensitive_data": "yes",
        }

        first = calculate_priority(incident)
        second = calculate_priority(incident)

        self.assertEqual(first, second)

    def test_invalid_input(self):
        incident = {
            "incident_type": "unknown",
            "system_importance": "low",
            "affected_users": "one",
            "sensitive_data": "no",
        }

        with self.assertRaises(ValueError):
            calculate_priority(incident)


if __name__ == "__main__":
    unittest.main()