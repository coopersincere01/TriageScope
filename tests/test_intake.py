import unittest
from app import app


class IncidentIntakeTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.valid_incident = {
            "incident_type": "phishing",
            "system_importance": "low",
            "affected_users": "one",
            "sensitive_data": "no"
        }

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incident Details", response.data)

    def test_valid_incident_submission(self):
        response = self.client.post(
            "/", data=self.valid_incident
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Incident details submitted successfully",
            response.data
        )

    def test_missing_required_field(self):
        incident = self.valid_incident.copy()
        incident.pop("incident_type")

        response = self.client.post("/", data=incident)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Incident Type is required",
            response.data
        )

    def test_invalid_incident_type(self):
        incident = self.valid_incident.copy()
        incident["incident_type"] = "invalid_type"

        response = self.client.post("/", data=incident)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Invalid selection for Incident Type",
            response.data
        )

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["status"], "ok"
        )


if __name__ == "__main__":
    unittest.main()