import pytest
import tmdb_client
from unittest.mock import Mock
from app import app


def test_get_poster_url_default_size():
    poster_api_path = "some-poster-path"
    expected_default_size = "w342"

    poster_url = tmdb_client.get_poster_url(path=poster_api_path)
    assert expected_default_size in poster_url


def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies(8, list_name="popular")
    assert movies_list is not None


def test_get_movies_list(monkeypatch):
    mock_movies_list = ["Movie 1", "Movie 2"]
    request_mock = Mock()
    response = request_mock.return_value
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.requests.get", request_mock)
    movies_list = tmdb_client.get_movies_list(list_name="popular")
    assert movies_list == mock_movies_list


def test_get_single_movie(monkeypatch):
    mock_movie = {"movie_key": "movie_data"}
    request_mock = Mock()
    request_mock.return_value = mock_movie
    monkeypatch.setattr("tmdb_client.call_tmdb_api", request_mock)
    movie = tmdb_client.get_single_movie(1)
    assert movie == mock_movie


def test_get_single_image(monkeypatch):
    mock_images = {"backdrops": [{"file_path": "Image 1"},
                                 {"file_path": "Image 1"}]
                   }
    request_mock = Mock()
    request_mock.return_value = mock_images
    monkeypatch.setattr("tmdb_client.call_tmdb_api", request_mock)
    image = tmdb_client.get_single_image(4)
    assert image == "Image 1"


def test_get_single_movie_cast(monkeypatch):
    mock_cast = {"cast": ["Actor 1"]}
    request_mock = Mock()
    request_mock.return_value = mock_cast
    monkeypatch.setattr("tmdb_client.call_tmdb_api", request_mock)
    cast = tmdb_client.get_single_movie_cast(2)
    assert cast == mock_cast["cast"]


def test_homepage(monkeypatch):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        api_mock.assert_called_once_with('movie/popular')


@pytest.mark.parametrize('list_type, result_code', (
        ("popular", 200),
        ("top_rated", 200),
        ("upcoming", 200),
        ("now_playing", 200)
))
def test_homepage_lists(monkeypatch, list_type, result_code):
    api_mock = Mock(return_value={"results": []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(f"/?list_type={list_type}")
        assert response.status_code == result_code
        api_mock.assert_called_once_with(f"movie/{list_type}")
