import unittest

from app import app
from guidance import build_explanation, build_checklist


class GuidanceTests(unittest.TestCase):

    def setUp(self):
        self.incident = {
            "incident_type": "unauthorized_access",
            "system_importance": "high",
            "affected_users": "multiple",
            "sensitive_data": "yes",
        }

    def test_high_priority_explanation(self):
        explanation = build_explanation(self.incident, "High")
        self.assertIn("high initial impact score", explanation)
        self.assertIn("sensitive information", explanation)

    def test_medium_priority_explanation(self):
        explanation = build_explanation(self.incident, "Medium")
        self.assertIn("moderate initial impact", explanation)

    def test_low_priority_explanation(self):
        explanation = build_explanation(self.incident, "Low")
        self.assertIn("relatively low initial", explanation)

    def test_unauthorized_access_checklist(self):
        checklist = build_checklist(self.incident, "High")
        self.assertTrue(any(
            "authentication logs" in step for step in checklist
        ))

    def test_sensitive_data_checklist(self):
        checklist = build_checklist(self.incident, "High")
        self.assertTrue(any(
            "exposed sensitive information" in step
            for step in checklist
        ))

    def test_guidance_displays_on_website(self):
        client = app.test_client()
        response = client.post("/", data=self.incident)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Why This Priority Was Assigned", response.data
        )
        self.assertIn(
            b"Recommended First-Response Checklist", response.data
        )
        self.assertIn(b"Escalate promptly", response.data)


if __name__ == "__main__":
    unittest.main()
