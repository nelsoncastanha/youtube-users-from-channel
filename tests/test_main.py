import pytest
from src.main import (
    get_channel_id_by_name,
    get_video_ids,
    get_comment_authors,
    fetch_comment_authors_by_channel_name
)


def test_get_channel_id_by_name_success(mocker):
    mock_youtube = mocker.Mock()
    mock_youtube.search().list().execute.return_value = {
        "items": [{"snippet": {"channelId": "123"}}]
    }

    result = get_channel_id_by_name(mock_youtube, "Canal Teste")
    assert result == "123"


def test_get_channel_id_by_name_not_found(mocker):
    mock_youtube = mocker.Mock()
    mock_youtube.search().list().execute.return_value = {"items": []}

    with pytest.raises(Exception, match="Canal não encontrado."):
        get_channel_id_by_name(mock_youtube, "Canal Inexistente")


def test_get_video_ids(mocker):
    mock_youtube = mocker.Mock()
    mock_youtube.channels().list().execute.return_value = {
        "items": [{"contentDetails": {"relatedPlaylists": {"uploads": "playlist123"}}}]
    }
    mock_youtube.playlistItems().list().execute.return_value = {
        "items": [
            {"contentDetails": {"videoId": "abc"}},
            {"contentDetails": {"videoId": "def"}},
        ]
    }

    result = get_video_ids(mock_youtube, "channel123")
    assert result == ["abc", "def"]


def test_get_comment_authors(mocker):
    mock_youtube = mocker.Mock()
    mock_youtube.commentThreads().list().execute.return_value = {
        "items": [
            {
                "snippet": {
                    "topLevelComment": {
                        "snippet": {
                            "authorDisplayName": "User A",
                            "authorChannelId": {"value": "channelA"},
                        }
                    }
                }
            }
        ]
    }

    result = get_comment_authors(mock_youtube, "video123")
    assert result == {("User A", "channelA")}


def test_fetch_comment_authors_by_channel_name(mocker):
    mock_youtube = mocker.Mock()

    # Mock build() para retornar o mock_youtube
    mocker.patch("src.main.build", return_value=mock_youtube)

    # Mock para get_channel_id_by_name
    mock_youtube.search().list().execute.return_value = {
        "items": [{"snippet": {"channelId": "123"}}]
    }

    # Mock para get_video_ids
    mock_youtube.channels().list().execute.return_value = {
        "items": [{"contentDetails": {"relatedPlaylists": {"uploads": "playlist123"}}}]
    }
    mock_youtube.playlistItems().list().execute.return_value = {
        "items": [
            {"contentDetails": {"videoId": "vid1"}},
            {"contentDetails": {"videoId": "vid2"}},
        ]
    }

    # Mock para get_comment_authors
    mock_youtube.commentThreads().list().execute.side_effect = [
        {
            "items": [
                {
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {
                                "authorDisplayName": "Alice",
                                "authorChannelId": {"value": "chanA"},
                            }
                        }
                    }
                }
            ]
        },
        {
            "items": [
                {
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {
                                "authorDisplayName": "Bob",
                                "authorChannelId": {"value": "chanB"},
                            }
                        }
                    }
                }
            ]
        },
    ]

    result = fetch_comment_authors_by_channel_name("Canal Exemplo")
    assert result == {("Alice", "chanA"), ("Bob", "chanB")}
