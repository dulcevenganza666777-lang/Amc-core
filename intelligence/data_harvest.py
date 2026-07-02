import sqlite3
from googleapiclient.discovery import build
# Necesitarás tener instalado: pip install google-api-python-client

def get_youtube_service():
    # Aquí usarías tus credenciales ya autenticadas
    return build('youtube', 'v3', developerKey='TU_API_KEY_AQUI') 

def harvest_my_channel(channel_id):
    youtube = get_youtube_service()
    conn = sqlite3.connect('v14_ceo_brain.db')
    cursor = conn.cursor()
    
    # 1. Obtener videos del canal
    request = youtube.search().list(part="snippet", channelId=channel_id, maxResults=10, type="video")
    response = request.execute()
    
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        
        # 2. Obtener estadísticas
        stats = youtube.videos().list(part="statistics", id=video_id).execute()
        views = stats['items'][0]['statistics'].get('viewCount', 0)
        
        # 3. Guardar en tu base de datos
        # Nota: Como la API no da retención gratis, asignamos 0 por defecto para que el Brain detecte que necesita actualizar esto
        cursor.execute("INSERT OR REPLACE INTO video_metrics VALUES (?,?,?,?,?)", 
                       (video_id, title, 0.0, int(views), 'auto_harvested'))
        print(f"✅ Harveasted: {title} | Vistas: {views}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Pon aquí tu ID de canal real
    harvest_my_channel("TU_CHANNEL_ID_AQUI")
