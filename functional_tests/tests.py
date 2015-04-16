from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(LiveServerTestCase):
        
        def setUp(self):
                self.browser = webdriver.Firefox()
                self.browser.implicitly_wait(3)

        def tearDown(self):
                self.browser.quit()

        def test_layout_and_styling(self):
                self.browser.get(self.live_server_url)
                self.browser.set_window_size(1024, 768)

                inputbox = self.browser.find_element_by_id('id_new_item')
                self.assertAlmostEqual(
                        inputbox.location['x'] + inputbox.size['width'] / 2,
                        512,
                        delta=5
                )

                inputbox.send_keys('testing\n')
                inputbox = self.browser.find_element_by_id('id_new_item')
                self.assertAlmostEqual(
                        inputbox.location['x'] + inputbox.size['width'] / 2,
                        512,
                        delta=5
                )
        
        def check_for_row_in_list_table(self, row_text):
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])

        def test_can_start_a_list_and_retrieve_it_later(self):
                # Edith has heard about a cool new online to-do app. She goes
                # to check out its homepage
                self.browser.get(self.live_server_url)

                # She notices the page title and header mention to-do lists
                self.assertIn('To-Do', self.browser.title)
                header_text = self.browser.find_element_by_tag_name('h1').text
                self.assertIn('To-Do', header_text)

                # She is invited to enter a to-do item straight away
                inputbox = self.browser.find_element_by_id('id_new_item')
                self.assertEqual(
                        inputbox.get_attribute('placeholder'),
                        'Enter a to-do item'
                    )

                #She types "Buy peacock feather" into a text box ('Edith's hobby
                # is tying fly fishing lures)
                inputbox.send_keys('Buy peacock feathers')

                # When she hits enter, the page updates, and now the pages lists
                # "1: Buy Peacock Feathers" as an item in a to-do list table
                inputbox.send_keys(Keys.ENTER)
                edith_list_url = self.browser.current_url
                self.assertRegex(edith_list_url, '/lists/.+')
                self.check_for_row_in_list_table('1: Buy peacock feathers')

                inputbox = self.browser.find_element_by_id('id_new_item')
                inputbox.send_keys('Use peacock feathers to make a fly')
                inputbox.send_keys(Keys.ENTER)
                self.check_for_row_in_list_table('1: Buy peacock feathers')
                self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

                ## We use a new browser session to make sure that no information of Edith's is coming through
                self.browser.quit()
                self.browser = webdriver.Firefox()

                #Second user visits home page.
                self.browser.get(self.live_server_url)
                page_text = self.browser.find_element_by_tag_name('body').text
                self.assertNotIn('Buy peacock feathers', page_text)
                self.assertNotIn('make a fly', page_text)

                inputbox = self.browser.find_element_by_id('id_new_item')
                inputbox.send_keys('Buy milk')
                inputbox.send_keys(Keys.ENTER)

                #Francis gets his own unique URL
                francis_list_url = self.browser.current_url
                self.assertRegex(francis_list_url, '/lists/.+')
                self.assertNotEqual(francis_list_url, edith_list_url)

                #No trace of Edith
                page_text = self.browser.find_element_by_tag_name('body').text
                self.assertNotIn('Buy peacock feathers', page_text)
                self.assertIn('Buy milk', page_text)
