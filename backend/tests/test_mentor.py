"""Mentor service tests with mocked AI provider."""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_mentor_fallback_no_key():
    from app.services.mentor import generate_mentor_reply
    with patch("app.services.mentor.settings") as mock_settings:
        mock_settings.AI_API_KEY = ""
        result = await generate_mentor_reply(
            "Why is my logistic regression not converging?",
            "hint",
            {"course": "Machine Learning", "level": 2},
            [],
        )
    assert result["provider_used"] == "local_socratic_fallback"
    assert len(result["content"]) > 50


@pytest.mark.asyncio
async def test_mentor_debug_mode():
    from app.services.mentor import generate_mentor_reply
    with patch("app.services.mentor.settings") as mock_settings:
        mock_settings.AI_API_KEY = ""
        result = await generate_mentor_reply(
            "I have a bug in my code",
            "debug",
            {"course": "Python Foundations"},
            [],
        )
    assert "debug" in result["content"].lower() or "bug" in result["content"].lower() or "trace" in result["content"].lower()


@pytest.mark.asyncio
async def test_mentor_with_mocked_api():
    from app.services.mentor import generate_mentor_reply
    mock_response = {
        "choices": [{"message": {"content": "Great question! Let's think step by step..."}}],
        "usage": {"total_tokens": 100},
    }
    with patch("app.services.mentor.settings") as mock_settings, \
         patch("httpx.AsyncClient") as mock_client:
        mock_settings.AI_API_KEY = "test-key"
        mock_settings.AI_BASE_URL = "https://api.openai.com/v1"
        mock_settings.AI_MODEL = "gpt-4o-mini"
        mock_settings.AI_MAX_TOKENS = 500
        mock_settings.AI_TEMPERATURE = 0.4
        mock_instance = mock_client.return_value.__aenter__.return_value
        response = type("MockResponse", (), {
            "json": lambda self: mock_response,
            "raise_for_status": lambda self: None,
        })()
        mock_instance.post = AsyncMock(return_value=response)

        result = await generate_mentor_reply("What is a neural network?", "beginner", {}, [])
    assert result["content"] == "Great question! Let's think step by step..."
