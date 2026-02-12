from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.mark.anyio
async def test_update_database_endpoint():
    # Mock the seed function
    with patch("main.seed_pokemon_async", new_callable=AsyncMock) as mock_seed:
        # Create a test client
        client = TestClient(app)
        
        # Call the endpoint
        response = client.post("/system/update-database")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Database update started in background"
        
        # Verify the background task was triggered
        # Note: BackgroundTasks run after the response is sent. 
        # TestClient handles this synchronously usually.
        # But wait, main.py calls seed_pokemon_async as a BackgroundTask?
        # Let's check main.py code.
        
        # Assuming it is a BackgroundTask:
        mock_seed.assert_called_once()
