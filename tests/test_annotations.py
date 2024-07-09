import pytest
from unittest.mock import patch, Mock
from grafana_annotation.annotations import GrafanaAnnotator

@pytest.fixture
def annotator():
    grafana_url = "http://mock-grafana-instance/api"
    api_key = "mock_api_key"
    return GrafanaAnnotator(grafana_url, api_key)

@patch('grafana_annotation.annotations.requests.post')
def test_create_annotation_success(mock_post, annotator):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "message": "Annotation added"}
    mock_post.return_value = mock_response

    # Act
    response = annotator.create_annotation(1625157000, "This is a test annotation")

    # Assert
    assert response == {"id": 1, "message": "Annotation added"}
    mock_post.assert_called_once_with(
        f"http://mock-grafana-instance/api/annotations",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer mock_api_key"
        },
        data='{"time": 1625157000, "text": "This is a test annotation", "tags": ["python"]}'
    )

@patch('grafana_annotation.annotations.requests.post')
def test_create_annotation_failure(mock_post, annotator):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"message": "Bad request"}
    mock_post.return_value = mock_response

    # Act & Assert
    with pytest.raises(Exception):
        annotator.create_annotation(1625157000, "This is a test annotation")

    mock_post.assert_called_once_with(
        f"http://mock-grafana-instance/api/annotations",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer mock_api_key"
        },
        data='{"time": 1625157000, "text": "This is a test annotation", "tags": ["python"]}'
    )
