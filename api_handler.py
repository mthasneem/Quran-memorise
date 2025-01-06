import requests

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
        url = f"https://api.alquran.cloud/v1/ayah/{sura_number}:{ayah_number}/editions/quran-simple"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('data'):
            ayah_text = data['data'][0]['text']
            return ayah_text
        else:
            print(f"Ayah {ayah_number} not found in Sura {sura_number}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ayah {ayah_number} of Sura {sura_number}:", e)
        return None