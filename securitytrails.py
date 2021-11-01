# coding:utf-8
'''
@File   :   securitytrails.py
@Time   :   2021/10/29
@Author :   Jarcis-cy
@Link   :   https://github.com/Jarcis-cy
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time

# 搜索
def getUrl():
	urlList = []
	a = browser.find_elements_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[2]/table/tbody/tr/td/a')
	for i in a:
		tmpUrl = i.get_attribute('textContent')
		urlList.append(tmpUrl)
	return urlList

# 传入参数设置
txtName = str(int(time.time())) + ".txt"
parser = argparse.ArgumentParser()
parser.add_argument('--gpu', action="store_false", help='输入该参数将显示chrome，显示爬取过程，默认为False')
parser.add_argument('-s', type=str, help='请输入你想查询的域名')
parser.add_argument('--tp', type=int, default=4000, help='设置最大爬取数量，默认4000，不建议修改')
parser.add_argument('--wp', type=int, default=0, help='设置想要爬取的数量，请输入100的整数，默认全部爬取（不超过最大爬取数量）')
parser.add_argument('-r', type=str, default=txtName, help='请输入你想输出的文件名称，默认为'+txtName)
args = parser.parse_args()

# 初始化设置
chrome_options = Options()
if args.gpu:
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get("https://securitytrails.com/")

# 登录
email = ""
passwd = ""
browser.find_element_by_xpath('//*[@id="login"]').click()
browser.find_element_by_xpath('//*[@id="email"]').send_keys(email)
browser.find_element_by_xpath('//*[@id="password"]').send_keys(passwd)
browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[3]/main/div/div/form/div[4]/button').click()
time.sleep(1) # 保险起见
WebDriverWait(browser,300).until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/section/nav/div/div[2]/div/ul/form/div/input')))
print("登陆成功")

browser.find_element_by_xpath('//*[@id="root"]/div/section/nav/div/div[2]/div/ul/form/div/input').send_keys(args.s)
browser.find_element_by_xpath('//*[@id="root"]/div/section/nav/div/div[2]/div/ul/form/div/button').click()
time.sleep(2)
subdomain_num = browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[1]/ul/li[4]/a/span/span[1]').get_attribute('textContent')
subdomain_num = int(subdomain_num.replace(',', ''))
print("共有"+str(subdomain_num)+"条子域名")
browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[1]/ul/li[4]/a').click()
time.sleep(2)
if args.wp == 0:
	if subdomain_num > args.tp:
		nextPageNum = args.tp / 100
	else:
		nextPageNum = int(subdomain_num / 100)
else:
	nextPageNum = args.wp
urlList = []
print("爬取第1页")
WebDriverWait(browser,300).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[2]/table/tbody/tr[1]')))
urlList.append(getUrl())
if nextPageNum != 0:
	for i in range(nextPageNum):
		browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[1]/ul/li[8]/a[1]').click()
		print("爬取第"+str(i+2)+"页")
		WebDriverWait(browser,300).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[2]/table/tbody/tr[1]')))
		urlList.append(getUrl())
	print("爬取完成")
else:
	print("爬取完成")
browser.quit()
f = open(args.r,"w")
for i in urlList:
	for j in i:
		f.write(j + "\n")
f.close()
print("文件已生成")
