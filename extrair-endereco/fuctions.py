import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.parse
import re
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from time import sleep
import os
import shutil


def extrair_dominio(link):
    # Encontra a posição do "url=" para começar a extração
    inicio_url = link.find("url=") + 4
    # Encontra o final da URL antes dos parâmetros adicionais
    fim_url = link.find("&", inicio_url)

    # Extrai a URL completa
    url_completa = link[inicio_url:fim_url]

    # Usa urllib para obter o domínio base
    parsed_url = urllib.parse.urlparse(url_completa)
    dominio = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    return dominio


def criar_diretorio_e_mover_arquivos(diretorio, arquivos):
    # Criando o diretório se ele não existir
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print(f'Diretório "{diretorio}" criado com sucesso.')
    else:
        print(f'Diretório "{diretorio}" já existe.')

    # Movendo os arquivos para o diretório criado
    for arquivo in arquivos:
        if os.path.isfile(arquivo):
            shutil.move(arquivo, diretorio)
            print(f'Arquivo "{arquivo}" movido para "{diretorio}".')
        else:
            print(f'Arquivo "{arquivo}" não encontrado.')


def extraindo_do_google(url):

    def extrair_https(urlextracao):
        # Encontrar a posição de "https://"
        posicao_https = url.find("https://")

        # Se "https://" for encontrado, retornar a parte da string a partir dele
        if posicao_https != -1:
            return urlextracao[posicao_https:]
        else:
            return None  # Retornar None se "https://" não for encontrado

    # Fazendo a requisição GET ao Google
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    link_google = url

    response = requests.get(link_google, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        content = response.content

        # Parseando o conteúdo HTML
        site = BeautifulSoup(content, 'html.parser')

        # Usando seletores CSS para capturar todas as tags <a> que têm um <h3> como filho, sem especificar a classe
        tags_a = site.select('a:has(h3)')

        # Lista para armazenar os hrefs
        hrefs = []

        # Iterando sobre as tags <a> e extraindo os atributos href
        for tag in tags_a:
            if 'href' in tag.attrs:
                hrefs.append(tag['href'])
    else:
        print(f"Erro ao acessar o site. Status code: {response.status_code}")

    # Extraindo links do google

    links_final = []

    for link in hrefs:
        resultado = extrair_https(link)
        if resultado != None:
            links_final.append(link)

    print(f'Consegui encontrar {
          len(links_final)} sites nessa pagina do google')

    return links_final


def salvar_excel(lista_a, lista_b, nome):
    # Criando um DataFrame a partir das listas com os nomes das colunas "sites" e "outra_coluna"
    df = pd.DataFrame({
        'SITE': lista_a,
        'EMAIL': lista_b
    })

    nome_planilha = 'pagina-' + nome + '.xlsx'

    # Salvando em um arquivo Excel
    df.to_excel(nome_planilha, index=False)


def limpeza_final_dominio(url):
    # Usando regex para extrair o domínio
    dominio = re.search(r'://(www\.)?(.+?)(/|$)', url)
    return dominio.group(2) if dominio else None


def extracao_selenium(url):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('window-size=400,800')

    navegador = webdriver.Edge(options=options)

    link_pesquisa = 'https://registro.br/tecnologia/ferramentas/whois?search=' + url

    navegador.get(link_pesquisa)

    sleep(3)

    site = BeautifulSoup(navegador.page_source, 'html.parser')

    # Extraindo o conteúdo do bloco <pre>
    pre_content = site.find('pre', style='display: none;').get_text(strip=True)

    # Processando o conteúdo para encontrar titular e e-mail
    lines = pre_content.split('\n')

    email = None

    for line in lines:
        if 'e-mail:' in line:
            email = line.split(':')[1].strip()

    navegador.quit()  # Fechar o navegador após a execução

    return email


def extrair_dominio_email(endere):

    lista_links_do_google = extraindo_do_google(endere)

    global link_limpo
    global email_limpo

    link_limpo = []
    email_limpo = []

    for lista_item in lista_links_do_google:

        limpando_url = extrair_dominio(lista_item)
        limpeza_profunda_dominio = limpeza_final_dominio(limpando_url)
        link_limpo.append(limpeza_profunda_dominio)

        email_desse_site = extracao_selenium(limpeza_profunda_dominio)

        email_limpo.append(email_desse_site)

    return link_limpo, email_limpo
