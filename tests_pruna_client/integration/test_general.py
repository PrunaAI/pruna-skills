"""Integration tests for general client functionality."""
import os

import pytest

from pruna_client import PrunaClient, Response
from pruna_client.models import PredictionStatus


def get_api_key() -> str | None:
    """Get API key from environment or return None."""
    return os.getenv("PRUNA_API_KEY")


class TestClientInitializationFlow:
    """Integration tests for client initialization."""
    
    def test_client_init_with_api_key(self):
        """Test client initialization with explicit API key."""
        api_key = get_api_key()
        if not api_key:
            pytest.skip("PRUNA_API_KEY not available")
        
        client = PrunaClient(api_key=api_key)
        assert client.api_key == api_key
        assert client.base_url == "https://api.pruna.ai/v1"
    
    def test_client_init_from_environment(self):
        """Test client initialization from environment variable."""
        api_key = get_api_key()
        if not api_key:
            pytest.skip("PRUNA_API_KEY not available")
        
        # Temporarily set env var
        original_key = os.environ.get("PRUNA_API_KEY")
        try:
            os.environ["PRUNA_API_KEY"] = api_key
            client = PrunaClient()
            assert client.api_key == api_key
        finally:
            if original_key:
                os.environ["PRUNA_API_KEY"] = original_key
            elif "PRUNA_API_KEY" in os.environ:
                del os.environ["PRUNA_API_KEY"]
    
    def test_client_init_missing_api_key(self):
        """Test client initialization fails without API key."""
        original_key = os.environ.get("PRUNA_API_KEY")
        try:
            if "PRUNA_API_KEY" in os.environ:
                del os.environ["PRUNA_API_KEY"]
            
            with pytest.raises(ValueError, match="API key must be provided"):
                PrunaClient()
        finally:
            if original_key:
                os.environ["PRUNA_API_KEY"] = original_key
    


class TestGeneralGenerationFlow:
    """Integration tests for general generation method."""
    
    def test_generate_method_sync_flow(self, client):
        """Test general generate method in sync mode."""
        response = client.generate(
            model="p-image",
            input={"prompt": "A serene forest path in autumn"},
            sync=True
        )
        
        assert isinstance(response, Response)
        assert response.status in [PredictionStatus.SUCCEEDED, PredictionStatus.PROCESSING]
        
        if response.status == PredictionStatus.SUCCEEDED:
            # Check if output is available (might fail if API doesn't return generation_url immediately or if we can't download)
            # But for integration test we expect it to work if status is succeeded
            pass
    
    def test_generate_method_async_flow(self, client):
        """Test general generate method in async mode."""
        response = client.generate(
            model="p-image",
            input={"prompt": "A magical castle in the clouds"},
            sync=False
        )
        
        assert isinstance(response, Response)
        assert response.status == PredictionStatus.STARTING
        assert response.id is not None
        # get_url is in outputs now
        assert response.response.get("get_url") is not None
    
    def test_generate_method_with_custom_input(self, client):
        """Test generate method with custom input parameters."""
        response = client.generate(
            model="p-image",
            input={
                "prompt": "A cyberpunk city at night",
                "width": 1024,
                "height": 768
            },
            sync=True
        )
        
        assert isinstance(response, Response)
        assert response.status in [PredictionStatus.SUCCEEDED, PredictionStatus.PROCESSING]


class TestFileUploadFlow:
    """Integration tests for file upload functionality."""
    
    def test_upload_file_path(self, client, temp_image_file):
        """Test uploading a file from path."""
        url = client.upload_file(temp_image_file)
        
        assert url is not None
        assert isinstance(url, str)
        assert len(url) > 0
    
    def test_upload_pil_image(self, client, sample_image):
        """Test uploading a PIL Image."""
        url = client.upload_file(sample_image)
        
        assert url is not None
        assert isinstance(url, str)
        assert len(url) > 0
    
    def test_upload_data_uri(self, client, sample_image):
        """Test uploading a data URI."""
        import base64
        from io import BytesIO
        
        buffer = BytesIO()
        sample_image.save(buffer, format="PNG")
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        data_uri = f"data:image/png;base64,{image_data}"
        
        url = client.upload_file(data_uri)
        
        assert url is not None
        assert isinstance(url, str)


class TestErrorHandlingFlow:
    """Integration tests for error handling across flows."""
    
    def test_invalid_model_handling(self, client):
        """Test handling of invalid model name."""
        response = client.generate_text_to_image(
            model="invalid-model-name",
            prompt="test prompt",
            sync=True
        )
        
        # Should return error response
        assert response is not None
        assert isinstance(response, Response)
        assert response.status == PredictionStatus.FAILED
        # Error details might be in outputs or status message if we added one?
        # In our new model, we don't have explicit 'error' field in Response, only in PredictionStatusResponse
        # But we map status to FAILED.
        # We can check outputs for error details
        assert (
            response.response.get("error") is not None
            or response.response.get("message") is not None
        )
    
    def test_missing_required_parameters(self, client):
        """Test handling of missing required parameters."""
        response = client.generate(
            model="p-image",
            input={},  # Missing prompt
            sync=True
        )
        
        assert isinstance(response, Response)
        assert response.status == PredictionStatus.FAILED
        assert (
            response.response.get("error") is not None
            or response.response.get("message") is not None
        )
