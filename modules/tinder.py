import sys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time



class Tinder():

    def set_driver(self, headless, location=None):
        opt=Options()
        if location is not None:
            with open(location, 'r') as f:
                for line in f.readlines():
                    if "lat" in line:
                        lat=line.split('=')[1].strip()
                    if "lng" in line:
                        lng=line.split('=')[1].strip()

            if lat is None or lng is None:
                print('[-] File whit location cordinats not found or not well formatted [-]')
                sys.exit(1)

            opt.set_preference('geo.provider.network.url','data:application/json,{"location": {"lat": %s, "lng": %s }, "accuracy": 100.0}' % lat, lng)
            
        else:
            #modify to not use geolocation for commit (like this is just for me)
            opt.set_preference('geo.provider.network.url','data:application/json,{"location": {"lat": 45.071402109119276, "lng": 7.682555169296413 }, "accuracy": 100.0}')


        opt.headless = headless
        opt.set_preference('geo.prompt.testing', True)
        opt.set_preference('geo.prompt.testing.allow', True)
        driver = Firefox(options=opt, firefox_binary='/usr/bin/firefox-esr',executable_path='/usr/local/bin/geckodriver')
        return driver


    def __init__(self, username, password, headless, location_path=None):
        self.br=self.set_driver(headless, location_path)
        self.username=username
        self.password=password

    def clean_prefs(self):
        self.br.get('about:config')
        accept_btn= self.br.find_element_by_xpath('//*[@id="warningButton"]')
        accept_btn.click()
        sleep(1)
        search_bar = self.br.find_element_by_xpath('//*[@id="about-config-search"]')
        search_bar.send_keys('webdriver')
        one='webdriver_accept_untrusted_certs'
        two='webdriver_assume_untrusted_issuer'
        three='webdriver_enable_native_events'
        mitm = 'security.certerrors.mitm.priming.enabled'
        br1="browser.safebrowsing.blockedURIs.enabled" # -> true
        br2="browser.safebrowsing.downloads.enabled"# -> true
        br3="browser.safebrowsing.enabled"# -> true
        br4="browser.safebrowsing.malware.enabled" #-> true
        br5="browser.safebrowsing.passwords.enabled"# -> true
        br6="browser.safebrowsing.phishing.enabled"# -> true
        br7="browser.search.update" #-> true
        br8="browser.search.update" #-> del 
        br10="app.update.auto"# -> true
        marP="marionette.port" # ->   set default
        update="app.update.disabledForTesting" #  -> del 
        mar="marionette.enabled" # ->   false
        br_true=[br1,br2,br3,br4,br5,br6,br7,br10]
        driver_prefs = [one,two, three]
        search_bar.clear()
        search_bar.send_keys('browser')
        sleep(3)
        ths = self.br.find_elements_by_tag_name('th')
        for pref in ths:
                for trg in br_true:
                    if trg in pref.text:
                        btn = pref.find_element_by_xpath('./../td[2]/button')
                        btn.click()
        search_bar.clear()
        search_bar.send_keys('marionette')
        sleep(3)
        ths = self.br.find_elements_by_tag_name('th')
        print(f'we have found {len(ths)} th elements')
        for pref in ths:
            if mar in pref.text:
                btn = pref.find_element_by_xpath('./../td[2]/button')
                btn.click()
            if marP in pref.text:
                btn = pref.find_element_by_xpath('./../td[3]/button')
                btn.click()
        search_bar.clear()
        search_bar.send_keys('disabledForTesting')
        sleep(3)
        ths = self.br.find_elements_by_tag_name('th')
        print(f'we have found {len(ths)} th elements')
        for pref in ths:
            if update in pref.text:
                btn = pref.find_element_by_xpath('./../td[3]/button')
                btn.click()

        sleep(2)
        ths = self.br.find_elements_by_tag_name('th')
        print(f'we have found {len(ths)} th elements')
        for pref in ths:
            for trg in driver_prefs:
                if trg in pref.text:
                    btn = pref.find_element_by_xpath('./../td[3]/button')
                    btn.click()
        sleep(2)

        search_bar.clear()
        search_bar.send_keys('mitm')
        sleep(3)
        ths = self.br.find_elements_by_tag_name('th')
        print(f'we have found {len(ths)} th elements')
        for pref in ths:
            if mitm in pref.text:
                btn = pref.find_element_by_xpath('./../td[3]/button')
                btn.click()
        sleep(2)


    def login(self):
        try:
            self.br.get('https://tinder.com')
            print(self.br.title)
            time.sleep(15)
            login_btn=self.br.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button")
            login_btn.click()
            time.sleep(3)
            facebook_login=self.br.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[3]/span/div[2]/button/span[2]")
            accept_cookie_btn=self.br.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[1]/button")
            accept_cookie_btn.click()
            wind_core= self.br.window_handles[0]
            facebook_login.click()
            time.sleep(7)
            wind_login= self.br.window_handles[1]
            self.br.switch_to_window(wind_login)
            email_fb=self.br.find_element_by_id("email")
            pass_fb = self.br.find_element_by_id("pass")
            login_fb_btn=self.br.find_element_by_id("loginbutton")    
            email_fb.send_keys(self.username)
            pass_fb.send_keys(self.password)
            time.sleep(3)
            login_fb_btn.click()
            time.sleep(5)
            self.br.switch_to_window(wind_core)
            allow_pos_btn=self.br.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/button[1]/span")
            allow_pos_btn.click()
            time.sleep(20)
            no_notification_btn=self.br.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/button[2]/span")
            no_notification_btn.click()
            time.sleep(5)
        except:
            print("[-] Error on login [-]")
        
        

    def love_all(self):        
        
        like_btn=self.br.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]")
        
        while True:
            

            try:
                like_btn.click()
               # time.sleep(3)
            except:
                pass
    #           print("You have loved all pussyz")
                #break

            try:
                self.br.find_element_by_xpath("/html/body/div[2]/div/div/button[2]").click() 
            except:
                pass 

            try:

                self.br.find_element_by_xpath("/html/body/div[2]/div/div/div/div[3]/button[2]").click() 
                print('[+] SOME PUSSY HAVE LIKED YOU!! GOO BIG, GOO HARD BROTHER!! [+]')
            except:
                pass

            try:
                self.br.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/button[2]").click() 
            except:
                pass




        close_driver()

    def close_driver(self):
        self.br.quit()
