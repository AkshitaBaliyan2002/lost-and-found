import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

import app as app_module
from app import app

URL = "http://127.0.0.1:5001"


@pytest.fixture(scope="module")
def server():
    app_module.items.clear()
    t = threading.Thread(target=lambda: app.run(port=5001), daemon=True)
    t.start()
    time.sleep(1.5)
    yield


@pytest.fixture
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()


def test_report_and_claim_item(server, driver):
    driver.get(URL)
    driver.find_element(By.ID, "name").send_keys("Blue Umbrella")
    driver.find_element(By.ID, "place").send_keys("Library")
    driver.find_element(By.ID, "add-btn").click()
    assert "Blue Umbrella" in driver.find_element(By.ID, "item-list").text
    driver.find_element(By.LINK_TEXT, "Mark claimed").click()
    assert "CLAIMED" in driver.find_element(By.ID, "item-list").text