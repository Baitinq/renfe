from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import logging
import os
from dotenv import load_dotenv


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    load_dotenv()

    test_ua = "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"

    options = Options()

    # options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
    # options.add_argument("--window-size=1920,1080")

    options.add_argument(f"--user-agent={test_ua}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)

    loginRenfe(driver)

    navigate_to_tickets(driver)

    main_loop(driver)

    logging.info("TICKET BOUGHT!!")

    sleep(999999999)


def loginRenfe(driver):
    driver.get("https://venta.renfe.com/vol/loginParticular.do")

    sleep(5)

    driver.find_element(By.ID, "num_tarjeta").send_keys(os.getenv("RENFE_EMAIL"))
    driver.find_element(By.ID, "pass-login").send_keys(os.getenv("RENFE_PASSWORD"))
    driver.find_element(By.ID, "loginButtonId").click()

    sleep(15)


def navigate_to_tickets(driver):
    driver.get("https://venta.renfe.com/vol/myPassesCard.do")

    sleep(5)

    element = driver.find_element(By.XPATH, "//a[contains(@onclick, 'submitNew')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    sleep(2)
    driver.execute_script("arguments[0].click();", element)

    sleep(5)

    # todo: select radio button ida o vuelta

    datepicker = driver.find_element(By.ID, "fecha1")
    driver.execute_script(f"arguments[0].value = '06/01/2025';", datepicker)

    element = driver.find_element(By.ID, "submitSiguiente")
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    sleep(2)
    driver.execute_script("arguments[0].click();", element)

    sleep(5)


def main_loop(driver):
    select_button = None
    while True:
        # if this is not found, then we presume we have to login again
        try:
            row = driver.find_element(By.XPATH, f"//tr[td[contains(text(), '18.50')]]")
        except Exception:
            loginRenfe(driver)
            navigate_to_tickets(driver)
            continue
        try:
            select_button = row.find_element(
                By.XPATH, ".//button[contains(text(), 'Seleccionar')]"
            )
            break
        except Exception:
            logging.info("No available places - refreshing...")
            driver.refresh()
            sleep(15)
            continue
    driver.execute_script("arguments[0].scrollIntoView(true);", select_button)
    sleep(2)
    driver.execute_script("arguments[0].click();", select_button)

    sleep(5)

    element = driver.find_element(By.ID, "submitSiguiente")
    driver.execute_script("arguments[0].click();", element)


if __name__ == "__main__":
    main()
