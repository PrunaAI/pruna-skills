"""Shared pytest fixtures for all tests."""
import os

import pytest
from PIL import Image

from pruna_client import PrunaClient


def get_api_key() -> str | None:
    """Get API key from environment or return None."""
    return os.getenv("PRUNA_API_KEY")


@pytest.fixture
def api_key():
    """Fixture providing API key or skipping tests if not available."""
    key = get_api_key()
    if not key:
        pytest.skip("PRUNA_API_KEY environment variable not set")
    return key


@pytest.fixture
def client(api_key):
    """Fixture creating a PrunaClient instance with real API key."""
    return PrunaClient(api_key=api_key)


@pytest.fixture
def sample_image():
    """Fixture creating a sample PIL Image for testing."""
    img = Image.new("RGB", (200, 200), color="red")
    return img


@pytest.fixture
def temp_image_file(sample_image, tmp_path):
    """Fixture creating a temporary image file."""
    img_path = tmp_path / "test_image.png"
    sample_image.save(img_path)
    return str(img_path)
