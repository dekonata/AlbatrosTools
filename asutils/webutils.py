from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv


# Funtion used for to read from csv and identify club ids of clubs to be selected when running create_term_availibilty_report method
def get_club_list(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            club_list = row
    return(club_list)


class AdminWebsite(webdriver.Chrome):
    ''' 
    Class created for simplyfying interaction with admin.handicaps.co.za website.
    Must be intatiated with valid username and password
    option = headless for headless operation
    '''
    def __init__(self, username, password, options=None):
        if options == 'headless':
            opts = Options()
            opts.headless = True
            super().__init__('./chromedriver', options=opts)
        elif options is None:
            super().__init__('./chromedriver')
        self.username = username
        self.password = password

    def login(func):
            def wrap_func(self, *args, **kwargs):  # noqa: E117
                self.get('https://admin.handicaps.co.za/index.php?sid=club')
                assert 'Handicap Server' in self.title
                username_field = self.find_element_by_name('PST_CTRL_login')
                username_field.send_keys(self.username)
                password_field = self.find_element_by_name('PST_CTRL_pwd')
                password_field.send_keys(self.password)
                submit_button = self.find_element_by_name('PST_CTRL_Submit')
                submit_button.click()
                try:
                    login_error = self.find_element_by_class_name('ValidationErrorTitle')
                    return(login_error.text)
                except NoSuchElementException:
                    result = func(self, *args, **kwargs)
                    return result
            return wrap_func

    @login
    def create_term_availibilty_report(self, sdate, edate, club_list):
        '''  # noqa: W291
        Automatically selects all clubs in list for which to generate availability report
        Start date (sdate) and end-date (edate) for report must be provided in 'dd-mm-yyyy' format
        Club list must be in CSV(MS Dos) format with all club id's on single row
        '''
        club_list = get_club_list(club_list)
        self.get('https://admin.handicaps.co.za/index.php?sid=super_admin_reports/csv/terminal_availability')
        start_date = self.find_element_by_id('PST_CTRL_StartDate')
        start_date.clear()
        start_date.send_keys(sdate)
        end_date = self.find_element_by_id('PST_CTRL_EndDate')
        end_date.clear()
        end_date.send_keys(edate)
        add_clubs = self.find_element_by_css_selector('div.gh-button.icon.add.plus')
        add_clubs.click()
        sleep(2)
        clear_all = self.find_element_by_css_selector('div.gh-button.danger.icon.remove.minus')
        clear_all.click()
        for club_id in club_list:
            try:
                club = 'PST_CTRL_Clubs[' + str(club_id) + ']'
                club_box = self.find_element_by_name(club)
                club_box.click()
            except NoSuchElementException as ecp:
                print(ecp)


    @login
    def get_club_playercount(self, clubname):
        ''' Get number of active members as club from admin.handicaps website at time of reporting'''
        self.get('https://admin.handicaps.co.za/index.php?sid=club')
        club_name_filter = self.find_element_by_name('PST_CTRL_FilterName')
        club_name_filter.send_keys(clubname)
        filter_button = self.find_element_by_name('PST_CTRL_Submit')
        filter_button.click()
        player_count = self.find_elements_by_xpath('//table/tbody/tr[2]/td')
        count = player_count[5].text
        full_name = (player_count[19].text).split("(")[0]  # split at ( and return 1st item in  split list to get full name only
        return {'Count':count, 'clubname': full_name}

    @login
    def get_club_terminal_type(self, clubname):
        self.get('https://admin.handicaps.co.za/index.php?sid=club')
        club_name_filter = self.find_element_by_name('PST_CTRL_FilterName')
        club_name_filter.send_keys(clubname)
        filter_button = self.find_element_by_name('PST_CTRL_Submit')
        print(filter_button.text)
        filter_button.click()
        terminal_button = self.find_elements_by_xpath('//table/tbody/tr[2]/td/a')[4]
        terminal_button.click()
        edit_button = self.find_element_by_class_name("edit")
        edit_button.click()
        terminal_type = self.find_element_by_name('PST_CTRL_Type').get_attribute("value")
        return terminal_type


if __name__ == '__main__':
    admindriver = AdminWebsite('Kriegler', 'Ludium99')
    print(admindriver.get_club_terminal_type('Athlone'))
