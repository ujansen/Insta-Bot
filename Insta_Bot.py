from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep

class InstaBot:
    
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('https://instagram.com')
        sleep(4)
        
    def login(self, username, password):
        self.driver.find_element_by_xpath("//input[@name = \"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name = \"password\"]")\
            .send_keys(password)
        self.driver.find_element_by_xpath("//button[@type = \"submit\"]")\
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        
    # Goes to the homepage
    def homepage(self):
        sleep(1)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img')\
            .click()
            
    # Searches for an account and opens their account
    def search(self, username):
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/input')\
            .send_keys(username)
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]')\
            .click()
        sleep(1)
        
    # Searches for an account and follows them
    def search_follow(self, username):
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/input')\
            .send_keys(username)
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]')\
            .click()
        sleep(1)
        if username not in self.follower_list:
            try:
                element = self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]")
                element.click()
            except:
                print('Already following')
        else:
            try:
                element = self.driver.find_element_by_xpath("//button[contains(text(), 'Follow Back')]")
                element.click()
            except:
                print('Already following')
        
    # Searches for an account and unfollows them
    def search_unfollow(self, username):
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/input')\
            .send_keys(username)
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]')\
            .click()
        sleep(1)
        try:
            self.driver.find_element_by_xpath('//span[@class = "glyphsSpriteFriend_Follow u-__7"]')\
                .click()
            sleep(2)
            self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")\
                .click()
        except:
            print('You are not following this person')
     
    # Gets a list of followers
    def followers(self, username):
        ib.homepage()
        sleep(4)
        self.driver.find_element_by_xpath('//a[contains(@href, "/{}")]'.format(username))\
            .click()
        sleep(4)
        
        buttons = self.driver.find_elements_by_xpath('//a[@class="-nal3 "]')
                
        self.follower_button = [button for button in buttons if 'follower' in button.get_attribute('href')]
        self.follower_button[0].click()
        follower_number = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span")\
            .text
        sleep(2)
        follower_window = self.driver.find_element_by_xpath('//div[@role="dialog"]//a')
        counter = 0
            # Scrolls through window
        sleep(2)
        try:
            while counter < int(follower_number) / 3: 
                follower_window.send_keys(Keys.END)
                counter += 1
                sleep(2)
        except:
            pass
        self.follower_list = self.driver.find_elements_by_xpath('//a[@class = "FPmhX notranslate  _0imsa "]')
        self.follower_list = [account.get_attribute('title') for account in self.follower_list]
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        print(self.follower_list)
    

    # Gets a list of following    
    def following(self, username):
        sleep(2)
        buttons = self.driver.find_elements_by_xpath('//a[@class="-nal3 "]')
        
        self.following_button = [button for button in buttons if 'following' in button.get_attribute('href')]
        self.following_button[0].click()
        following_number = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span")\
            .text
        sleep(2)
        following_window = self.driver.find_element_by_xpath('//div[@class="PZuss"]//a')
        counter = 0
        # Scrolls through window
        try:
            while counter < int(following_number) / 3: 
                following_window.send_keys(Keys.END)
                counter += 1
                sleep(2)
        except:
            pass
        self.following_list = self.driver.find_elements_by_xpath('//a[@class = "FPmhX notranslate  _0imsa "]')
        self.following_list = [account.get_attribute('title') for account in self.following_list]
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()

    # Prints a list of people you follow but don't follow back    
    def find_unfollowers(self, username):
        sleep(2)
        ib.followers(username)
        ib.following(username)
        self.follower_list = set(self.follower_list)
        self.following_list = set(self.following_list)
        self.unfollower_list = self.following_list- self.follower_list
        print(self.unfollower_list)
     
        
    # Sends a message to any account
    def send_message(self, username, message):
        sleep(2)
        if username in self.following_list:
            
            self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/input')\
                .send_keys(username)
            sleep(2)
            self.driver.find_element_by_xpath('//*[@id = "react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]')\
                .click()
            sleep(1)
            # Clicks the message button when their account is opened
            self.driver.find_element_by_xpath('//button[@class = "fAR91 sqdOP  L3NKy _4pI4F   _8A5w5    "]').click()
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')\
                .send_keys(message)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')\
                .click()
        else:
            # Opens DM
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/a')\
                .click()
            sleep(2)
            # Opens compose new message option
            self.driver.find_element_by_xpath('//button[@class = "wpO6b ZQScA"]').click()
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input')\
                .send_keys(username) 
            sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div')\
                .click()
            self.driver.find_element_by_xpath('//button[@class = "sqdOP yWX7d    y3zKF   cB_4K  "]').click()
            sleep(2)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')\
                .send_keys(message)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')\
                .click()
      
    
    # Checks unseen stories
    def check_stories(self):
        sleep(1)
        # Story with circle around it
        element = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/\
                                                    div[1]/div[1]/div/div/div/div/ul/li[3]/div/\
                                                    button/div[1]/canvas')
                                        
        
        # If story is unseen, the circle around it makes its width 66 and if not, it's 64
        if element.size['width'] == 66:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/\
                                                  div[1]/div[1]/div/div/div/div/ul/li[3]/\
                                                      div/button/div[1]').click()
            sleep(4)
            while True:
                try:
                    # Skips through each story until no more unseen stories are left
                    sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div/section/div[2]/button[2]/div')\
                            .click()
                except:
                    break
    
    def logout(self, username):
        self.driver.find_element_by_xpath('//a[contains(@href, "/{}")]'.format(username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath('//button[@class="wpO6b "]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//button[contains(text(), "Log Out")]').click()
        sleep(1)
        self.driver.find_element_by_xpath('//button[contains(text(), "Log Out")]').click()
                                     
ib = InstaBot()
ib.login('udtrialbot', 'Insta@123')
ib.check_stories()
ib.find_unfollowers('udtrialbot')
#ib.search_follow('barelyexists')
#ib.find_unfollowers('udtrialbot')
ib.homepage()
ib.logout('udtrialbot')
#ib.send_message('neymarjr', 'Hello, from the other side?')

