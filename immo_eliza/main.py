
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import csv



url="https://www.immoweb.be/en/search/house/for-sale?countries=BE&minBedroomCount=4&page=1&orderBy=relevance" 
headers= {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

r= requests.get(url,headers=headers)
soup=BeautifulSoup(r.content, 'html.parser')
links=soup.find_all("a", class_="card__title-link")

listings = []

for link in links:
    house_url=link.get("href")
    house_response=requests.get(house_url, headers=headers)
    house_soup=BeautifulSoup(house_response.text, 'html.parser')

    house_data= {}

# Property Type 
    try:
        house_type= house_soup.find('h1', class_='classified__title')
        cleaned_title = house_type.text.replace("for sale", "").strip()
        house_data['Property Type'] = cleaned_title  
    except:
        house_data['Property Type'] = 'None' 

# Property ID
    try:
        immoweb_code = house_soup.find('div', class_='classified__header--immoweb-code')
        code = immoweb_code.text.split(':')
        house_data['Property ID'] = code[1].strip()
    except:
        house_data['Property ID'] = 'None'
    

# Price
    try:
        price_elements = house_soup.find('span', class_='sr-only')
        text= price_elements.text
        prices = text.replace('From ', '').replace('To ', '').replace('€', '').split()
        price_range = '-'.join(prices)
        house_data['Price'] = price_range.strip()
    except:
        house_data['Price'] = 'None'

# Number of Bedrooms
    try:
        info = house_soup.find('p', class_="classified__information--property")
        parts = info.text.split('|')
        bedrooms = parts[0].strip()  # İlk kısmı (bedrooms) al
        no=bedrooms[0:2]
        house_data['Bedrooms'] = no
    except (IndexError, AttributeError):
        house_data['Bedrooms'] = 'None'

# Living Area
    try:
        info = house_soup.find('p', class_="classified__information--property")
        parts = info.text.split('|')
        area = parts[1].strip()
        are=area.split()[0]
        house_data['Living Area'] = are
    except (IndexError, AttributeError):
        house_data['Living Area'] = 'None'

# Kitchen Type
    try:
        kitchen = house_soup.find('th', string='Kitchen type').find_next_sibling('td').contents[0].strip()
        house_data['Kitchen Type'] = kitchen
    except:
        house_data['Kitchen Type'] = 'None'

# Terrace
    try:
        terrace=house_soup.find('th', string=['Terrace', 'Terrace surface']).find_next_sibling('td').contents[0].strip() 
        house_data['Terrace'] = terrace
    except:
        house_data['Terrace'] = 'None'

# Garden
    try:
        garden=house_soup.find('th', string=['Garden surface', 'Garden surface']).find_next_sibling('td').contents[0].strip() 
        house_data['Garden'] = garden
    except:
        house_data['Garden'] = 'None'

# Furnished
    try:
        furnish=house_soup.find('th', string='Furnished').find_next_sibling('td').contents[0].strip() 
        house_data['Furnished'] = furnish
    except:
         house_data['Furnished'] = 'None'      

    listings.append(house_data)

 # İlanları bir DataFrame'e çevir        
df = pd.DataFrame(listings)

# DataFrame'i CSV dosyasına kaydet
csv_file_path = 'house_list.csv'  # CSV dosya ismi
df.to_csv(csv_file_path, index=False)  # index=False ile indeks sütunu eklenmez




 

