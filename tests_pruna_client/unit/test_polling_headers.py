import os
from unittest.mock import MagicMock, patch

import pytest

from pruna_client import PrunaClient, Response
from pruna_client.models import PredictionStatus


class TestPollingHeaders:
    @pytest.fixture
    def client(self):
        return PrunaClient(api_key="test_key")

    def test_poll_status_uses_defaults(self, client):
        """Test that defaults are used when no headers are provided."""
        response = Response(
            id="test_id",
            model="test_model",
            inputs={},
            status=PredictionStatus.STARTING,
            response={"get_url": "http://test.url"},
        )

        with (
            patch("time.sleep") as mock_sleep,
            patch.object(client, "_request_with_retry") as mock_request,
            patch.object(client, "download_content", return_value=b"fake_content"),
        ):
            # First response has no headers
            mock_response1 = MagicMock()
            mock_response1.ok = True
            mock_response1.json.return_value = {"status": "processing"}
            mock_response1.headers = {}

            # Second response is success
            mock_response2 = MagicMock()
            mock_response2.ok = True
            mock_response2.json.return_value = {
                "status": "succeeded",
                "generation_url": "http://gen.url",
            }
            mock_response2.headers = {}

            mock_request.side_effect = [mock_response1, mock_response2]

            client.poll_status(response=response)

            # Should use default poll interval (1 second based on DEFAULT_POLL_INTERVAL)
            mock_sleep.assert_called_with(
                float(os.getenv("DEFAULT_PRUNA_POLL_INTERVAL"))
            )

    def test_poll_status_respects_x_max_wait_header(self, client):
        """Test that X-Max-Wait header is used for timeout, not poll interval."""
        response = Response(
            id="test_id",
            model="test_model",
            inputs={},
            status=PredictionStatus.STARTING,
            response={"get_url": "http://test.url"},
        )

        with (
            patch("time.sleep") as mock_sleep,
            patch.object(client, "_request_with_retry") as mock_request,
            patch.object(client, "download_content", return_value=b"fake_content"),
        ):
            # First response has X-Max-Wait header
            mock_response1 = MagicMock()
            mock_response1.ok = True
            mock_response1.json.return_value = {"status": "processing"}
            mock_response1.headers = {"X-Max-Wait": "5.5"}

            # Second response is success
            mock_response2 = MagicMock()
            mock_response2.ok = True
            mock_response2.json.return_value = {
                "status": "succeeded",
                "generation_url": "http://gen.url",
            }
            mock_response2.headers = {}

            mock_request.side_effect = [mock_response1, mock_response2]

            client.poll_status(response=response)

            # Should use default poll interval (1.0) since X-Max-Wait only affects timeout
            mock_sleep.assert_called_with(
                float(os.getenv("DEFAULT_PRUNA_POLL_INTERVAL"))
            )

    def test_poll_status_respects_x_poll_interval_header(self, client):
        """Test that X-Poll-Interval header is used for poll interval (sleep time)."""
        response = Response(
            id="test_id",
            model="test_model",
            inputs={},
            status=PredictionStatus.STARTING,
            response={"get_url": "http://test.url"},
        )

        with (
            patch("time.sleep") as mock_sleep,
            patch.object(client, "_request_with_retry") as mock_request,
            patch.object(client, "download_content", return_value=b"fake_content"),
        ):
            # First response has X-Poll-Interval header
            mock_response1 = MagicMock()
            mock_response1.ok = True
            mock_response1.json.return_value = {"status": "processing"}
            mock_response1.headers = {"X-Poll-Interval": "3.0"}

            # Second response is success
            mock_response2 = MagicMock()
            mock_response2.ok = True
            mock_response2.json.return_value = {
                "status": "succeeded",
                "generation_url": "http://gen.url",
            }
            mock_response2.headers = {}

            mock_request.side_effect = [mock_response1, mock_response2]

            client.poll_status(response=response)

            # Should use X-Poll-Interval value (3.0) for sleep time
            mock_sleep.assert_called_with(3.0)

