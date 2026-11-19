import unittest
from app import app


class ClearFormTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_clear_form_button_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Clear Form", response.data)
        self.assertIn(b'href="/" class="clear-button"', response.data)

    def test_clear_removes_previous_assessment(self):
        incident = {
            "incident_type": "unauthorized_access",
            "system_importance": "high",
            "affected_users": "multiple",
            "sensitive_data": "yes",
        }

        assessment = self.client.post("/", data=incident)
        self.assertEqual(assessment.status_code, 200)
        self.assertIn(b"High Priority", assessment.data)

        cleared = self.client.get("/")
        self.assertEqual(cleared.status_code, 200)
        self.assertNotIn(b"Assessment Score:", cleared.data)
        self.assertNotIn(
            b"Incident details submitted successfully",
            cleared.data,
        )

    def test_clear_resets_sample_selections(self):
        sample = self.client.get("/?sample=unauthorized-access")
        self.assertEqual(sample.status_code, 200)
        self.assertRegex(
            sample.data.decode(),
            r'<option value="unauthorized_access"[^>]*selected',
        )

        cleared = self.client.get("/")
        self.assertEqual(cleared.status_code, 200)
        self.assertNotRegex(
            cleared.data.decode(),
            r'<option\b[^>]*\bselected\b',
        )


if __name__ == "__main__":
    unittest.main()
