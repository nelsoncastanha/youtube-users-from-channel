from googleapiclient.discovery import build
import argparse

# Sua API KEY aqui (substitua pela real)
API_KEY = ''


def get_channel_id_by_name(youtube, channel_name):
    search_response = (
        youtube.search()
        .list(q=channel_name, part="snippet", type="channel", maxResults=1)
        .execute()
    )

    if not search_response["items"]:
        raise Exception("Canal não encontrado.")

    return search_response["items"][0]["snippet"]["channelId"]


def get_video_ids(youtube, channel_id, max_videos=5):
    channel = youtube.channels().list(part="contentDetails", id=channel_id).execute()

    uploads_playlist = channel["items"][0]["contentDetails"]["relatedPlaylists"][
        "uploads"
    ]

    videos = (
        youtube.playlistItems()
        .list(part="contentDetails", playlistId=uploads_playlist, maxResults=max_videos)
        .execute()
    )

    return [item["contentDetails"]["videoId"] for item in videos["items"]]


def get_comment_authors(youtube, video_id):
    authors = set()
    comments = (
        youtube.commentThreads()
        .list(part="snippet", videoId=video_id, maxResults=100, textFormat="plainText")
        .execute()
    )

    for item in comments["items"]:
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        name = snippet["authorDisplayName"]
        cid = snippet["authorChannelId"]["value"]
        authors.add((name, cid))

    return authors


def fetch_comment_authors_by_channel_name(channel_name):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    channel_id = get_channel_id_by_name(youtube, channel_name)
    video_ids = get_video_ids(youtube, channel_id)

    all_authors = set()
    for vid in video_ids:
        all_authors.update(get_comment_authors(youtube, vid))

    return all_authors


def main(channel_name):
    authors = fetch_comment_authors_by_channel_name(channel_name)
    print(
        f"\nUsuários que comentaram nos vídeos mais recentes do canal '{channel_name}':\n"
    )
    for name, _ in authors:
        print(f"{name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Buscar usuários que comentaram nos vídeos de um canal"
    )
    parser.add_argument("canal", help="Nome do canal do YouTube")
    args = parser.parse_args()

    main(args.canal)
