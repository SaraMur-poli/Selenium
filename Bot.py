import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
chrome_options.add_argument("--start-maximized")  
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--ignore-certificate-errors")  
chrome_options.add_argument("--disable-logging")  
chrome_options.add_argument("--log-level=3")

service = Service("driver/chromedriver.exe")
driver = webdriver.Chrome(service = service, options = chrome_options)

url = "https://www.viajesexito.com"
driver.get(url)

print(f"Open page: {driver.title}")


try:

    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#\\39 9b8a2c4-84a1-445d-89e3-c7c1ca9a7f65 > div > iframe"))
    )
    driver.switch_to.frame(iframe) 
    print("Switch to the Pop-up iframe")

    closeButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "bhr-ip__c__close"))
    )
    closeButton.click()
    print("Pop-up closed successfully")

    driver.switch_to.default_content()

    time.sleep(3) 

    paquetes_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="paquetesTooltips"]/a'))
    )
    paquetes_link.click()
    print("Click made in flight+hotel")

    time.sleep(3) 

    texto_origen = "José María Cordova"
    pyperclip.copy(texto_origen)  

    campo_origen = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="CityPredictiveFrom_netactica_airhotel"]'))
    )
    campo_origen.click()  

    time.sleep(3) 

    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    print("Pasted text and click on the origin city")

    time.sleep(3) 

    texto_destino = "(CUN-Aeropuerto Internacional de Cancún)"
    pyperclip.copy(texto_destino) 

    campo_destino = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="CityPredictiveTo_netactica_airhotel"]'))
    )
    campo_destino.click()  

    time.sleep(3) 

    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    print("Pasted text and click on the destination city ")

    time.sleep(3)

    xpath_aeropuerto = "//li[@item-name='Cancún, Quintana Roo (CUN-Aeropuerto Internacional de Cancún)']"
    aeropuerto_element = driver.find_element(By.XPATH, xpath_aeropuerto)
    aeropuerto_element.click()

    time.sleep(3) 

    fecha_salida_js = """
        let fechaSalida = document.getElementById('DateFrom_netactica_airhotel');
        fechaSalida.value = '26-12-2024';
        fechaSalida.dispatchEvent(new Event('change', { bubbles: true }));
    """
    driver.execute_script(fecha_salida_js)
    print("Departure date: 26-12-2024")

    time.sleep(3)

    fecha_regreso_js = """
        let fechaRegreso = document.getElementById('DateTo_netactica_airhotel');
        fechaRegreso.value = '05-01-2025';
        fechaRegreso.dispatchEvent(new Event('change', { bubbles: true }));
    """
    driver.execute_script(fecha_regreso_js)
    print("Return date: 05-01-2025")

    time.sleep(5)
    boton_agregar_habitacion_js = """
        let boton = document.getElementById('btbAddRoomtwopaquetes');
        boton.click();
    """

    time.sleep(5)
    driver.execute_script(boton_agregar_habitacion_js)
    print("A second room was added")

    time.sleep(5)
    habitacion_1_js = """
        let habitacion1 = document.querySelector('#ddlAirHotelNumberAdults');
        habitacion1.value = '2';
        habitacion1.dispatchEvent(new Event('change', { bubbles: true }));
    """
    
    time.sleep(3)
    driver.execute_script(habitacion_1_js)
    print("First room configured for 2 people")

    habitacion_2_js = """
        let habitacion2 = document.getElementById('ddlAirHotelNumberAdultsDos');
        habitacion2.value = '3';
        habitacion2.dispatchEvent(new Event('change', { bubbles: true }));
    """
    driver.execute_script(habitacion_2_js)
    print("Second room configured for 3 people")
    time.sleep(5)


    boton_buscar_js = """
    let botonBuscar = document.getElementById('sbm_netactica_airhotel');
    botonBuscar.click();
    """
    driver.execute_script(boton_buscar_js)
    print("Click on the search button")

except Exception as e:
    print(f"Error filling in the fields: {e}")

#Manejo de la nueva ventana y extraccion de precios de paquetes
try:

    print("Esperando que se abra la nueva ventana...")
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

    ventanas = driver.window_handles
    print(f"Ventanas abiertas: {len(ventanas)}")

    driver.switch_to.window(ventanas[-1])
    print("Se cambió a la ventana de resultados.")

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.totalpackprice.small-text-center.price-extra.money"))
    )
    print("Los precios específicos de los paquetes se han cargado correctamente.")

    precios_paquetes = driver.find_elements(By.CSS_SELECTOR, "p.totalpackprice.small-text-center.price-extra.money")
    print("Precios de los paquetes encontrados:")

    for precio in precios_paquetes:

        precio_texto = precio.find_element(By.CLASS_NAME, "currencyText").text.strip()
        print(precio_texto)
    
    time.sleep(2)

except Exception as e:
    print(f"Error: {e}")

time.sleep(3)    

#Parte de las opciones avanzadas y la aerolinea
try:

    aerolinea = "avianca (AV)"

    opciones_avanzadas_js = """
    let botonOpcionesAvanzadas = document.querySelector("a.active-button");
    botonOpcionesAvanzadas.click();
    """
    driver.execute_script(opciones_avanzadas_js)
    print("Click en el botón de 'Opciones Avanzadas' realizado.")

    time.sleep(3)  

    campo_aerolinea_js = """
    let campoAero = document.getElementById('txtAirlineCode');
    campoAero.click();
    """
    driver.execute_script(campo_aerolinea_js)
    print("Click en el campo de aerolínea realizado.")

    time.sleep(3)  

    pegar_aerolinea_js = f"""
    let campoAero = document.getElementById('txtAirlineCode');
    campoAero.value = '{aerolinea}';
    campoAero.dispatchEvent(new Event('input', {{ bubbles: true }}));  // Simular entrada
    """
    driver.execute_script(pegar_aerolinea_js)
    print(f"Valor '{aerolinea}' ingresado en el campo de aerolínea y Enter presionado.")

    time.sleep(2) 

    click_boton_js = """
    let botonBuscar = document.querySelector('input.button.expanded.round.small.btnPackageDoNewSearch');
    if (botonBuscar) botonBuscar.click();
    """
    driver.execute_script(click_boton_js)
    print("Click realizado en el botón de buscar.")

except Exception as e:
    print(f"Error durante la interacción con 'Opciones Avanzadas': {e}")

#Segunda extraccion de precios en base a la aerolinea
try:

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.totalpackprice.small-text-center.price-extra.money"))
    )
    print("Los precios específicos de los paquetes se han cargado correctamente.")

    precios_paquetes = driver.find_elements(By.CSS_SELECTOR, "p.totalpackprice.small-text-center.price-extra.money")
    print("Precios de los paquetes encontrados segun la aerolinea:")

    for precio in precios_paquetes:

        precio_texto = precio.find_element(By.CLASS_NAME, "currencyText").text.strip()
        print(precio_texto)
    
    time.sleep(2)

except Exception as e:
    print(f"Error: {e}")

#Click al numero de whatsApp de la agencia
click_whatsapp_js = """
let botonWhatsApp = document.querySelector('a[href*="https://api.whatsapp.com/send"]');
if (botonWhatsApp) botonWhatsApp.click();
"""
driver.execute_script(click_whatsapp_js)
print("Click realizado en el botón de WhatsApp.")

time.sleep(5)
driver.quit()

