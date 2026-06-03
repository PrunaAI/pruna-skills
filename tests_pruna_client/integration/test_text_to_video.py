"""Integration tests for text-to-video generation."""

from pruna_client.models import PredictionStatus


class TestTextToVideoFlow:
    """Integration tests for text-to-video generation flow."""

    def test_wan_t2v_model(self, client):
        """Test text-to-video generation with wan-t2v model using async polling."""
        response = client.generate_text_to_video(
            model="wan-t2v",
            prompt="A sports car is driving very fast along a beach at sunset, aerial drone shot, cinematic",
            sync=False,
        )
        final_response = client.poll_status(response=response)
        assert final_response.status == PredictionStatus.SUCCEEDED
