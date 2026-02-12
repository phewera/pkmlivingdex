import os
from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from seed import download_image

@pytest.mark.anyio
async def test_download_image_creates_directory():
    # Mocks
    mock_client = AsyncMock()
    mock_client.get.return_value = MagicMock(status_code=200, content=b"fake-image-data")
    
    fake_path = "static/sprites/fake.png"
    fake_dir = "static/sprites"
    
    # We mock os.path.exists to return False so it proceeds to download
    with patch("os.path.exists", return_value=False):
        # We mock os.makedirs to verify it's called
        with patch("os.makedirs") as mock_makedirs:
            # We mock anyio.open_file to avoid actual file writing
            with patch("anyio.open_file", new_callable=AsyncMock) as mock_open:
                # Mock the file context manager
                mock_file = AsyncMock()
                mock_open.return_value.__aenter__.return_value = mock_file
                
                await download_image(mock_client, "http://fake.url/img.png", fake_path)
                
                # Check makedirs called with correctly directory
                mock_makedirs.assert_called_once()
                # Use os.path.normpath to handle potential separator differences on Windows
                called_arg = mock_makedirs.call_args[0][0]
                assert os.path.normpath(called_arg) == os.path.normpath(fake_dir)

@pytest.mark.anyio
async def test_download_image_skips_existing():
    mock_client = AsyncMock()
    fake_path = "static/sprites/existing.png"
    
    # Verify it returns early if file exists
    with patch("os.path.exists", return_value=True):
        await download_image(mock_client, "http://url", fake_path)
        
        mock_client.get.assert_not_called()
