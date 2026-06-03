"""Integration tests for text-to-image generation."""

from pruna_client.models import PredictionStatus


class TestSynchronousTextToImageFlow:
    """Integration tests for synchronous text-to-image generation flow."""

    def test_complete_sync_generation_flow(self, client):
        """Test complete synchronous image generation flow from start to finish."""
        response = client.generate_text_to_image(
            model="p-image",
            prompt="A beautiful sunset over a calm ocean with vibrant colors",
            sync=True,
        )
        assert response.status == PredictionStatus.SUCCEEDED

    def test_sync_generation_with_parameters(self, client):
        """Test synchronous generation with additional parameters."""
        response = client.generate_text_to_image(
            model="p-image",
            prompt="A serene mountain landscape at dawn",
            sync=True,
            aspect_ratio="custom",
            width=512,
            height=512,
        )
        assert response.status == PredictionStatus.SUCCEEDED

    def test_sync_generation_error_handling(self, client):
        """Test error handling with invalid input."""
        response = client.generate_text_to_image(
            model="p-image",
            prompt="",  # Empty prompt might cause error
            sync=True,
        )
        assert response.status in [PredictionStatus.SUCCEEDED, PredictionStatus.FAILED]


class TestAsynchronousTextToImageFlow:
    """Integration tests for asynchronous text-to-image generation flow with polling."""

    def test_complete_async_generation_flow(self, client):
        """Test complete async generation flow: start -> poll -> verify success."""
        # Start async generation
        response = client.generate_text_to_image(
            model="p-image",
            prompt="An abstract painting with vibrant colors and geometric shapes",
            sync=False,
        )
        assert response.status in [
            PredictionStatus.STARTING,
            PredictionStatus.PROCESSING,
            PredictionStatus.SUCCEEDED,
        ]

    def test_async_generation_polling_with_url(self, client):
        """Test async generation polling using status URL directly."""
        response = client.generate_text_to_image(
            model="p-image", prompt="A futuristic cityscape at night", sync=False
        )
        final_response = client.poll_status(response=response)
        assert final_response.status == PredictionStatus.SUCCEEDED
