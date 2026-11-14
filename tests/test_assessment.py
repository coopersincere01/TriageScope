import unittest
from app import app


class AssessmentIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_high_priority_displays(self):
        incident = {
            "incident_type": "unauthorized_access",
            "system_importance": "high",
            "affected_users": "multiple",
            "sensitive_data": "yes",
        }

        response = self.client.post("/", data=incident)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"High Priority", response.data)
        self.assertIn(b"12 / 12", response.data)

    def test_medium_priority_displays(self):
        incident = {
            "incident_type": "malware",
            "system_importance": "medium",
            "affected_users": "multiple",
            "sensitive_data": "no",
        }

        response = self.client.post("/", data=incident)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Medium Priority", response.data)
        self.assertIn(b"5 / 12", response.data)

    def test_low_priority_displays(self):
        incident = {
            "incident_type": "phishing",
            "system_importance": "low",
            "affected_users": "one",
            "sensitive_data": "no",
        }

        response = self.client.post("/", data=incident)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Low Priority", response.data)
        self.assertIn(b"0 / 12", response.data)

    def test_invalid_incident_has_no_assessment(self):
        incident = {
            "incident_type": "invalid",
            "system_importance": "high",
            "affected_users": "multiple",
            "sensitive_data": "yes",
        }

        response = self.client.post("/", data=incident)

        self.assertEqual(response.status_code, 400)
        self.assertNotIn(b"High Priority", response.data)


if __name__ == "__main__":
    unittest.main()