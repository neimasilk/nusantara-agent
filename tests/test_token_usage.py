import unittest

from src.utils.token_usage import extract_token_usage, merge_usage


class DummyMessage:
    def __init__(self, usage_metadata=None, response_metadata=None):
        self.usage_metadata = usage_metadata
        self.response_metadata = response_metadata


class TokenUsageTests(unittest.TestCase):
    def test_extract_from_usage_metadata(self):
        msg = DummyMessage(
            usage_metadata={"input_tokens": 11, "output_tokens": 7, "total_tokens": 18},
            response_metadata={},
        )
        self.assertEqual(
            extract_token_usage(msg),
            {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18},
        )

    def test_extract_from_response_metadata(self):
        msg = DummyMessage(
            usage_metadata={},
            response_metadata={"token_usage": {"prompt_tokens": 3, "completion_tokens": 5, "total_tokens": 8}},
        )
        self.assertEqual(
            extract_token_usage(msg),
            {"prompt_tokens": 3, "completion_tokens": 5, "total_tokens": 8},
        )

    def test_extract_total_fallback_sum(self):
        msg = DummyMessage(
            usage_metadata={"input_tokens": 4, "output_tokens": 6},
            response_metadata={},
        )
        self.assertEqual(
            extract_token_usage(msg),
            {"prompt_tokens": 4, "completion_tokens": 6, "total_tokens": 10},
        )

    def test_merge_usage(self):
        acc = {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3}
        merge_usage(acc, {"prompt_tokens": 4, "completion_tokens": 5, "total_tokens": 9})
        self.assertEqual(acc, {"prompt_tokens": 5, "completion_tokens": 7, "total_tokens": 12})


if __name__ == "__main__":
    unittest.main()
