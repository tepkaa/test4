import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from numpy import random
from page import page


class TestWebsite:
    # 1. Check address by name
    # 2. Run 'Selenium Tests' configuration
    # 3. Test report will be created in reports/ directory

    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        self.browser = webdriver.Chrome(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.browser.get("https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all")

        yield

        self.browser.close()
        self.browser.quit()

    def test_address_by_name(self, name='Giovanni Rovelli', address='Via Ludovico il Moro 22'):

        main_page = page.MainPage(self.browser)
        main_page.run_sql_button().click()

        main_page.assert_sql_table_structure(3, 'ContactName')
        main_page.assert_sql_table_structure(4, 'Address')

        locator = self.browser.find_element(By.XPATH,
                                            "//tr/td[3][contains(text(), '" + name + "')]"
                                                                                     "/following-sibling::td[1][contains(text(),'" + address + "')]")
        # td[3] needed to ensure we are at the ContactName column, td[1] to ensure it's an address column
        assert locator is not None

    def test_number_of_city_records(self, city='London', number_of_records=6):
        script = "window.editor.setValue(\"SELECT * FROM Customers where City = \'" + city + "\';\");"
        self.browser.execute_script(script)
        main_page = page.MainPage(self.browser)
        main_page.run_sql_button().click()
        assert main_page.number_of_records() == str(number_of_records)

    def test_insert_record(self, table_name='Customers'):
        main_page = page.MainPage(self.browser)
        postal_code = random.randint(10000000)
        # check if record already exist, if so - delete it
        script = "window.editor.setValue(\"SELECT * FROM Customers WHERE " \
                 "CustomerName = 'Xnbonaaal' and " \
                 "ContactName = 'Call Denny' and " \
                 "Address = 'Raavercrow 21' and " \
                 "City = 'Dandy' and " \
                 "Country = 'Serbia';\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        # time.sleep(2) TODO: investigate lags handle
        try:
            assert main_page.resultsql_text_div() == 'No result.'
        except AssertionError:
            print("WARNING There was record with that parameters")
            script = "window.editor.setValue(\"DELETE FROM Customers WHERE CustomerName='Xnbonaaal';\");"
            self.browser.execute_script(script)
            main_page.run_sql_button().click()
            assert main_page.resultsql_text_div() == "You have made changes to the database"
        # insert
        script = "window.editor.setValue(\"INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country) " \
                 "VALUES ('Xnbonaaal', 'Call Denny', 'Raavercrow 21', 'Dandy', '" + str(
            postal_code) + "', 'Serbia');\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        assert main_page.resultsql_text_div() == "You have made changes to the database. Rows affected: 1"
        # select and assert it in DB
        script = "window.editor.setValue(\"SELECT * FROM Customers WHERE " \
                 "CustomerName = 'Xnbonaaal' and " \
                 "ContactName = 'Call Denny' and " \
                 "Address = 'Raavercrow 21' and " \
                 "City = 'Dandy' and " \
                 "PostalCode = '" + str(postal_code) + "' and " \
                                                       "Country = 'Serbia';\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        assert main_page.number_of_records() == '1'
        main_page.assert_table_cell("Xnbonaaal")
        main_page.assert_table_cell("Call Denny")
        main_page.assert_table_cell("Raavercrow 21")
        main_page.assert_table_cell("Dandy")
        main_page.assert_table_cell(str(postal_code))
        main_page.assert_table_cell("Serbia")
        # delete inserted row
        script = "window.editor.setValue(\"DELETE FROM Customers WHERE CustomerName='Xnbonaaal' and PostalCode=" + str(
            postal_code) + ";\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        assert main_page.resultsql_text_div() == "You have made changes to the database. Rows affected: 1"

    def test_update_record(self):
        # insert
        main_page = page.MainPage(self.browser)
        script = "window.editor.setValue(\"INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country) " \
                 "VALUES ('Dehrw', 'Call Lizzy', 'DW league 3', 'Bamby', '97554', 'Bosnia');\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        # time.sleep(2) TODO: investigate lags handle
        assert main_page.resultsql_text_div() == "You have made changes to the database. Rows affected: 1"
        # update
        main_page = page.MainPage(self.browser)
        script = "window.editor.setValue(\"UPDATE Customers " \
                 "SET CustomerName = 'Dehrw2', ContactName= 'Call Lizzy2', Address='DW league 32', City='Bamby2', PostalCode='975542', Country='Bosnia2' " \
                 "WHERE CustomerName = 'Dehrw' and " \
                 "ContactName = 'Call Lizzy' and " \
                 "Address = 'DW league 3' and " \
                 "City = 'Bamby' and " \
                 "PostalCode = '97554' and " \
                 "Country = 'Bosnia';\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        assert main_page.resultsql_text_div() == "You have made changes to the database. Rows affected: 1"
        # assert
        script = "window.editor.setValue(\"SELECT * FROM Customers WHERE " \
                 "CustomerName = 'Dehrw2' and " \
                 "ContactName = 'Call Lizzy2' and " \
                 "Address = 'DW league 32' and " \
                 "City = 'Bamby2' and " \
                 "PostalCode = '975542' and " \
                 "Country = 'Bosnia2';\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        assert main_page.number_of_records() == '1'
        main_page.assert_table_cell("Dehrw2")
        main_page.assert_table_cell("Call Lizzy2")
        main_page.assert_table_cell("DW league 32")
        main_page.assert_table_cell("Bamby2")
        main_page.assert_table_cell("975542")
        main_page.assert_table_cell("Bosnia2")
        # delete
        script = "window.editor.setValue(\"DELETE FROM Customers WHERE CustomerName='Dehrw2';\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        assert main_page.resultsql_text_div() == "You have made changes to the database. Rows affected: 1"

    def test_delete_record(self):
        # insert
        main_page = page.MainPage(self.browser)
        script = "window.editor.setValue(\"INSERT INTO Customers (CustomerName) VALUES ('Delete');\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        # time.sleep(2) TODO: investigate lags handle
        # delete
        script = "window.editor.setValue(\"DELETE FROM Customers WHERE CustomerName='Delete';\");"
        self.browser.execute_script(script)
        main_page.run_sql_button().click()
        assert main_page.resultsql_text_div() == "You have made changes to the database. Rows affected: 1"

        # TODO: refactor insert/delete/select DB record method
        # TODO: investigate lags and handle waiters
        # TODO: better setup teardown
        # TODO: tags
        # TODO: fully implement Page object pattern, store all actions and data in pages, create test runs
        # TODO: implement settins to store parameters (base url, data sets etc.)
