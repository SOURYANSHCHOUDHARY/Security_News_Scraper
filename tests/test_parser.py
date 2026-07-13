import unittest
from parser import extract_iocs


class TestIOCParser(unittest.TestCase):

    def test_domain(self):
        text = "Visit microsoft.com"

        result = extract_iocs(text)

        self.assertIn("microsoft.com", result["Domains"])

    def test_ip(self):
        text = "Server IP is 192.168.1.10"

        result = extract_iocs(text)

        self.assertIn("192.168.1.10", result["IPs"])

    def test_url(self):
        text = "https://google.com"

        result = extract_iocs(text)

        self.assertIn(
            "https://google.com",
            result["URLs"]
        )


if __name__ == "__main__":
    unittest.main()