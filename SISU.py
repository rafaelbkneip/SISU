from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from time import sleep
from selenium.webdriver.common.keys import Keys
import os
import glob

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
navegador = webdriver.Chrome(ChromeDriverManager().install(), options=options)

navegador.get("https://sisu.mec.gov.br/#/selecionados")

#Counter / Contador
cont = 1

while(True):

    navegador.refresh()
    sleep(10)

    #Move the page to the instituition list / Move a página para a lista de instituições 
    quadro = navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[1]/h2')
    navegador.execute_script("arguments[0].scrollIntoView(true)", quadro)  

    #Show the list / Abre a lista
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[1]/div[2]/ng-select[1]/div/div/div[2]/input').click()
    sleep(2)

    #Next instituiton / Próxima instituição
    for j in range(cont):
        navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[1]/div[2]/ng-select[1]/div/div/div[2]/input').send_keys(Keys.ARROW_DOWN)
    #Select the corresponding instituiton / Seleciona a instituição correspondente
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[1]/div[2]/ng-select[1]/div/div/div[2]/input').send_keys(Keys.ENTER)
    sleep(2)
    #Move to the next input field / Mover para o próximo campo de texto
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[1]/div[2]/ng-select[2]/div/div/div[2]/input').send_keys(Keys.ENTER)

    #The .csv files contain information about all the campuses, courses, course types, and time combinations for that institution: the user just needs to select one of them in the options to enable the file download option /
    #O arquivo .csv contém informações obre todas as combinações de campus, cursos, graus e turnos para a instituição: o usuário precisa acessar uma dela nas opções para habilitar a opção de download do arquivo
    #Campus
    sleep(2)
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[2]/div[2]/ng-select[1]/div/div/div[2]/input').send_keys(Keys.ENTER)
    sleep(2)
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[2]/div[2]/ng-select[1]/div/div/div[2]/input').send_keys(Keys.ENTER)

    #Course / Curso
    sleep(2)
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[2]/div[2]/ng-select[2]/div/div/div[2]/input').send_keys(Keys.ENTER)
    sleep(2)
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[2]/div[2]/ng-select[2]/div/div/div[2]/input').send_keys(Keys.ENTER)

    #Course type and time / Grau e turno
    sleep(2)
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[3]').click()

    #Download
    #Move the page to the download button / Mover a página para o botão de download
    sleep(10)
    data_quadro = navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[2]/div[3]')
    navegador.execute_script("arguments[0].scrollIntoView(true)", data_quadro)  
    WebDriverWait(navegador,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="interna"]/div/div[3]/div[1]/div[4]/a')))
    navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[3]/div[1]/div[4]/a').click()
    sleep(10)

    #Rename
    #Instituition name / Nome da instituição
    ies = (navegador.find_element(By.XPATH, '//*[@id="interna"]/div/div[3]/div[1]/div[1]/div/div[1]').text.replace("/", "-"))
    print(ies)

    #Get the last downloaded file / Pegar o último arquivo baixado
    list_of_files = glob.glob('path' '\\*csv') 
    latest_file = max(list_of_files, key=os.path.getmtime)
    print(latest_file)

    #Raise an error if the file already exists, that is, the loop breaks when it tries to download the file from the same institution for the second time/
    #Erro quando o arquivo já existe, isso é, o loop é quebrado quando o programa tenta baixar o arquivo de uma mesma instituição pela segunda vez
    try:
        os.rename(latest_file, 'path' + ies +'.csv')
        cont = cont + 1
    except:
        break