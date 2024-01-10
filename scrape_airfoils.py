from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os

import time

BASE_URL = "http://www.airfoiltools.com/search/index?MAirfoilSearchForm%5BtextSearch%5D=&MAirfoilSearchForm%5BmaxThickness%5D=&MAirfoilSearchForm%5BminThickness%5D=&MAirfoilSearchForm%5BmaxCamber%5D=&MAirfoilSearchForm%5BminCamber%5D=&MAirfoilSearchForm%5Bgrp%5D=&MAirfoilSearchForm%5Bsort%5D=1&yt0=Search"
RANGE_URL = "http://www.airfoiltools.com/userairfoil/index"
DOWNLOADS_PATH = "C:\\Users\\Marco\\Downloads"


def update_range():
    driver = webdriver.Chrome()
    driver.get(RANGE_URL)
    dropdown_element = driver.find_element(By.ID, "MUserAirfoilRecord_lowRe")
    dropdown = Select(dropdown_element)
    dropdown.select_by_value("1000000")

    dropdown_element = driver.find_element(By.ID, "MUserAirfoilRecord_lowNcrit")
    dropdown = webdriver.support.ui.Select(dropdown_element)
    dropdown.select_by_value("9")

    driver.find_element(By.NAME, "yt0").click()

    driver.get(BASE_URL)
    try:
        driver.find_element(
            By.XPATH,
            "//button[contains(@class,'fc-button fc-cta-consent fc-primary-button')]",
        ).click()
    except Exception as e:
        print(e)
        pass
    for i in range(164 - 45):  # num pages
        get_airfoils_data(driver, driver.current_url)
        driver.find_element(By.LINK_TEXT, "Next").click()


def get_airfoils_data(driver, current_url):
    table = driver.find_element(By.CLASS_NAME, "afSearchResult")
    rows = table.find_elements(By.TAG_NAME, "tr")
    i = 0
    while i < len(rows):
        row = rows[i]
        try:
            row.find_element(By.CLASS_NAME, "ad")
            i += 1
            continue
        except Exception as e:
            pass
        airfoil_details_url = row.find_element(
            By.LINK_TEXT, "Airfoil details"
        ).get_attribute("href")
        airfoil_name = airfoil_details_url.split("airfoil=")[-1].strip("-il")
        save_path = os.path.join(os.getcwd(), "data", airfoil_name)
        if os.path.exists(save_path):
            i += 2
            continue
        coords_url = row.find_element(
            By.LINK_TEXT, "Selig format dat file"
        ).get_attribute("href")
        coords = extract_coords(driver, coords_url)
        polar = extract_polar(driver, airfoil_details_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        if isinstance(polar, pd.DataFrame):
            os.mkdir(save_path)
            coords.to_csv(
                os.path.join(save_path, "coords.csv"),
                index=False,
            )
            polar.to_csv(
                os.path.join(save_path, "polar.csv"),
                index=False,
            )
        i += 2


def extract_coords(driver, coords_url):
    driver.execute_script(f"window.open('{coords_url}')")
    driver.switch_to.window(driver.window_handles[-1])
    coords = driver.find_element(By.TAG_NAME, "pre").text
    # remove header
    coords = coords.split("\n")[1:]
    coords = pd.DataFrame(
        [coord.split() for coord in coords], columns=["x", "y"]
    ).astype(float)
    return coords


def extract_polar(driver, airfoil_details_url):
    driver.get(airfoil_details_url)
    try:
        driver.find_element(
            By.XPATH,
            "//button[contains(@class,'fc-button fc-cta-consent fc-primary-button')]",
        ).click()
    except Exception as e:
        print(e)
        pass
    try:
        table = driver.find_element(By.CLASS_NAME, "polar")
    except NoSuchElementException as e:
        return False
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows[:-1]:
        if (
            row.find_element(By.CLASS_NAME, "cell2").text == "1,000,000"
            and row.find_element(By.CLASS_NAME, "cell5").text == "Mach=0 Ncrit=9"
        ):
            polar_details_url = row.find_element(By.LINK_TEXT, "Details").get_attribute(
                "href"
            )
            driver.get(polar_details_url)
            csv_elem = driver.find_element(By.PARTIAL_LINK_TEXT, "1000000.csv")
            file_name = csv_elem.text
            csv_elem.click()
            time.sleep(0.5)
            with open(os.path.join(DOWNLOADS_PATH, file_name), "r") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith("Alpha,Cl"):
                    with open(os.path.join(DOWNLOADS_PATH, file_name), "w") as f:
                        f.writelines(lines[i:])
                    break

            polar_coords = pd.read_csv(os.path.join(DOWNLOADS_PATH, file_name))
            os.remove(os.path.join(DOWNLOADS_PATH, file_name))
            # remove all columns except cl, cd
            polar_coords = polar_coords[["Cl", "Cd"]]
            return polar_coords

    return False


if __name__ == "__main__":
    update_range()
