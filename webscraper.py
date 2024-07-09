# import external libraries.
import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
# run server
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# set xvfb display since there is no GUI in docker container.
if platform.system() == 'Linux':
    display = Display(visible=0, size=(800, 600))
    display.start()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--headless')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# basic routes
@app.get("/")
def translate_text():
    print('building session')
    if platform.system() == 'Linux':
        chromedriver_path = os.path.join(os.getcwd(),'chromedriver','chromedriver-linux64','chromedriver')
    else:
        chromedriver_path = os.path.join(os.getcwd(),'chromedriver','chromedriver_mac')

    print(f'dirver path: {chromedriver_path}')

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    print('ggggggg 1')
    driver.get('https://www.google.com/')
    print('ggggggg 2')
    time.sleep(2)
    driver.close()
    if platform.system() == 'Linux':
        # close chromedriver and display
        display.stop()
    return datetime.now()

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
