from selenium.webdriver.common.by import By
from page.BasePage import BasePage


class MainPage(BasePage):

    def run_sql_button(self):
        return self.browser.find_element(By.XPATH, "//button[text()='Run SQL »']")

    def codemirror_div(self):
        return self.browser.find_element(By.XPATH, "//div[contains(@class, 'cm-s-default')]")

    def resultsql_div(self):
        return self.browser.find_element(By.ID, "resultSQL")

    def resultsql_text_div(self):
        return self.browser.find_element(By.XPATH, "//div[@id='resultSQL']//div/div").text

    def assert_table_cell(self, text):
        assert self.browser.find_element(By.XPATH, "//td[contains(text(), '" + text + "')]")

    def assert_sql_table_structure(self, column, header):
        try:
            assert self.browser.find_element(By.XPATH, "//div[@id='divResultSQL']//tbody/tr[1]/th[" + str(column) + "]").text == header
        except AssertionError:
            print("\nSQL table structure ERROR: '" + header + "' is not " + str(column) + "column anymore")
            raise

    def number_of_records(self):
        return self.browser.find_element(By.XPATH, "//*[contains(text(),'Number of Records')]").text.removeprefix('Number of Records:').strip()
