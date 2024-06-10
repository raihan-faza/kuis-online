import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MySeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.external_api_url = 'http://localhost:5000/api/users/login'  # Replace with the actual API URL

    def test_login(self):
        self.driver.get(f'{self.live_server_url}/auth/')
        wait = WebDriverWait(self.driver, 10)

        email_input = wait.until(EC.element_to_be_clickable((By.ID, 'email')))
        email_input.send_keys('demian020277@gmail.com')

        password_input = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
        password_input.send_keys('123456')

        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit-login')))
        submit_button.click()
        
        time.sleep(5)
        
        # Check if the expected result from the external API is displayed on the page
        expected_result = "Dashboard Page"
        self.assertIn(expected_result, self.driver.page_source)

    def tearDown(self):
        self.driver.quit()