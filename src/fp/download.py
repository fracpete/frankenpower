import argparse
import logging
import traceback
from datetime import datetime, timedelta
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# logging setup
logger = logging.getLogger("fp.download")


CONSUMPTION = "https://myaccount.frankenergy.co.nz/account/products/consumption"


def download(user: str, password: str, from_date: str, to_date: str, output_dir: str = None):
    """
    Downloads the

    :param user:
    :param password:
    :param from_date:
    :param to_date:
    :param output_dir:
    :return:
    """

    # parse dates
    logger.info("Parsing from date: %s" % from_date)
    _from_date = datetime.strptime(from_date, '%Y-%m-%d')
    logger.info("Parsing to date: %s" % to_date)
    _to_date = datetime.strptime(to_date, '%Y-%m-%d')
    if _from_date > _to_date:
        raise Exception("From date must be smaller than to date: from=%s, to=%s" % (from_date, to_date))
    delta_dates = _to_date - _from_date

    # init selenium
    logger.info("Initialize driver")
    options = None
    if output_dir is not None:
        logger.debug("Using output dir: %s" % output_dir)
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", output_dir)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(30)

    ############
    # 1. login #
    ############
    # open page
    logger.info("Accessing page: %s" % CONSUMPTION)
    driver.get(CONSUMPTION)

    # enter email
    logger.info("Enter email: %s" % user)
    input_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'email')))
    input_element.send_keys(user)

    # continue
    logger.info("Click continue")
    input_element = driver.find_element("id", "continue")
    input_element.send_keys(Keys.ENTER)

    # enter password
    logger.info("Enter password")
    input_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password')))
    input_element.send_keys(password)

    # next
    logger.info("Click next")
    input_element = driver.find_element("id", "next")
    input_element.send_keys(Keys.ENTER)

    ############
    # 2. usage #
    ############

    # wait for page to load
    logger.info("Wait for usage page to load")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'account-switcher-button-name')))

    # wait for loader to finish
    logger.debug("Wait for loader to finish")
    loader = driver.find_element(By.CLASS_NAME, 'show-loader')
    WebDriverWait(driver, 30).until(EC.invisibility_of_element(loader))

    # switch to hourly
    logger.info("Switch to hourly")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'electricity-historical-tabs')))
    hourly_button = driver.find_element(By.XPATH, '//button[text()="Hourly"]')
    hourly_button.click()

    for i in range(delta_dates.days + 1):
        curr_date = _from_date + timedelta(days=i)
        curr_date_str = curr_date.strftime("HOURLY_%Y_%m_%d")

        # open date dropdown
        logger.info("Open date dropdown list")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-dropdown-with-button")))
        date_dropdown_div = driver.find_element(by=By.CLASS_NAME, value="card-dropdown-with-button")
        date_dropdown_button = date_dropdown_div.find_element(by=By.CLASS_NAME, value="toggle")
        date_dropdown_button.click()

        # select date
        logger.info("Select date: %s" % curr_date.strftime("%Y-%m-%d"))
        date_dropdown_button = date_dropdown_div.find_element(By.ID, curr_date_str)
        date_dropdown_button.click()

        # wait for data to be plotted
        logger.info("Waiting for data plot")
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "amcharts-main-div")))
            sleep(2.0)  # TODO better wait?

            # download CSV
            logger.info("Download as CSV")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "download-usage-excel")))
            button_download = driver.find_element(by=By.CLASS_NAME, value="download-usage-excel")
            button_download.click()
        except:
            # error?
            error_divs = driver.find_elements(by=By.CLASS_NAME, value="error-text")
            if len(error_divs) > 0:
                logger.error("Error encountered: %s" % error_divs[0].text)

    driver.close()


def main(args=None):
    """
    Runs the .nfo generation.
    Use -h/--help to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Downloads enervy consumption data as CSV files.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="fp-download")
    parser.add_argument("-u", "--user", required=True, help="The Frank Energy user to use, typically an email address.")
    parser.add_argument("-p", "--password", required=True, help="The password of the Frank Energy user.")
    parser.add_argument("-o", "--output_dir", required=False, help="The directory to download the CSV files to.")
    parser.add_argument("-f", "--from_date", required=True, help="The start date (format: YYYY-MM-DD).")
    parser.add_argument("-t", "--to_date", required=True, help="The end date (format: YYYY-MM-DD).")
    parser.add_argument("--verbose", action="store_true", dest="verbose", required=False, help="whether to output logging information")
    parser.add_argument("--debug", action="store_true", dest="debug", required=False, help="whether to output debugging information")
    parsed = parser.parse_args(args=args)
    # configure loggin
    if parsed.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed.verbose:
        logging.basicConfig(level=logging.INFO)
    logger.debug(parsed)
    download(parsed.user, parsed.password, parsed.from_date, parsed.to_date, output_dir=parsed.output_dir)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        logger.info(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
