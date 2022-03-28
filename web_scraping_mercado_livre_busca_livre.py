# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 16:24:47 2022

@author: Usuario
"""


from selenium import webdriver
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager



pesquisar = str(input(' O que você quer comprar?'))


driver = webdriver.Chrome(ChromeDriverManager().install())

url_ml = "https://www.mercadolivre.com.br/"

driver.get(url_ml)


campo_busca_ml = driver.find_element_by_xpath('//input[@aria-label="Digite o que você quer encontrar"]')

campo_busca_ml.send_keys(pesquisar)

campo_busca_ml.send_keys(Keys.RETURN)

pagina_inicial_ml = int(driver.find_element_by_xpath('//span[@class="andes-pagination__link"]').text)

pagina_final_ml = int(driver.find_element_by_xpath('//li[@class = "andes-pagination__page-count"]').text[3:])

referencia = driver.find_element_by_xpath('//li[@class="andes-pagination__button andes-pagination__button--next"]//a')


proxima_pagina = referencia.get_attribute('href')

driver.get(proxima_pagina)

chave_next = proxima_pagina[:-2]

#no mercado livre

produtos_ml = []
preco_ml = []
descricaoProdutoLista_ml = []

for i in range(51, 1000, 50):
    driver.get(chave_next + str(i))
    driver.implicitly_wait(1)

    tituloProduto = driver.find_elements_by_xpath('//h2[@class="ui-search-item__title"]')
    precoProduto = driver.find_elements_by_class_name('price-tag-fraction')

    descricaoProduto = driver.find_elements_by_xpath('//div[@class="ui-search-result__content-wrapper"]')

    for x in tituloProduto:
        produtos_ml.append(x.text)

    for x in precoProduto:
        preco_ml.append(x.text)
        

    for x in descricaoProduto:
         descricaoProdutoLista_ml.append(x.text)
         
driver.close()


df_ml = pd.DataFrame()

df_ml['card_ml'] = descricaoProdutoLista_ml

df_ml['produto'] = df_ml['card_ml'].apply(lambda x: '\n'.join(re.findall('\A.*', str(x))))

df_ml['antes'] = df_ml['card_ml'].apply(lambda x: '\n'.join(re.findall('(?<=Antes:\s)\d+', x)))
df_ml['preco_cleaning_1'] = df_ml['card_ml'].apply(lambda x: re.sub(r'.+(?<=Antes:\s)\d+.*|R\$', '', x ))
df_ml['preco_atual'] = df_ml['preco_cleaning_1'].apply(lambda x:  '\n'.join(re.findall(r'(?<!x)\n(\d+(?=\sreais\n))', x)))
        
df_ml['preco_atual'] = df_ml['preco_atual'].apply(lambda x: '0' if len(x) == 0 else x)

df_ml['preco_atual'] = df_ml['preco_atual'].astype('int64')

df_ml = df_ml.loc[df_ml['preco_atual'] != 0]

df_ml.to_csv('df_ml.csv')
df_ml.to_excel('df_ml.xlsx')
df_ml.to_jason('df_ml.json', orient = 'table')