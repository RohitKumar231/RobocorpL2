import time
from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.Assistant import Assistant

browser = Selenium()
http = HTTP()
table = Tables()
pdf = PDF()
archive = Archive()
assistant = Assistant()

@task
def order_robots_from_RobotSpareBin():
    user_input_task()
    orders = get_orders()
    close_annoying_model()
    for each in orders:
        fill_the_form(each)
        time.sleep(1)
        take_screenshot(each['Order number'])
        generate_pdf(each['Order number'])
        merge_img_in_pdf(each['Order number'])
        order_another_robo()
        close_annoying_model()
        archive.archive_folder_with_zip('output/pdfs', 'output/pdf.zip')

def open_robot_order_website(url):
    browser.open_available_browser(url,maximized=True)

def get_orders():
    http.download('https://robotsparebinindustries.com/orders.csv',overwrite=True, target_file='output/order.csv')

    return table.read_table_from_csv('output/order.csv')


def close_annoying_model():
    browser.click_button('OK')


def fill_the_form(each):
    browser.select_from_list_by_index('id:head',each['Head'])
    browser.select_radio_button('body',each['Body'])
    browser.input_text('xpath://*[@class="form-control"]',each['Legs'])
    browser.input_text('id:address',each['Address'])
    browser.click_element_when_clickable('id:order')
    while browser.does_page_contain_element('class:alert-danger'):
        browser.click_element_when_clickable('id:order')


def take_screenshot(odr_num):
    try:
        browser.scroll_element_into_view('class:attribution')
    except:
        pass
    time.sleep(1)
    browser.capture_element_screenshot('robot-preview-image',f'output/screenshots/{odr_num}.png')


    
def order_another_robo():
    browser.click_button('Order another robot')


def generate_pdf(odr_num):
    receipt_html=browser.get_element_attribute('id:receipt','outerHTML')
    pdf.html_to_pdf(receipt_html,f'output/pdfs/{odr_num}.pdf')

def merge_img_in_pdf(odr_num):
    pdf.add_files_to_pdf([f'output/screenshots/{odr_num}.png'],f'output/pdfs/{odr_num}.pdf',append=True)

def user_input_task():
    assistant.add_heading("Input From User")
    assistant.add_text_input("text_input",placeholder="Please Enter URL")
    assistant.add_submit_buttons("Submit",default="Submit")
    result = assistant.run_dialog()
    url = result.text_input
    open_robot_order_website(url)

# URL = 'https://robotsparebinindustries.com/#/robot-order'