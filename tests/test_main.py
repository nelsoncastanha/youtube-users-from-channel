import pytest
from src.main import get_channel_id_by_name, get_video_ids, get_comment_authors


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
