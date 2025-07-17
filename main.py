from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

#Configuracion de  Selenium y abrir navegador
servicio = Service("chromedriver-win64/chromedriver.exe")
opciones = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=servicio, options=opciones)

#Abrir página principal
driver.get("https://books.toscrape.com")
time.sleep(2)

#Hacer Click en categoría "Fantasy"
driver.find_element(By.LINK_TEXT, "Fantasy").click()
time.sleep(2)

#Capturar datos de todos los libros de la primera página
libros = driver.find_elements(By.CLASS_NAME, "product_pod")

data = []
for libro in libros:
    titulo = libro.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
    precio = libro.find_element(By.CLASS_NAME, "price_color").text
    disponibilidad = libro.find_element(By.CLASS_NAME, "availability").text.strip()

    #Ir a detalle para obtener descripción
    link = libro.find_element(By.TAG_NAME, "a").get_attribute("href")
    driver.execute_script("window.open(arguments[0]);", link)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)

    try:
        descripcion = driver.find_element(By.XPATH, '//div[@id="product_description"]/following-sibling::p').text
    except:
        descripcion = "No disponible"

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    data.append({
        "Título": titulo,
        "Precio": precio,
        "Disponibilidad": disponibilidad,
        "Descripción": descripcion
    })

#Guardar resultados en CSV
df = pd.DataFrame(data)
df.to_csv("libros_fantasy.csv", index=False, encoding='utf-8')

#Captura de pantalla
driver.save_screenshot("pantalla_fantasy.png")

# Cerrar navegador
driver.quit()
