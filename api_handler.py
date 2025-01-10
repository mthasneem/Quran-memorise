import requests
import os

def fetch_sura_list():
    try:
        response = requests.get("https://api.alquran.cloud/v1/surah")
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print("Error fetching sura list:", e)
        return []

def fetch_ayah(sura_number, ayah_number):
    try:
        url = f"https://api.alquran.cloud/v1/ayah/{sura_number}:{ayah_number}/editions/quran-simple,ar.alafasy"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('data'):
            ayah_text = data['data'][0]['text']  # Quran text
            audio_url = data['data'][1]['audio']  # Audio URL (from alafasy recitation)
            return ayah_text, audio_url
        else:
            print(f"Ayah {ayah_number} not found in Sura {sura_number}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ayah {ayah_number} of Sura {sura_number}:", e)
        return None, None

def download_audio(audio_url, file_path):
    try:
        response = requests.get(audio_url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if it doesn't exist
        with open(file_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return False