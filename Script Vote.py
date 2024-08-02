import time, bs4, csv, threading, requests,json,random,string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

MAX_DAILY = 100
url_to_boost = ""
USED_TIMES = 0

def create_instance():
    #prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options = webdriver.ChromeOptions()
    for ele in ["--no-sandbox", '--start-maximized', "--ignore-certificate-errors", "--homepage=about:blank", "--no-first-run"]:
        chrome_options.add_argument(ele)
    #chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path='chromedriver.exe',
                              desired_capabilities=chrome_options.to_capabilities())
    return driver
def page_has_loaded(driver):
    #self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'
def get_email(email=False, check=False):
    'https://api.internal.temp-mail.io/api/v2/email/yh3rt7m9yn@safemail.icu/messages'
    s1 = requests.session()
    s1.verify = False

    headers_get = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://temp-mail.io',
        'pragma': 'no-cache',
        'referer': 'https://temp-mail.io/en',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36',
    }
    if email != False:
        digits = "".join( [random.choice(string.digits) for i in range(3)] )
        chars = "".join( [random.choice(string.ascii_letters) for i in range(8)] )
        s1.verify = False
        url = s1.post('https://api.internal.temp-mail.io/api/v3/email/new',headers=headers_get, json={"name":(chars + " _ " + digits),"domain":"myinbox.icu"})
        new_email = json.loads(url.text)['email']
        return new_email

    if check != False:
        #https://api.internal.temp-mail.io/api/v3/email/z1b9kvaqtc@cloud-mail.top/messages
        url2 = s1.get('https://api.internal.temp-mail.io/api/v3/email/{}/messages'.format(check),headers=headers_get)
        #print(url2.text)
        print(check)
        for ele in json.loads(url2.text):
            if ele['subject'] == 'Activate your Webnovel account':
                soup = bs4.BeautifulSoup(ele['body_html'],'lxml')
                all_links = soup.findAll('a',href=True)
                complete_url = all_links[2]['href']

                '''resp = requests.get(complete_url,headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Upgrade-Insecure-Requests': '1'
                },allow_redirects=True).text
                print(resp)
                soup2 = bs4.BeautifulSoup(resp,'lxml')
                pclass = soup2.find('p',{'class':'m-status'})
                if 'possibly because it has already been used.' in pclass.text.lstrip().rstrip().replace('\\n',''):

                    return False

                else:'''
                return all_links[1]['href']

        #res2 = parser(1,url2.text)
        #if res2 != False:
        #    vote_link = res2
        #    return vote_link
        #else:
        #    return False
def main_ses(url_to_give):
    driver = create_instance()
    try:
        driver.get('https://passport.webnovel.com/register.html')
        email = get_email(email=True)
        driver.find_element_by_xpath('/html/body/div/div/div/div[1]/form/fieldset/p[1]/input').send_keys(email)
        driver.find_element_by_xpath('/html/body/div/div/div/div[1]/form/fieldset/p[2]/input').send_keys(
            'Supermario0010')
        driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(15)
        email2 = get_email(check=email)
        driver.get(email2)
        time.sleep(6)
        page_has_loaded(driver)
        wait = WebDriverWait(driver, 30 * 1000)
        route1 = '/html/body/header/div/div/div/div/a/img'
        wait.until(EC.presence_of_element_located((By.XPATH, route1)))
        driver.get(url_to_give)
        driver.find_element_by_xpath(
            '//*[@id="powerCard"]/div/div[1]/div/div/div/span/button').click()
        time.sleep(5)
        #input('AJAAAAA')
        driver.quit()
        return True
    except:
        driver.quit()
        return False

for i in range(MAX_DAILY):
    try:
        res = main_ses(url_to_boost)
        if res == True:
            USED_TIMES+=1
            print('TOTAL VOTES > {}'.format(str(USED_TIMES)))
        else:
            print('ERR')
    except Exception as e:
        print('ERROR > {}'.format(str(e)))
