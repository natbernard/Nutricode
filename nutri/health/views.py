import requests
import certifi
import django
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render

BASE_JUMIA_URL = 'https://www.jumia.co.ke/catalog/?q={}'
BASE_NAIVAS_URL = 'https://www.naivas.co.ke/search?q={}'

# Create your views here.
def home(request):
    return render(request, 'landing.html')


# def price_search(item):
#     #search = request.POST.get('search')
#     print(quote_plus(item))
#     print(certifi.where())
#     final_url = BASE_JUMIA_URL.format(quote_plus(item))
#     print(final_url)
#     html_object = requests.get(final_url, verify=certifi.where())
#     webpage = html_object.text
#     soup = BeautifulSoup(webpage, features='html.parser')
#     #print(soup.prettify())
#     price = soup.find_all('div', {'class': 'prc'})

#     try:
#         money = price[0].text
#     except IndexError:
#         money = "Nothing"
#     #disease_search()
    
#     return money

def price_search_naivas(item):
    print(quote_plus(item))
    print(certifi.where())
    final_url = BASE_NAIVAS_URL.format(quote_plus(item))
    print(final_url)
    html_object = requests.get(final_url, verify = False)
    webpage = html_object.text
    soup = BeautifulSoup(webpage, features = 'html.parser')
    price = soup.find_all('span', {'class': 'product-price txt-md'})

    try:
        money = price[0].text
    except IndexError:
        money = "Nothing"

    return money
    

def disease_search(request):
    SITE_URL = 'https://www.britannica.com/science/nutritional-disease'
    web_page = requests.get(SITE_URL, verify=certifi.where())
    html_doc = web_page.content
    scraper = BeautifulSoup(html_doc, features='html.parser')
    table = scraper.body.table.find_all('tr')
    search = request.POST.get('search')
    tr = list(table)
    
    link_to_get_parent = ()
    for i in range(3, 9):
        disease_data = tr[i].find_all('td', {'scope': 'row'})
        for a in disease_data:
            link = a.find('a')
            if search.lower() in link.text:
                link_to_get_parent = link
            else:
                print('not in database')

    list_of_all_data_in_parent = list(link_to_get_parent.parent.parent.find_all('td'))
    disease_name = list_of_all_data_in_parent[0].text
    disease_symptoms = list_of_all_data_in_parent[1].text
    disease_diet = list_of_all_data_in_parent[2].text
    print(disease_name)
    print(disease_symptoms)
    diet_list = disease_diet.split(',')
    
    for food in diet_list:
        print(price_search_naivas(food))
            

    frontend_display = {
        'search': disease_name,
        'disease_symptoms': disease_symptoms,
        'disease_diet': disease_diet,
    }
    return render(request, 'health/new_search.html', frontend_display)
    




