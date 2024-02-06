ENDPOINT="database-2.cvwhw7xmj43j.ap-south-1.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="ap-south-1b"
DBNAME="postgres"
PASS = "January2021"
SECRET = '04bd3a7c4cb7c026bc2816ae907a6ef6d711ba100cbd6bd904532bd5ee37043c'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import psycopg2
import json
import pandas as pd
import time

def sql():
    global conn, cur
    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
        cur = conn.cursor()
    except Exception as e:
        print("ERROR",e)

def sql_query(query):
    global cur
    try:
        cur.execute(query)
    except:
        sql()
        cur.execute(query) 

query = "Select url from gmb_website_status"
sql_query(query)
res = cur.fetchall()
options = webdriver.ChromeOptions() 
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')
# options.add_argument("--disable-popup-blocking")

def form_submission(driver):
    reservation_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/a/div")
    driver.execute_script("arguments[0].click();", reservation_btn)
    name = driver.find_element(By.XPATH, '//*[@id="name"]')
    name.send_keys("Deepesh")
    phone = driver.find_element(By.XPATH, '//*[@id="phone"]')
    phone.send_keys("7987215728")
    submit_btn = driver.find_element(By.XPATH,'//*[@id="submit"]')
    driver.execute_script("arguments[0].click();", submit_btn)
    try:
        success = driver.find_element(By.XPATH,'//*[@id="success"]')
        return {"result":"success"}
    except:
        print("ERROR : ",res[0])
        return {"result":"success"}

res = ["https://wow-wax-co.chrone.work"]
report = {}
for r in res:
    driver = webdriver.Chrome('chromedriver',chrome_options=options)
    action = ActionChains(driver)
    # driver.get(r[0])
    driver.get(r)
    driver.maximize_window()
    # form_submission_res = form_submission(driver)
    report['url']=r
    report['url_open']  = "success"
    try:
        banner_img = driver.find_element(By.XPATH, '//*[@class="bannerimg"]')
        report['banner_img'] = banner_img.get_attribute("src")

        banner_title = driver.find_element(By.XPATH, '//*[@class="banner-title"]')
        report['banner_title'] = banner_title.text

        banner_text = driver.find_element(By.XPATH, '//*[@class="banner-text"]')
        report['banner_text'] = banner_text.text

        services_img = driver.find_element(By.XPATH, '//*[@class="image-3"]')
        report['services_img'] = services_img.get_attribute("src")

        services_cont = driver.find_element(By.XPATH, '//*[@id="services"]')
        report['services_cont'] = "success"

        categories = driver.find_elements(By.XPATH, '//*[contains(@class,"question-text")]')
        report['categories'] = len(categories)

        services = driver.find_elements(By.XPATH, '//*[@class="service-item-row"]')
        report['services'] = len(services)

        testimonial_cont = driver.find_element(By.XPATH, '//*[@id="testimonials"]')
        action.move_to_element(testimonial_cont).perform()
        report['testimonial_cont'] = "success"

        testimonials = driver.find_elements(By.XPATH, '//*[contains(@class,"beautyslide")]')
        report['testimonials'] = len(testimonials)

        testimonials_sliders = driver.find_elements(By.XPATH, '//*[contains(@class,"w-slider-dot")]')
        report['testimonials'] = len(testimonials_sliders)

        images_cont = driver.find_element(By.XPATH, '//*[@class="image_grid"]')
        report['images_cont'] = "success"

        driver.set_window_size(480, 1080)
        menu_button = driver.find_element(By.XPATH, '//*[@id="menu_btn"]')
        menu_button.click()
        time.sleep(2)



        

        time.sleep(3)
        all_images = driver.find_elements(By.XPATH, '//*[contains(@class,"grid_images")]')
        image_load = False
        for i in all_images:
            cls = i.get_attribute("class")
            if 'loaded' in cls:
                image_load = True
                continue
            else:
                image_load = False
                break

        if(image_load): report['images'] = "image loaded"        
        else: report['images'] = "image not loaded"

        script_tags = driver.find_elements(By.TAG_NAME, 'script')
        script_src = False
        for i in script_tags:
            src = i.get_attribute("src")
            if "chrone.ai" in src or "localhost" in src:
                script_src = False
                break
            else:
                script_src = True

        if(script_src): report['script_src'] = "success"
        else: report['script_src'] = "failed"

        

    except Exception as e:
        report['Exception'] = str(e) 
        services_cont = driver.find_element(By.XPATH, '//*[@id="services"]')
        action.move_to_element(services_cont).perform()
        report['services_cont'] = "success"
        time.sleep(3)
        all_images = driver.find_elements(By.XPATH, '//*[contains(@class,"grid_images")]')
        for i in all_images:
            cls = i.get_attribute("class")
            image_load = False
            for i in all_images:
                cls = i.get_attribute("class")
                if 'loaded' in cls:
                    image_load = True
                    continue
                else:
                    image_load = False
                break
    time.sleep(1)

    report_df = pd.DataFrame(list(report.items()),columns = ['test','result']) 
    report_df.to_csv("report.csv",index=False)
    driver.close()
