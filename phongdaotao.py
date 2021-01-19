from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import os
from io import BytesIO
import requests
import json
import time

username = ""
password = ""
def OCR(dir):
	url = "https://api.ocr.space/parse/image"
	payload={'apikey': 'd7908af91d88957',
	'language': 'eng'}
	files=[
	  ('file',('a.png',open(dir,'rb'),'image/png'))
	]
	headers = {}

	response = requests.request("POST", url, headers=headers, data=payload, files=files)
	jsondata = json.loads(response.text)
	result = jsondata["ParsedResults"][0]["ParsedText"]
	return result
def captureElement(driver,element,savefile="screenshot.png"):
	location = element.location
	size = element.size
	png = driver.get_screenshot_as_png() # saves screenshot of entire page
	im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
	left = location['x']
	top = location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']
	im = im.crop((left, top, right, bottom)) # defines crop points
	im.save(savefile) # saves new cropped image

d = os.path.dirname(os.path.abspath(__file__))


driver = webdriver.Edge()

driver.get("http://phongdaotao2.ntt.edu.vn/")
elementUsername = driver.find_element_by_id("ctl00_ucRight1_txtMaSV")
elementPassword = driver.find_element_by_id("ctl00_ucRight1_txtMatKhau")
elementCaptcha = driver.find_element_by_id("txtSercurityCode")
elementIMGCaptcha = driver.find_element_by_id("imgSecurityCode")

#giai captcha
captureElement(driver,elementIMGCaptcha)
kq_ocr = OCR(d+'\\screenshot.png')

elementUsername.send_keys(username)
elementPassword.send_keys(password)
elementCaptcha.send_keys(kq_ocr)

driver.get("http://phongdaotao2.ntt.edu.vn/LichHocLichThiTuan.aspx")
#driver.fullscreen_window()

driver.execute_script('(document.evaluate(\'//div[@class="div-ChiTietLich"][1]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).scrollIntoView()')
lichhoc = driver.find_element(By.XPATH, '//div[@class="div-ChiTietLich"][1]')

driver.save_screenshot("lichhoc.png")
#captureElement2(driver,lichhoc,'lichhoc.png')
