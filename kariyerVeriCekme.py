import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

def kariyer_net_ozet_cek(url):
    # Web sayfasını al
    response = requests.get(url)

    # Hata kontrolü
    if response.status_code != 200:
        print("Hata: Sayfa yüklenemedi.")
        return None

    # BeautifulSoup nesnesi oluştur
    soup = BeautifulSoup(response.content, "html.parser")

    # Şirket adını al
    company_name_tag = soup.find("a", class_="company-name company-name-hover")
    if company_name_tag:
        company_name = company_name_tag.get_text(strip=True)
    else:
        company_name = "Şirket adı bulunamadı"

    # İş pozisyonunu al
    job_title_tag = soup.find("span", style="box-shadow:transparent 0 0;")
    if job_title_tag:
        job_title = job_title_tag.get_text(strip=True)
    else:
        job_title = "İş pozisyonu bulunamadı"

    # Genel nitelikler ve iş tanımını al
    qualifications_section = soup.find("div", class_="job-detail-content")
    if qualifications_section:
        qualifications_heading = qualifications_section.find("h2", string="GENEL NİTELİKLER VE İŞ TANIMI")
        if qualifications_heading:
            qualifications_data = qualifications_heading.find_next_sibling()
            qualifications = qualifications_data.get_text("\n", strip=True)
        else:
            qualifications = "Genel nitelikler ve iş tanımı bulunamadı"
    else:
        qualifications = "Genel nitelikler ve iş tanımı bölümü bulunamadı"

    # Aday kriterlerini al
    criteria_section = soup.find("h2", string="Aday Kriterleri")
    if criteria_section:
        parent_section = criteria_section.find_parent("div", class_="aligment-container my-3")
        if parent_section:
            criteria_items = parent_section.find_all("label")
            criteria_text = "\n".join([f"{label.get_text(strip=True)}: {label.find_next_sibling().get_text(strip=True)}" if label.find_next_sibling() else f"{label.get_text(strip=True)}: Veri bulunamadı" for label in criteria_items if label.find_next_sibling() is not None])
        else:
            criteria_text = "Aday kriterleri bulunamadı"
    else:
        criteria_text = "Aday kriterleri başlığı bulunamadı"

    # Verileri sözlük olarak döndür
    return {"Şirket": company_name, "İş Pozisyonu": job_title, "Genel Nitelikler ve İş Tanımı": qualifications, "Aday Kriterleri": criteria_text}

while True:
    # Kariyer.net'in iş ilanları sayfasının URL'sini al
    url = input("Lütfen Kariyer.net'in iş ilanları sayfasının URL'sini girin (Çıkmak için q tuşuna basın): ")

    if url.lower() == 'q':
        print("Program sonlandırılıyor...")
        break

    # Kariyer.net'ten şirket adı, iş pozisyonu, genel nitelikler ve iş tanımını çek
    ozet = kariyer_net_ozet_cek(url)

    if ozet is not None:
        # Verileri ekrana yazdır
        print("\nŞirket:", ozet["Şirket"])
        print("\nİş Pozisyonu:", ozet["İş Pozisyonu"])
        print("\nGenel Nitelikler ve İş Tanımı:")
        print(ozet["Genel Nitelikler ve İş Tanımı"])
        print("\nAday Kriterleri:")
        print(ozet["Aday Kriterleri"])
        print("\n")

        # Verileri Excel dosyasına yaz
        try:
            existing_data = pd.read_excel('ilan_kar.xlsx')
        except FileNotFoundError:
            existing_data = None

        new_data = pd.DataFrame([ozet])

        if existing_data is not None:
            all_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            all_data = new_data

        all_data.to_excel('ilan_kar.xlsx', index=False)
