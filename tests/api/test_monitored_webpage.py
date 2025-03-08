def test_list_webpages(test_client):
    response = test_client.get('/monitored-webpage')
    assert len(response.json()) == 0
