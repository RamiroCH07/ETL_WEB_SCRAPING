from selenium import webdriver #importamos el módulo webdriver de la librería selenium
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
from time import sleep
import sys

#%% Abrir mavegador Chrome con el recurso requerido
url = "https://www.coes.org.pe/Portal/portalinformacion/demanda?indicador=maxima" # URL del recurso HTML
driver = webdriver.Chrome('/.chromedriver.exe')  # en una variable guardamos un objeto webdriver.Chrome
driver.maximize_window()
driver.get(url) # el objeto driver adquiere una url mediante uno e sus métodos
sleep(5)
#%% Acceder al frame que contiene los datos de interés
frame_data = driver.find_element('xpath','//*[@id="ifrMaximaDemanda"]')
driver.switch_to.frame(frame_data)
sleep(5)
#%% Interacción con los elementos dinámicos del recurso HTML
##Cambiar la fecha en el input text 
meses = ["01","02","03","04","05","06","07","08","09","10","11","12"]
años = ["2018"]
for año in años:
    for mes in meses:
        ##Cambiar la fecha en el input text 
        periodo_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="mes"]')))
        driver.execute_script("arguments[0].setAttribute('value',"+"'"+mes+" "+año+"'"+")",periodo_input)

        #Hacer click en el botón "consultar"
        consultar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="btnConsultar"]')))
        consultar_button.click()
        sleep(40)
        #%% Recuperamos el recurso HTML en formato de texto y hacemos uso de la librería BS
        html = driver.page_source
        with open("htmls/html"+mes+"_"+año+".html","w",encoding = "utf-8") as f:
            f.write(html)
#Cerramos el driver google
driver.quit()
#Eliminamos todas las variables
sys.modules[__name__].__dict__.clear()