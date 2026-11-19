import unittest
from app import app


class IncidentComparisonTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.incident_a = {
            "a_incident_type": "malware",
            "a_system_importance": "medium",
            "a_affected_users": "multiple",
            "a_sensitive_data": "no",
        }
        self.incident_b = {
            "b_incident_type": "unauthorized_access",
            "b_system_importance": "high",
            "b_affected_users": "multiple",
            "b_sensitive_data": "yes",
        }

    def test_comparison_page_loads(self):
        response = self.client.get("/compare")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Compare Two Incidents", response.data)
        self.assertIn(b"Incident A", response.data)
        self.assertIn(b"Incident B", response.data)

    def test_homepage_links_to_comparison(self):
        response = self.client.get("/")
        self.assertIn(b'href="/compare"', response.data)

    def test_incident_b_has_higher_score(self):
        data = {**self.incident_a, **self.incident_b}
        response = self.client.post("/compare", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incident B has the higher assessment score.", response.data)
        self.assertIn(b"5 / 12", response.data)
        self.assertIn(b"12 / 12", response.data)

    def test_incident_a_has_higher_score(self):
        data = {
            **{f"a_{key[2:]}": value for key, value in self.incident_b.items()},
            **{f"b_{key[2:]}": value for key, value in self.incident_a.items()},
        }
        response = self.client.post("/compare", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incident A has the higher assessment score.", response.data)

    def test_equal_scores(self):
        data = {
            **self.incident_a,
            **{f"b_{key[2:]}": value for key, value in self.incident_a.items()},
        }
        response = self.client.post("/compare", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Both incidents have the same assessment score.", response.data)

    def test_missing_field_is_rejected(self):
        data = {**self.incident_a, **self.incident_b}
        data.pop("b_sensitive_data")
        response = self.client.post("/compare", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Incident B:", response.data)
        self.assertIn(b"Sensitive Information is required", response.data)
        self.assertNotIn(b"Comparison Results", response.data)

    def test_invalid_value_is_rejected(self):
        data = {**self.incident_a, **self.incident_b}
        data["a_system_importance"] = "critical_invalid"
        response = self.client.post("/compare", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid selection for System Importance", response.data)


if __name__ == "__main__":
    unittest.main()
