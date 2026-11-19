import unittest


class PipelineFailureDemo(unittest.TestCase):

    def test_intentional_ci_failure(self):
        """Temporary test to demonstrate CI failure detection."""
        self.assertEqual(
            "approved",
            "blocked",
            "Intentional failure for CI/CD verification"
        )


if __name__ == "__main__":
    unittest.main()
