"""Integration tests for image editing."""
import base64
from io import BytesIO

from PIL import Image

from pruna_client.models import PredictionStatus


class TestImageEditingFlow:
    """Integration tests for image editing flow."""

    def test_complete_image_edit_flow_with_file_path(self, client, temp_image_file):
        """Test complete image editing flow: upload -> edit -> verify success."""
        response = client.generate_image_edit(
            model="p-image-edit",
            prompt="Make the image blue and add a sunset sky",
            images=[temp_image_file],
            sync=True,
        )
        assert response.status == PredictionStatus.SUCCEEDED

    def test_image_edit_flow_with_pil_image(self, client, sample_image):
        """Test image editing flow using PIL Image object."""
        response = client.generate_image_edit(
            model="p-image-edit",
            prompt="Transform the image into a watercolor painting style",
            images=[sample_image],
            sync=True,
        )
        assert response.status == PredictionStatus.SUCCEEDED

    def test_image_edit_flow_with_data_uri(self, client, sample_image):
        """Test image editing flow using data URI."""
        # Convert image to data URI
        buffer = BytesIO()
        sample_image.save(buffer, format="PNG")
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        data_uri = f"data:image/png;base64,{image_data}"

        response = client.generate_image_edit(
            model="p-image-edit",
            prompt="Add a beautiful landscape background",
            images=[data_uri],
            sync=True,
        )
        assert response.status == PredictionStatus.SUCCEEDED

    def test_image_edit_flow_with_multiple_images(self, client, sample_image):
        """Test image editing flow with multiple images."""
        # Create second image
        image2 = Image.new("RGB", (200, 200), color="blue")

        response = client.generate_image_edit(
            model="p-image-edit",
            prompt="Blend and merge these images into a cohesive composition",
            images=[sample_image, image2],
            sync=True,
        )
        assert response.status == PredictionStatus.SUCCEEDED
