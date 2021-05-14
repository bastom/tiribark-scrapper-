import json
from pathlib import Path
import requests as requests
from selenium import webdriver
import time

f = open('./man.json', 'r')
json_data = json.loads(f.readlines()[0])

driver = webdriver.Chrome("./chromedriver")

for j in range(len(json_data)):
    # create a folder for the shoe
    Path('./'+json_data[j]['id']).mkdir(parents=True, exist_ok=True)
    link = json_data[j]['link']
    driver.get(link)
    if j == 0:
        driver.execute_script("document.querySelectorAll('[data-var=acceptBtn]')[0].click();")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(3)

    elem = driver.find_element_by_id("pdp-6-up")
    buttons = driver.find_elements_by_xpath('//button[@data-sub-type="image"]')

    for i in range(len(buttons)):
        pictureTag = buttons[i].find_element_by_tag_name('div').find_elements_by_tag_name('picture')[1]
        image_url = pictureTag.find_elements_by_tag_name('img')[0].get_attribute("src")
        if image_url is not None:
            r = requests.get(image_url)

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True

                # Open a local file with write binary permission.
                with open('./'+json_data[j]['id']+'/'+json_data[1]['id'] + '-' + str(i) + '.png', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                print('Image Couldn\'t be retreived')

driver.close()
if __name__ == "__main__":
    print('tartour')
