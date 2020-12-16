from selenium import webdriver
from PIL import Image
import os
from io import BytesIO
import requests
import json
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
d = os.path.dirname(os.path.abspath(__file__))

driver = webdriver.Chrome()
driver.get("http://dkhp.ntt.edu.vn/Account/Login")
elementUsername = driver.find_element_by_id("UserName")
elementPassword = driver.find_element_by_id("Password")
elementCaptcha = driver.find_element_by_id("Captcha")
elementIMGCaptcha = driver.find_element_by_id("newcaptcha")

elementUsername.send_keys(username)
elementPassword.send_keys(password)

location = elementIMGCaptcha.location
size = elementIMGCaptcha.size
png = driver.get_screenshot_as_png() # saves screenshot of entire page
im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']
im = im.crop((left, top, right, bottom)) # defines crop points
im.save('screenshot.png') # saves new cropped image
kq_ocr = OCR(d+'\\screenshot.png')
elementCaptcha.send_keys(kq_ocr)