import pytest

from util import verify_vaild


def test_is_valid_id_numeric():
    assert verify_vaild.is_valid_id("12345") is False


def test_is_valid_id_alphanumeric():
    assert verify_vaild.is_valid_id("abc123") is True


def test_valid_response_and_parse():
    sample = {
        "count": 1,
        "items": [
            {
                "handle": "tester",
                "rating": 1500,
                "tier": 5,
                "solvedCount": 42,
            }
        ],
    }

    assert verify_vaild.is_valid_response(sample) is True

    parsed = verify_vaild.parse_user_info(sample)
    assert parsed == {
        "boj_id": "tester",
        "rating": 1500,
        "tier": 5,
        "solved_count": 42,
    }
