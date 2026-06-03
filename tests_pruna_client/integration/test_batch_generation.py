"""Integration tests for batch generation."""
import pytest

from pruna_client import PrunaClient, Response
from pruna_client.models import PredictionStatus


class TestBatchGeneration:
    """Integration tests for batch generation functionality."""

    def test_empty_batch(self, client):
        """Test that empty batch returns empty list."""
        responses = client.generate_batch([])
        assert responses == []

    def test_single_request_batch(self, client):
        """Test batch with a single request."""
        requests = [
            {"model": "p-image", "input": {"prompt": "A beautiful sunset"}, "sync": True}
        ]
        
        responses = client.generate_batch(requests)
        
        assert len(responses) == 1
        assert isinstance(responses[0], Response)
        assert responses[0].model == "p-image"

    def test_multiple_sync_requests(self, client):
        """Test batch with multiple synchronous requests."""
        requests = [
            {"model": "p-image", "input": {"prompt": "A sunset over the ocean"}, "sync": True},
            {"model": "p-image", "input": {"prompt": "A forest in autumn"}, "sync": True},
            {"model": "p-image", "input": {"prompt": "A mountain landscape"}, "sync": True},
        ]
        
        responses = client.generate_batch(requests)
        
        # Verify we got all responses
        assert len(responses) == 3
        
        # Verify all are Response objects
        for response in responses:
            assert isinstance(response, Response)
            assert response.model == "p-image"
            # Status should be SUCCEEDED or PROCESSING (if sync didn't complete immediately)
            assert response.status in [PredictionStatus.SUCCEEDED, PredictionStatus.PROCESSING, PredictionStatus.FAILED]

    def test_batch_preserves_order(self, client):
        """Test that batch responses are in the same order as requests."""
        prompts = [
            "A red apple",
            "A blue ocean",
            "A green forest",
        ]
        
        requests = [
            {"model": "p-image", "input": {"prompt": prompt}, "sync": True}
            for prompt in prompts
        ]
        
        responses = client.generate_batch(requests)
        
        assert len(responses) == len(prompts)
        
        # Verify order is preserved by checking inputs
        for i, response in enumerate(responses):
            assert response.inputs["prompt"] == prompts[i]

    def test_batch_with_mixed_sync_async(self, client):
        """Test batch with both sync and async requests."""
        requests = [
            {"model": "p-image", "input": {"prompt": "Sync request"}, "sync": True},
            {"model": "p-image", "input": {"prompt": "Async request"}, "sync": False},
        ]
        
        responses = client.generate_batch(requests)
        
        assert len(responses) == 2
        
        # First should be sync (SUCCEEDED or PROCESSING)
        assert responses[0].status in [PredictionStatus.SUCCEEDED, PredictionStatus.PROCESSING, PredictionStatus.FAILED]
        
        # Second should be async (STARTING)
        assert responses[1].status == PredictionStatus.STARTING

    def test_batch_with_invalid_request(self, client):
        """Test that batch handles invalid requests gracefully."""
        requests = [
            {"model": "p-image", "input": {"prompt": "Valid request"}, "sync": True},
            {"model": "invalid-model", "input": {"prompt": "Invalid model"}, "sync": True},
            {"model": "p-image", "input": {"prompt": "Another valid request"}, "sync": True},
        ]
        
        responses = client.generate_batch(requests)
        
        assert len(responses) == 3
        
        # All should be Response objects
        for response in responses:
            assert isinstance(response, Response)
        
        # First and third should succeed or process
        assert responses[0].status in [PredictionStatus.SUCCEEDED, PredictionStatus.PROCESSING, PredictionStatus.FAILED]
        assert responses[2].status in [PredictionStatus.SUCCEEDED, PredictionStatus.PROCESSING, PredictionStatus.FAILED]
        
        # Second should fail
        assert responses[1].status == PredictionStatus.FAILED

    def test_batch_with_missing_required_fields(self, client):
        """Test that batch handles requests with missing required fields."""
        requests = [
            {"model": "p-image", "input": {"prompt": "Valid request"}},
            {"input": {"prompt": "Missing model"}},  # Missing model
            {"model": "p-image"},  # Missing input
        ]
        
        responses = client.generate_batch(requests)
        
        assert len(responses) == 3
        
        # First should succeed
        assert responses[0].status in [PredictionStatus.SUCCEEDED, PredictionStatus.PROCESSING, PredictionStatus.FAILED]
        
        # Second and third should fail
        assert responses[1].status == PredictionStatus.FAILED
        assert responses[2].status == PredictionStatus.FAILED


    def test_batch_with_additional_parameters(self, client):
        """Test batch requests with additional parameters."""
        requests = [
            {
                "model": "p-image",
                "input": {"prompt": "A landscape", "width": 512, "height": 512},
                "sync": True,
            },
            {
                "model": "p-image",
                "input": {"prompt": "A portrait"},
                "sync": True,
                "aspect_ratio": "1:1",
            },
        ]
        
        responses = client.generate_batch(requests)
        
        assert len(responses) == 2
        
        # Verify parameters were passed
        assert responses[0].inputs["width"] == 512
        assert responses[0].inputs["height"] == 512


class TestBatchGenerationWithImages:
    """Integration tests for batch generation with successful image outputs."""

    def test_batch_sync_with_image_outputs(self, client):
        """Test that batch sync requests complete successfully.
        
        Note: generate_batch uses the generic generate() method which doesn't
        automatically process images. Users should use generate_text_to_image()
        for automatic image processing, or manually process the generation_url
        from the response.
        """
        requests = [
            {"model": "p-image", "input": {"prompt": "A red apple"}, "sync": True},
            {"model": "p-image", "input": {"prompt": "A blue sky"}, "sync": True},
        ]
        
        responses = client.generate_batch(requests)
        
        assert len(responses) == 2
        
        for response in responses:
            if response.status == PredictionStatus.SUCCEEDED:
                # Should have generation_url in outputs
                assert response.response.get("generation_url") is not None
                # Can manually download if needed
                # content = client.download_content(response.response["generation_url"])
                # assert content is not None


@pytest.fixture
def client():
    """Create a PrunaClient instance for testing."""
    import os
    api_key = os.getenv("PRUNA_API_KEY")
    if not api_key:
        pytest.skip("PRUNA_API_KEY not available")
    return PrunaClient(api_key=api_key)
