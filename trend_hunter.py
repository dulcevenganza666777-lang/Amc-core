import requests, re, json, os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "token.json")
CLIENT_SECRET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "client_secret.json")
EXCLUDED_TAGS = ['shorts', 'china view', 'chinatravel', 'chinatown', '中国旅游', '美丽的中国', 'china', 'travel', 'vlog']
def _auth():
    creds = None
    if os.path.exists(TOKEN_FILE): creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"\n🌐 Abre este enlace:\n{auth_url}")
            code = input("\nPega el código: ")
            flow.fetch_token(code=code)
            creds = flow.credentials
        with open(TOKEN_FILE, "w") as t: t.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)
def get_competitor_data():
    channels = ['UCV21jU2I-cwoUAnHw_M9j5w','UCSQvQmNMP6uC-3zaeCoyifA','UCR0c7RsLmVPV0FSl469ZVLQ','UC7qGin654PkdvJmuugoFeDA']
    youtube = _auth()
    titles, tags = [], []
    for channel_id in channels:
        try:
            req = youtube.search().list(part="id", channelId=channel_id, maxResults=5, order="date", type="video")
            video_ids = [item["id"]["videoId"] for item in req.execute().get("items", [])]
            if video_ids:
                resp2 = youtube.videos().list(part="statistics,snippet", id=",".join(video_ids)).execute()
                for item in resp2.get("items", []):
                    snippet = item.get("snippet", {})
                    titles.append(snippet.get("title", ""))
                    raw_tags = snippet.get("tags", [])
                    tags.extend([t for t in raw_tags if t not in EXCLUDED_TAGS])
        except Exception as e: print(f"[TREND HUNTER] Error en canal {channel_id}: {e}")
    return {"titles": titles, "tags": list(set(tags)), "styles": ["spiral", "bounce", "cascade", "circle"]}
def get_global_search_data():
    queries = ["satisfying physics balls","bouncing balls simulation","particles loop satisfying","oddly satisfying physics","physics simulation shorts"]
    youtube = _auth()
    top_titles, top_tags, seen_ids = [], [], set()
    for query in queries:
        try:
            resp = youtube.search().list(part="id", q=query, type="video", order="viewCount", videoDuration="short", maxResults=10).execute()
            video_ids = [item["id"]["videoId"] for item in resp.get("items", [])]
            if video_ids:
                resp2 = youtube.videos().list(part="statistics,snippet,contentDetails", id=",".join(video_ids)).execute()
                for item in resp2.get("items", []):
                    views = int(item.get("statistics", {}).get("viewCount", 0))
                    if views >= 1_000_000 and item["id"] not in seen_ids:
                        seen_ids.add(item["id"])
                        snippet = item.get("snippet", {})
                        top_titles.append(snippet.get("title", ""))
                        raw_tags = snippet.get("tags", [])
                        top_tags.extend([t for t in raw_tags if t not in EXCLUDED_TAGS])
        except Exception as e: print(f"[TREND HUNTER] Error en query '{query}': {e}")
    return {"top_titles": top_titles[:20], "top_tags": list(set(top_tags)), "top_styles": []}
