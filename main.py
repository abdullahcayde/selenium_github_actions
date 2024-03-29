import time
import numpy as np
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Sleep function 
def sleep(x):
    time.sleep(x)


# Wait for a certain measure of time before throwing an exception
def wait(x):
    driver.implicitly_wait(x)


# Click Function
def click_bann_byID(ID):
    actions = ActionChains(driver)
    akzeptieren = driver.find_element(By.ID, ID)
    actions.click(akzeptieren).perform()
    wait(10)
    sleep(0.5)


# Find Element Function
def find_element(E):
    elements = driver.find_elements(By.CLASS_NAME, E)
    list_elements = [element.text for element in elements]
    return list_elements


# Find Elements Function
def find_elements_HPCO(H,P,C,O):
    header = driver.find_elements(By.CLASS_NAME, H)
    publish = driver.find_elements(By.CLASS_NAME, P)
    company = driver.find_elements(By.CLASS_NAME, C)
    ort = driver.find_elements(By.CLASS_NAME, O) 

    list_header = [title.text for title in header]
    list_publish = [pub.text for pub in publish]
    list_company = [comp.text for comp in company]
    list_ort = [o.text for o in ort]
    return list_header, list_publish, list_company, list_ort


def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("gitlogfile.txt","a") as f:
        f.write(timestamp + ',' + message + '\n')



print('---------------------- StepStone Job Searching Selenium Project ----------------------')
start=datetime.now()
log('start_stepstone')
# Link Descriptions
link_original_stepstone = 'https://www.stepstone.de/jobs/data-analyst/in-rietberg?radius=50&page=2'

website_name = 'stepstone'
job_name = 'Data Engineer'
ort_ = 'Rietberg'
radius = 100
page_number = 1


#  1 - Create Driver
chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
print('Create Driver')


#  2 - Go to Website
job_link = job_name.replace(' ', '-').lower()
ort_link = ort_.lower()
link = f'https://www.stepstone.de/jobs/{job_link}/in-{ort_link}?radius={radius}&page={page_number}&sort=2&action=sort_publish'


driver.get(link)
wait(5)
sleep(2)
print('Go to Website')



# 4 -  Take Infos from Page
# 4.1 - Headers, Publish_Time ,Company, City
H, P, C, O = ('res-29pyh9', 'res-rf8k2x', 'res-hbyqhf', 'res-1wf9en7')
list_header, list_publish, list_company, list_ort = find_elements_HPCO(H,P,C,O)


# 4.2 - Description and Page number of results
description = driver.find_elements(By.CLASS_NAME, 'res-17md5or')


# 4.3 - Get Links 'res-1dwe62q'
list_link01  = driver.find_elements(By.CLASS_NAME, 'res-1dwe62q')
list_link = [link.get_attribute('href') for link in list_link01]

# 4.4 - Get Texts for each finding
list_description = [des.text for des in description]
print('Header',len(list_header), 'Publish',len(list_publish), 'Company',len(list_company[1:]), 'Ort',len(list_ort), 'Desc', len(list_description), 'Link',len(list_link))


# 4.6 - DataFrame df
d = dict(job_title=np.array(list_header), publish=np.array(list_publish), company=np.array(list_company[1:]), city=np.array(list_ort) , description=np.array(list_description), link=np.array(list_link))
df01 = pd.DataFrame.from_dict(d, orient='index')
df01 = df01.T


print(f'DataFrame End : {df01.shape}')
df01['website'] = website_name
time_ = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
df01['date'] = time_
df01['search_title'] = job_name


# 5.1 - Quit
end =datetime.now() 
print('Code Runned No Problem')
log('end_stepstone')
print(f'Time = {end - start}')
sleep(0.5)
driver.quit()


# 6.1 Dataframe first 5 Rows
print(df01.head(2))


print('---------------------- Xing Job Searching Selenium Project ----------------------')
start=datetime.now()
log('start_xing')  


# Link Descriptions
link_original_xing = 'https://www.xing.com/jobs/search?keywords=Data%20Engineer&location=Rietberg&page=1&radius=100'
website_name = 'xing'
job_name = 'Data Engineer'
ort_ = 'Rietberg'
radius = 50
page_number = 1


#  1 - Create Driver

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


#  2 - Go to Website
job_link = job_name.replace(' ', '-').lower()
ort_link = ort_.lower()
link = f'https://www.xing.com/jobs/search?keywords=Data%20Engineer&location=Rietberg&page=1&radius=100&sort=date'
driver.get(link)
wait(10)
sleep(1)



# 4 -  Take Infos from Page
# 4.1 - Headers, Publish_Time ,Company, City
H = 'utils-line-clamp-lineClamp2-dfe26aab'
D = 'list-item-job-teaser-list-item-highlight-bb8ddbb6'
L = 'list-item-job-teaser-list-item-location-a5b28738'
ALL = 'list-item-job-teaser-list-item-listItem-f04c772e'


# 4 -  Take Infos from Page
# 4.1 - Headers, Publish_Time ,Company, City
list_header = find_element(H)
list_description = find_element(D)
list_ort = find_element(L)
list_all = find_element(ALL)


list_publish = []
list_full_time = [] 
for i in list_all:
    date = i.split('\n')[-2]
    time_ = i.split('\n')[-3]
    list_publish.append(date)
    list_full_time.append(time_)


list_title =[]
list_company = []
n = 0
while n < len(list_header):
    list_title.append(list_header[n])
    list_company.append(list_header[n+1])
    n += 2


# 4.3 - Get Links
Link = 'list-item-job-teaser-list-item-listItem-f04c772e'
header = driver.find_elements(By.CLASS_NAME, Link)
list_link = [link.get_attribute('href') for link in header]


# 4.4 - DataFrame df
d = dict(job_title=np.array(list_title), publish=np.array(list_publish), company=np.array(list_company), city=np.array(list_ort) , description=np.array(list_description), link=np.array(list_link))
df02 = pd.DataFrame.from_dict(d, orient='index')
df02 = df02.T
df02['website'] = website_name
time_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
df02['date'] = time_now
df02['search_title'] = job_name


list_of_list = [list_header, list_description, list_ort, list_publish, list_link]
print([len(i) for i in list_of_list])


# 5.1 Quit Driver
sleep(1)
driver.quit()
print('Finish', time_now)
log('end_xing')
end =datetime.now() 
print(f'Time = {end - start}')


# 6.1 Dataframe firts 5 Rows
print(df02.head(2))


today_ = datetime.today().strftime('%Y-%m-%d')
df01.to_csv(f'{job_name}_{today_}.csv', header=True)
df02.to_csv(f'{job_name}_{today_}.csv', mode='a', header=False)
