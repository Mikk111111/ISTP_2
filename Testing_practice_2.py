from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time,threading,math

app = Flask(__name__)

# HTML for the first page (with the button)
first_page_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Start Code Execution</title>
</head>
<body>
    <h1>Welcome to the Code Execution Page</h1>
    <button onclick="window.location.href='/start_execution'">Start Code Execution</button>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(first_page_html)

# Function to handle the Selenium task
def selenium_task():
    firefox_options = Options()
    # firefox_options.add_argument("--headless")  # Comment out for non-headless mode for debugging
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    try:
        driver.get('http://suninjuly.github.io/alert_accept.html')
        time.sleep(0.5)
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        button.click()
        alert = Alert(driver)
        alert.accept()
        time.sleep(0.5)
        driver.get('http://suninjuly.github.io/alert_redirect.html')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'input_value')))
        # Solve the math problem (ln(abs(12 * sin(x))))
        x_value = driver.find_element(By.ID, 'input_value').text
        result = str(eval('math.log(abs(12 * math.sin(' + x_value + ')))', {'math': math}))

        answer_field = driver.find_element(By.ID, 'answer')
        answer_field.send_keys(result)
        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()
        time.sleep(0.5)

    finally:
        driver.quit()

@app.route('/start_execution')
def start_execution():
    # Use threading to run the selenium_task asynchronously and prevent blocking
    threading.Thread(target=selenium_task).start()
    return 'Code execution has started. Please check the browser.'

if __name__ == '__main__':
    app.run(debug=False)  # Disable Flask debug mode
