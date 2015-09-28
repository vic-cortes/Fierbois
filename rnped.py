from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas
import time
import csv

def extract_list(driver):
    tabla_completa = []
    table_rows = driver.find_elements_by_xpath("//tr[@role='row']")
    for row in table_rows:
        if row.text != "Fecha País Entidad Clave de entidad Municipio Clave del municipio País de nacimiento Nacionalidad Sexo":
            elementos_fila = []
            elements = row.find_elements_by_tag_name("td")
            print(len(elements))
            for element in elements:
                elementos_fila.append(element.text)
            if len(elementos_fila) != 0: tabla_completa.append(elementos_fila)
    return tabla_completa

driver = webdriver.Firefox()
driver.get("https://rnped.segob.gob.mx/")
time.sleep(3)
#fuero_comun= driver.find_element_by_partial_link_text("Fuero Común")
#fuero_comun.click()
#time.sleep(3)
sex_box = driver.find_element_by_id("federal_c_sexo")
#sex_box = driver.find_element_by_id("comun_c_sexo")
sex_box.send_keys("Mu")
sex_box.click()
sex_box.send_keys(Keys.RETURN)
search_federal= driver.find_element_by_id("busca_federal")
#search_federal= driver.find_element_by_id("busca_comun")
search_federal.click()
time.sleep(1)
lista_inicial = extract_list(driver)
next_page = driver.find_element_by_id("t_federal_next")
is_next_disabled = driver.find_elements_by_xpath("//a[@class='paginate_button next disabled']")
while len(is_next_disabled) == 1:
    works = 0
    while works == 0:
        works = 1
        try:
            next_page.click()
            time.sleep(1)
            lista_actual = extract_list(driver)
        except:
            works = 0
        lista_inicial = lista_inicial + lista_actual
        next_page = driver.find_element_by_id("t_federal_next")
        is_next_disabled = driver.find_elements_by_xpath("//a[@class='paginate_button next disabled']")
    print(next_page)
with open("Mujeres_Federal.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(lista_inicial)