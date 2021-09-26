import os
from time import sleep

from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait

# Environment variable in .env file
load_dotenv()
executable_path = os.environ.get('EXECUTABLE_PATH')  # Chromedriver path
given_name = os.environ.get('GIVEN_NAME')
surname = os.environ.get('SURNAME')
birthdate = os.environ.get('BIRTHDATE')  # dd/mm/yyyy
email = os.environ.get('EMAIL')
pp_no = os.environ.get('PASSPORT_NUMBER')

# Random user agent to prevent from being request blocked
options = Options()
user_agent = UserAgent(use_cache_server=False, verify_ssl=False).random
print(user_agent)  # Check
options.add_argument(f'user-agent={user_agent}')
# options.add_argument('user-data-dir=your/chrome/profile/path')  # Go chrome://version and check Profile Path
options.add_argument('disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# Browser setting
driver = webdriver.Chrome(executable_path=executable_path, options=options)
driver.maximize_window()
driver.get('https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm')


def irp_auto():
    actions = ActionChains(driver)
    # Wait for webpage rendering and close cookie window
    # Refresh if getting blocked
    try:
        WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('cookiescript_close').is_enabled())
    except TimeoutException:
        driver.refresh()
        irp_auto()

    # Are you happy to accept cookies?
    driver.find_element_by_id('cookiescript_close').click()

    # Category
    category_select = Select(driver.find_element_by_id('Category'))
    category_select.select_by_value('All')

    # SubCategory
    subcategory_select = Select(driver.find_element_by_id('SubCategory'))
    subcategory_select.select_by_value('All')

    # Declaration
    declaration_checkbox = driver.find_element_by_id('UsrDeclaration')
    declaration_checkbox.click()

    # Salutation
    salutation_select = Select(driver.find_element_by_id('Salutation'))
    salutation_select.select_by_visible_text('Mr')  # Mr, Mrs, Miss, Ms, Dr

    # Given Name
    driver.find_element_by_name('GivenName').send_keys(given_name)

    # Surname
    driver.find_element_by_name('SurName').send_keys(surname)

    # Date of Birth
    dob = driver.find_element_by_name('DOB')
    driver.execute_script("arguments[0].removeAttribute('readonly')", dob)
    dob.send_keys(birthdate)

    # Scroll down to appointment button to display following elements
    appointment_button = driver.find_element_by_id('btLook4App')
    actions.move_to_element(appointment_button).perform()

    # Nationality
    nationality_select = Select(driver.find_element_by_id('Nationality'))
    nationality_select.select_by_index(153)  # Index 153 is Taiwan, check yours by inspecting elements in Console

    # Email
    driver.find_element_by_name('Email').send_keys(email)

    # Confirm Email
    driver.find_element_by_name('EmailConfirm').send_keys(email)

    # Is this a family application?
    fam_app_yn_select = Select(driver.find_element_by_id('FamAppYN'))
    fam_app_yn_select.select_by_visible_text('No')  # Yes, No, only work for `No` 🤡

    # Do you have a Passport or Travel Document?
    pp_no_yn_select = Select(driver.find_element_by_id('PPNoYN'))
    pp_no_yn_select.select_by_visible_text('Yes')  # Yes, No, only work for `Yes` 🤡

    # Passport Number or Travel Document Number (max 30 characters)
    driver.find_element_by_name('PPNo').send_keys(pp_no)

    # Look for Appointment
    appointment_button.click()

    # Scroll down to bottom
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    # Search for appointments by:
    appointment_date_select = Select(driver.find_element_by_id('AppSelectChoice'))
    appointment_date_select.select_by_value('S')  # D -> specific date, S -> closest to today, only work for `S` 🤡

    # Find Available Appointments
    find_appointment_button = driver.find_element_by_id('btSrch4Apps')

    # Click
    count = 0
    while True:
        count += 1
        print(f'Try {count} times')  # Check
        find_appointment_button.click()
        sleep(2)
        try:
            driver.find_element_by_xpath('//button[text()="Book This"]').click()
            # driver.find_element_by_id('Submit').click()   # Will fail due to reCAPTCHA so please
            os.system('say "Please check for I R P appointment"')
            # Use your `normal` browser for submit
            sleep(600)
        except NoSuchElementException:
            # Edge case control
            if not find_appointment_button.is_enabled() or driver.find_elements_by_xpath(
                    "//*[contains(text(), 'Why is this happening to me?')]") \
                    or driver.find_elements_by_xpath("//*[contains(text(), 'Please try reloading this page.')]"):
                driver.refresh()
                irp_auto()
            # No appointment(s) are currently available
            else:
                sleep(8)


irp_auto()
