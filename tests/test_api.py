def test_stock_api_endpoint(client):
    """
    Tests the /api/stock/<ticker> endpoint.
    GIVEN a Flask application client
    WHEN the '/api/stock/AAPL' page is requested (GET)
    THEN check that the response is valid
    """
    # Make a GET request to the API endpoint
    response = client.get('/api/stock/AAPL')

    # 1. Check for a successful response code
    assert response.status_code == 200

    # 2. Check that the response content type is JSON
    assert response.content_type == 'application/json'

    # 3. Parse the JSON and check the data's structure
    data = response.get_json()
    assert isinstance(data, list) # The data should be a list of records
    assert len(data) > 0 # The list should not be empty
    assert 'ticker' in data[0] # Each record should have a 'ticker' key
    assert data[0]['ticker'] == 'AAPL' # The ticker should be correct