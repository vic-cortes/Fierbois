from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas

def get_links(soup):
    links_pagina = []
    for link in soup.find_all('a'):
        direccion_link = link.get('href',None)
        try: 
            if "Extra_FlowController_1id" in direccion_link: 
                if direccion_link not in links_pagina:
                    links_pagina.append(direccion_link)
        except:
            print("")
    return links_pagina

def clean_string(input_string):
    input_string =str(input_string)
    input_string =input_string.replace("\xa0","")
    input_string =input_string.replace("\r","")
    input_string =input_string.replace("\n","")
    input_string =input_string.replace("<label>","")
    input_string =input_string.replace("</label>","")
    input_string =input_string.replace("</td>","")
    input_string =input_string.replace("</span>","")
    input_string =input_string.strip()
    lista_string = input_string.split(':') 
    return lista_string[1]

def get_links(soup):
    links_pagina = []
    for link in soup.find_all('a'):
        direccion_link = link.get('href',None)
        try: 
            if "Extra_FlowController_1id" in direccion_link: 
                if direccion_link not in links_pagina:
                    links_pagina.append(direccion_link)
        except:
            print("")
    return links_pagina

def extract_data(soup_pagina):
    page_table = soup_pagina.find_all('table')
    td_table = page_table[5].find_all('td')
    i = 4
    lista_respuestas = []
    while i < 24:
        lista_respuestas.append(clean_string(td_table[i]))
        i = i + 1
    return lista_respuestas

def extract_page(url):
    request_pagina = requests.get(url)
    soup_pagina = BeautifulSoup(request_pagina.text)
    data =extract_data(soup_pagina)
    return data

driver = webdriver.Firefox()
driver.get("http://ssp.gob.mx/extraviadosWeb/portals/extraviados.portal")
age_element = driver.find_element_by_name("Extra_FlowController_1wlw-select_key:{actionForm.edad}")
age_element.send_keys("Ma")
search_element =driver.find_element_by_name("Submit")
search_element.click()
soup=BeautifulSoup(driver.page_source,"lxml")
links_pagina = get_links(soup)
lista_registros = []
while len(links_pagina)>0:
    for link in links_pagina:
        data = extract_page(link)
        lista_registros.append(data)
    driver.get('http://ssp.gob.mx:80/extraviadosWeb/portals/extraviados.portal?_nfpb=true&_st=&_windowLabel=Extra_FlowController_1&Extra_FlowController_1_actionOverride=%2FConsulta%2FExtra_Flow%2Fsiguientes')
    soup=BeautifulSoup(driver.page_source,"lxml")
    links_pagina = get_links(soup)
df_lista_registros.to_csv("mujeres_ninas_mayores.csv", quoting=csv.QUOTE_ALL)