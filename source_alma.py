import requests

def webSource(url):
    # Web sayfasını al
    response = requests.get(url)

    # Hata kontrolü
    if response.status_code != 200:
        print("Hata: Sayfa yüklenemedi.")
        return None

    # HTML içeriğini döndür
    return response.text

# Kariyer.net'in iş ilanları sayfasının URL'sini al
url = input("Lütfen siteninin iş ilanları sayfasının URL'sini girin: ")

# Sitenin iş ilanları sayfasının HTML kaynak kodunu al
source = webSource(url)

# HTML kaynak kodunu ekrana yazdır
if source:
    print(source)
else:
    print("Sayfa kaynağı alınamadı.")