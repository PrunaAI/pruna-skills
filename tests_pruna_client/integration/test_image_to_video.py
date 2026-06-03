"""Integration tests for image-to-video generation."""

from pruna_client.models import PredictionStatus


class TestImageToVideoFlow:
    """Integration tests for image-to-video generation flow."""

    def test_wan_i2v_model(self, client, sample_image):
        """Test image-to-video generation with wan-i2v model using async polling."""
        response = client.generate_image_to_video(
            model="wan-i2v",
            prompt="The camera slowly pushes in, gentle movement",
            image=sample_image,
            sync=False,
        )
        final_response = client.poll_status(response=response)
        assert final_response.status == PredictionStatus.SUCCEEDED
