#!/usr/bin/python3
import sys
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

with open('pw.txt', 'r') as f:
    cp = f.readlines()

i = 0
tevek_szama = int(len(cp)/2)
driver = webdriver.Chrome()

for teve in range(tevek_szama):
    # login
    driver.get('https://teveclub.hu/')
    time.sleep(2)
    print("\n\n-----------------------------------------------")
    print("Oldal megnyitva.")

    id_box = driver.find_element(By.NAME, 'tevenev')
    id_box.send_keys(cp[0+i].strip())
    id_box = driver.find_element(By.NAME, 'pass')
    id_box.send_keys(cp[1+i].strip(), Keys.ENTER)
    time.sleep(2)


    if "Teve Legyen Veled!" in driver.page_source:
        linkek = driver.find_elements(By.XPATH, "//a[@href]")
        for elem in linkek:
            if "usernumber=" in elem.get_attribute("href"):
                leltarszam = elem.get_attribute("href")
                leltarszam = leltarszam.split("=")
        print(f"Sikeres bejelentkezés! Teve: {cp[0+i]} Leltárszáma: {leltarszam[1]}")
    elif "Vagy a tevéd nevét, vagy a hívójelét eltévesztetted!" in driver.page_source:
        sys.exit("Sikertelen bejelentkezés. Hibás név vagy jelszó.")
    else:
        sys.exit("Sikertelen bejelentkezés, ismeretlen hiba.")
    time.sleep(2)

    # etetes beta
    for k in range(7, -1, -1):
        try:
            select_etetes = Select(driver.find_element(By.NAME, "kaja"))
            select_etetes.select_by_value(str(k))
            time.sleep(0.5)
            select_itatas = Select(driver.find_element(By.NAME, "pia"))
            select_itatas.select_by_value(str(k))
            time.sleep(0.5)
            etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
            etet_gomb.click()
            print(str(k) + " adag kaja és pia odaadva!")
        except NoSuchElementException:
            #TODO
            # a teve nem volt éhes
            pass

    # tanitas
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

    # egyszám játék
    egyszam = randint(100, 420)
    driver.get('https://teveclub.hu/egyszam.pet')
    time.sleep(2)
    try:
        egyszam_mezo = driver.find_element(By.NAME, "honnan")
        egyszam_mezo.send_keys(egyszam)
        time.sleep(1)
        egyszam_mezo.send_keys(Keys.ENTER)
        print(f"Egyszámjáték sikeres! Megjátszott szám: {egyszam}")
    except NoSuchElementException:
        try:
            tipp = driver.find_element(By.XPATH, "//span[@class='kiem'][2]").text
            print(f"Ma már játszott egyszámjátékot. Tippje: {tipp}")
        except NoSuchElementException:
            pass

    # levelek megnyitása, elolvasása, hogy nertél-e & törlése
    driver.get('https://teveclub.hu/inbox.pet')
    time.sleep(2)
    try:
        level_gomb = driver.find_element(By.XPATH, "//img[@alt='Olvasd el ezt a levelet!']")
        level_gomb.click()
        time.sleep(1)

        if leltarszam[1] + " AL" in driver.page_source:
            print("\nGRATULÁLOK! Nyertél egy vagy több datolyát az egyszámjátékon!\n")
        else:
            print("Sajnos nem nyertél az egyszámjátékon.")
        driver.get('https://teveclub.hu/inbox.pet')

    except NoSuchElementException:
        pass
    try:
        kijeloles_gomb = driver.find_element(By.XPATH, "//input[@value='kijelöl mindet'][@type='button']")
        kijeloles_gomb.click()
        torles_gomb = driver.find_element(By.NAME, "deleteall")
        torles_gomb.click()
        obj = driver.switch_to.alert
        time.sleep(0.5)
        obj.accept()
        print("Üzenet(ek) sikeresen törölve!")
    except NoSuchElementException:
        print("Nincs törölni való üzenet.")
        pass

    # logout
    logout_button = driver.find_element(By.NAME, "menu7")
    logout_button.click()
    i += 2
    print("Sikeres kijelentkezés.")
