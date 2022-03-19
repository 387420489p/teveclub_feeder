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
    print(i)
    # login
    driver.get('https://teveclub.hu/')
    time.sleep(2)
    print("Oldal megnyitva.")


    id_box = driver.find_element(By.NAME, 'tevenev')
    id_box.send_keys(cp[0+i].strip())
    id_box = driver.find_element(By.NAME, 'pass')
    id_box.send_keys(cp[1+i].strip(), Keys.ENTER)
    time.sleep(2)

    if "Teve Legyen Veled!" in driver.page_source:
        print(f"Sikeres bejelentkezés {cp[0+i]}-hez!")
    elif "Vagy a tevéd nevét, vagy a hívójelét eltévesztetted!" in driver.page_source:
        sys.exit("Sikertelen bejelentkezés. Hibás név vagy jelszó.")
    else:
        sys.exit("Sikertelen bejelentkezés, ismeretlen hiba.")


    # etetes
    try:
        select_etetes = Select(driver.find_element(By.NAME, "kaja"))
        select_etetes.select_by_value("7")
        time.sleep(0.5)
        select_itatas = Select(driver.find_element(By.NAME, "pia"))
        select_itatas.select_by_value("7")
        time.sleep(0.5)
        etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
        etet_gomb.click()
        print("7 adag kaja és pia odaadva!")
    except NoSuchElementException:
        try:
            select_etetes = Select(driver.find_element(By.NAME, "kaja"))
            select_etetes.select_by_value("6")
            time.sleep(0.5)
            select_itatas = Select(driver.find_element(By.NAME, "pia"))
            select_itatas.select_by_value("6")
            time.sleep(0.5)
            etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
            etet_gomb.click()
            print("6 adag kaja és pia odaadva!")
        except NoSuchElementException:
            try:
                select_etetes = Select(driver.find_element(By.NAME, "kaja"))
                select_etetes.select_by_value("5")
                time.sleep(0.5)
                select_itatas = Select(driver.find_element(By.NAME, "pia"))
                select_itatas.select_by_value("5")
                time.sleep(0.5)
                etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
                etet_gomb.click()
                print("5 adag kaja és pia odaadva!")
            except NoSuchElementException:
                try:
                    select_etetes = Select(driver.find_element(By.NAME, "kaja"))
                    select_etetes.select_by_value("4")
                    time.sleep(0.5)
                    select_itatas = Select(driver.find_element(By.NAME, "pia"))
                    select_itatas.select_by_value("4")
                    time.sleep(0.5)
                    etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
                    etet_gomb.click()
                    print("4 adag kaja és pia odaadva!")
                except NoSuchElementException:
                    try:
                        select_etetes = Select(driver.find_element(By.NAME, "kaja"))
                        select_etetes.select_by_value("3")
                        time.sleep(0.5)
                        select_itatas = Select(driver.find_element(By.NAME, "pia"))
                        select_itatas.select_by_value("3")
                        time.sleep(0.5)
                        etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
                        etet_gomb.click()
                        print("3 adag kaja és pia odaadva!")
                    except NoSuchElementException:
                        try:
                            select_etetes = Select(driver.find_element(By.NAME, "kaja"))
                            select_etetes.select_by_value("2")
                            time.sleep(0.5)
                            select_itatas = Select(driver.find_element(By.NAME, "pia"))
                            select_itatas.select_by_value("2")
                            time.sleep(0.5)
                            etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
                            etet_gomb.click()
                            print("2 adag kaja és pia odaadva!")
                        except NoSuchElementException:
                            try:
                                select_etetes = Select(driver.find_element(By.NAME, "kaja"))
                                select_etetes.select_by_value("1")
                                time.sleep(0.5)
                                select_itatas = Select(driver.find_element(By.NAME, "pia"))
                                select_itatas.select_by_value("1")
                                time.sleep(0.5)
                                etet_gomb = driver.find_element(By.XPATH, "//input[@name='etet'][@type='submit']")
                                etet_gomb.click()
                                print("1 adag kaja és pia odaadva!")
                            except NoSuchElementException:
                                print("A teve nem volt éhes.")
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
    egyszam = randint(1, 300)
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

    # levelek megynitása & törlése
    driver.get('https://teveclub.hu/inbox.pet')
    time.sleep(2)
    try:
        for n in range(1, 7):
            level_gomb = driver.find_element(By.XPATH, "//img[@alt='Olvasd el ezt a levelet!'][i]")
            level_gomb.click()
            time.sleep(1)
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
