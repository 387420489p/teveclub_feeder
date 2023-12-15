#!/usr/bin/python3
import sys
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def wait_for_element(driver, by, value, timeout=10):
    try:
        element_present = EC.presence_of_element_located((by, value))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(f"Timed out waiting for element {by}: {value}")

def login(driver, username, password):
    driver.get('https://teveclub.hu/')
    wait_for_element(driver, By.NAME, 'tevenev')
    driver.find_element(By.NAME, 'tevenev').send_keys(username)
    driver.find_element(By.NAME, 'pass').send_keys(password, Keys.ENTER)

def feed_teve(driver):
    for k in range(7, -1, -1):
        try:
            select_etetes = Select(driver.find_element(By.NAME, "kaja"))
            select_etetes.select_by_value(str(k))
            time.sleep(0.5)
            select_itatas = Select(driver.find_element(By.NAME, "pia"))
            select_itatas.select_by_value(str(k))
            time.sleep(0.5)
            etet_gomb = driver.find_element(
                By.XPATH, "//input[@name='etet'][@type='submit']")
            etet_gomb.click()
            print(str(k) + " adag kaja és pia odaadva!")
            break
        except NoSuchElementException:
            if k == 0:
                print("Nem volt éhes.")
            pass

def teach_teve(driver):
    driver.get('https://teveclub.hu/tanit.pet')
    time.sleep(2)
    try:
        select_tanitas = Select(driver.find_element(By.NAME, "tudomany"))
        select_tanitas.select_by_value("1")
    except NoSuchElementException:
        pass
    try:
        tanitas_gomb = driver.find_element(By.NAME, "learn")
        tanitas_gomb.click()
        print("Tanítás sikeres!")
    except NoSuchElementException:
        print("Ma már tanult.")
        pass

def play_number_game(driver):
    egyszam = randint(100, 420)
    driver.get('https://teveclub.hu/egyszam.pet')
    time.sleep(3)
    try:
        egyszam_mezo = driver.find_element(By.NAME, "honnan")
        egyszam_mezo.send_keys(egyszam)
        time.sleep(2)
        egyszam_mezo.send_keys(Keys.ENTER)
        print(f"Egyszámjáték sikeres! Megjátszott szám: {egyszam}")
    except NoSuchElementException:
        try:
            tipp = driver.find_element(
                By.XPATH, "//span[@class='kiem'][2]").text
            print(f"Ma már játszott egyszámjátékot. Tippje: {tipp}")
        except NoSuchElementException:
            pass

def handle_messages(driver, leltarszam):
    driver.get('https://teveclub.hu/inbox.pet')
    time.sleep(2)
    try:
        level_gomb = driver.find_element(
            By.XPATH, "//img[@alt='Olvasd el ezt a levelet!']")
        level_gomb.click()
        time.sleep(1)

        if leltarszam[1] + " AL" in driver.page_source:
            print("\nGRATULÁLOK! Nyertél egy vagy több datolyát az egyszámjátékon!\n")
        else:
            print("Sajnos nem nyertél az egyszámjátékon.")
        driver.get('https://teveclub.hu/inbox.pet')

    except NoSuchElementException:
        pass

def main():
    with open('./pw.txt', 'r') as f:
        cp = f.readlines()

    tevek_szama = int(len(cp)/2)
    driver = webdriver.Chrome()

    for i in range(0, len(cp), 2):
        try:
            login(driver, cp[i].strip(), cp[i + 1].strip())
            time.sleep(2)

            # Néha van, hogy az Újdonságok oldal jön be login után, ezt kerüljük ki itt
            driver.get('https://teveclub.hu/myteve.pet')

            if "Teve Legyen Veled!" in driver.page_source:
                leltarszam = [
                    elem.get_attribute("href").split("=")[1] for elem in driver.find_elements(By.XPATH, "//a[@href]") if "usernumber=" in elem.get_attribute("href")
                ]
                print(f"Sikeres bejelentkezés! Teve: {cp[i].strip()} Leltárszáma: {leltarszam[0]}")
            else:
                sys.exit("Sikertelen bejelentkezés, ismeretlen hiba.")
            time.sleep(2)

            # Perform other actions (feeding, teaching, playing game, handling messages)
            feed_teve(driver)
            teach_teve(driver)
            play_number_game(driver)
            handle_messages(driver, leltarszam)

            # Logout
            logout_button = driver.find_element(By.NAME, "menu7")
            logout_button.click()
            print("Sikeres kijelentkezés.")
            time.sleep(2)

        except Exception as e:
            print(f"Error for Teve {cp[i].strip()}: {str(e)}")

    # Close the browser window
    driver.quit()

if __name__ == "__main__":
    main()
