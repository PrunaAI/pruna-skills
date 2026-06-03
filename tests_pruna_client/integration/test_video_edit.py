"""Integration tests for video editing with VACE model."""

from pruna_client.models import PredictionStatus


class TestVideoEditFlow:
    """Integration tests for video editing flow with VACE model."""

    def test_vace_model(self, client):
        """Test video generation with vace model using async polling."""
        response = client.generate_video_edit(
            model="vace",
            prompt="A person walking through a magical forest with glowing trees",
            sync=False,
        )
        final_response = client.poll_status(response=response)
        assert final_response.status == PredictionStatus.SUCCEEDED
