import unittest

from app import app


class SampleIncidentTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_sample_scenarios_appear_on_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Suspicious Email", response.data)
        self.assertIn(b"Malware on Workstations", response.data)
        self.assertIn(b"Unauthorized Access", response.data)

    def test_phishing_sample_prefills_form(self):
        response = self.client.get("/?sample=suspicious-email")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="phishing"', response.data)
        self.assertIn(b'value="low"', response.data)
        self.assertIn(b'value="one"', response.data)
        self.assertIn(b'value="no"', response.data)
        self.assertIn(b"selected", response.data)

    def test_malware_sample_prefills_form(self):
        response = self.client.get("/?sample=workstation-malware")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="malware"', response.data)
        self.assertIn(b'value="medium"', response.data)
        self.assertIn(b'value="multiple"', response.data)

    def test_unauthorized_access_sample_prefills_form(self):
        response = self.client.get("/?sample=unauthorized-access")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="unauthorized_access"', response.data)
        self.assertIn(b'value="high"', response.data)
        self.assertIn(b'value="yes"', response.data)

    def test_unknown_sample_does_not_crash(self):
        response = self.client.get("/?sample=does-not-exist")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incident Details", response.data)


if __name__ == "__main__":
    unittest.main()
