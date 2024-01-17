import os
import json
import time
import hashlib
import validators
from bs4 import BeautifulSoup
from selenium import webdriver
from colorama import Fore, Style
from collections import OrderedDict
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style


class XpathGenerator:
    """This class contains methods that generates xpath file for any given URL"""

    old_xpath_file_path = None
    hash_file_path = "config\\.XpathHash.json"
    tags = ["a", "button", "span", "div", "input", "li", "label"]
    high_priority_tags = ["a", "button"]

    def __init__(self):
        """
        Constructor method create a JSON file, if not already exists, to keep track of all xpath files created.
        This allow the utility to save time by not generating xpath files for same URL again and again.
        """

        if not os.path.exists(XpathGenerator.hash_file_path):
            with open(XpathGenerator.hash_file_path, "w", encoding="utf-8"):
                pass


    @classmethod
    def _blink_output_messages(cls):
        """Blinks statements on terminal for 3 seconds"""

        end_time = time.time() + 3
        message = "..."
        while time.time() < end_time:
            print(message, end="\r")  # \r is used to overwrite the previous line
            time.sleep(0.5)  # Blinking speed is set to 0.5 seconds for now
            print(" " * len(message), end="\r")  # Clears the line
            time.sleep(0.5)


    @classmethod
    def _update_hash_dictionary(cls, hash_dictionary, url_hash):
        """Updates Hash dictionary with Hash of the URL and Xpath file name"""

        cls.new_xpath_file_path = input(
            "Enter the name that you want to give to your xpath file: "
        )
        cls.new_xpath_file_path = (new_xpath_file_path.split(".")[0]) + ".py"
        cls.hash_dictionary[url_hash] = new_xpath_file_path

        # update XpathHash.json file with new file name
        # with open(XpathGenerator.hash_file_path, "w", encoding="utf-8") as hash_file:
        #     json.dump(hash_dictionary, hash_file)

    # Creating a Hash for the given URL using SHA-256 and storing it as a key in dictionary
    # with xpath file name as value
    def _check_xpath_file_exists(self, url):
        """Generates a Hash for the given URL and checks if a xpath file already exists for the given URL"""

        url_hash = hashlib.sha256(url.encode()).hexdigest()
        try:
            with open(
                XpathGenerator.hash_file_path, "r", encoding="utf-8"
            ) as hash_file:
                hash_dictionary = json.load(hash_file)
        except json.decoder.JSONDecodeError:
            hash_dictionary = {}

        if url_hash in hash_dictionary.keys():
            global XpathGenerator.old_xpath_file_path
            XpathGenerator.old_xpath_file_path = hash_dictionary.get(url_hash)

            if os.path.exists(old_xpath_file_path):
                response = input(
                    f"{Fore.ORANGE}Last time you generated a xpath file '{old_xpath_file_path}' for the same URL. Do you want to create a new file? (y/n): {Style.RESET_ALL}"
                ).lower()

                if response not in {"y", "yes"}:
                    print(
                        f"Terminating xpaths file creation as the file {Fore.YELLOW}{old_xpath_file_path}.py{Style.RESET_ALL} already exists",
                        end=" ",
                    )
                    self._blink_output_messages()
                    return False
                else:
                    self.update_hash_dictionary(hash_dictionary, url_hash)
            else:
                print(
                    f"Last time, a xpath file with name {old_xpath_file_path} was generated for the same URL, but the given file has been renamed or deleted from Locator folder."
                )
                self.update_hash_dictionary(hash_dictionary, url_hash)
        else:
            self.update_hash_dictionary(hash_dictionary, url_hash)

        return True

    def open_url(self):
        url = input("Enter the URL to generate xpath file: ")
        if url.endswith("/"):
            url = url[:-1]

        if not validators.url(url):
            raise ValueError(
                f"{Fore.RED} Passed URL is invalid. Include 'http' or 'https' protocol in the url to make it valid{Style.RESET_ALL}"
            )

        html_doc = None

        if self.check_xpath_file_exists(url):
            chrome_driver_path = "drivers\\chromedriver.exe"
            # Use Selenium to load the page with JavaScript execution
            chrome_options = Options()
            # Not running Chrome in Headless mode because some websites need to authenticate
            # user in order to access the application
            # chrome_options.add_argument("--headless")

            # Set the ChromeDriver executable path directly in the constructor
            service = Service(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(url)
            driver.maximize_window()
            WebDriverWait(driver, 3)

            # Waiting for 60 seconds in order to load page completely
            # This step does not guarantee that page will be loaded completely (Limitation of Selenium)
            # If the page has been modified after loading (for example, by Javascript) there is no guarantee that the returned text is that of the modified page
            # From Stackoverflow: Is there any generic function to check if the page has completely loaded through Selenium? The answer is No.
            # Read more on this topic from thread: https://stackoverflow.com/questions/50327132/do-we-have-any-generic-function-to-check-if-page-has-completely-loaded-in-seleni
            WebDriverWait(driver, 60).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )

            html_doc = driver.page_source
            driver.quit()

        return html_doc

    def create_xpaths_from_page_source(html_doc):
        tags = XpathGenerator.tags
        high_priority_tags = XpathGenerator.high_priority_tags
        soup = BeautifulSoup(html_doc, "html.parser")

        # create an empty dictionary to store xpaths
        # This dictionary is made Ordered intentionally so that indexing of the elements having
        # same xpaths can be preversed. But dictionaries are ordered for version > 3.7. Well, we
        # do not know who is going to use this utility, so making sure that dictionary is always ordred
        xpath_dictionary = OrderedDict()

        for tag in tags:
            all_elements = soup.find_all(tag)
            index = 1  # xpath index starts from 1

            for element in all_elements:
                # for link tags and button, create xpaths directly
                if tag in high_priority_tags:
                    xpath = self.select_xpath_attribute(element)
                    node = self.key_name(element, index)
                    xpath_dictionary[node] = xpath
                else:
                    # If any of the other link has a parent as a tag or button tag,
                    # don't create xpaths for them as xpaths for their parent is all that
                    # matters. Do not include them as it will create duplicate elements
                    ancestors = [ancestor.name for ancestor in element.find_parents()]

                    if any(parent in ancestors for parent in high_priority_tags):
                        # do not create xpaths for such elements
                        pass
                    elif not element.find():
                        # create xpaths for only those links which do not have any other child
                        xpath = self.select_xpath_attribute(element)
                        node = self.key_name(element, index)
                        xpath_dictionary[node] = xpath

                index += 1

        return xpath_dictionary

    def select_xpath_attribute(self, element):
        tag = element.name

        if element.get("id"):
            attr_value = element.get("id")
            xpath = f"//{tag}[@id = '{attr_value}']"
        elif element.get("href"):
            attr_value = element.get("href")
            xpath = f"//{tag}[@href = '{attr_value}']"
        elif element.get("src"):
            attr_value = element.get("src")
            xpath = f"//{tag}[@src = '{attr_value}']"
        elif element.get("class"):
            attr_value = " ".join(element.get("class"))
            xpath = f"//{tag}[@class = '{attr_value}']"
        elif element.get("aria-label"):
            attr_value = element.get("aria-label")
            xpath = f"//{tag}[@aria-label = '{attr_value}']"
        elif element.get("title"):
            attr_value = element.get("title")
            xpath = f"//{tag}[@title = '{attr_value}']"
        elif element.string and str(element.string).strip():
            xpath = f"//{tag}[contains(text(), '{str(element.string).strip()}')]"
        elif element.get("name"):
            attr_value = element.get("name")
            xpath = f"//{tag}[(@name = '{attr_value}')]"
        elif element.get("value"):
            attr_value = element.get("value")
            xpath = f"//{tag}[(@value = '{attr_value}')]"
        elif element.get("type"):
            attr_value = element.get("type")
            xpath = f"//{tag}[(@type = '{attr_value}')]"
            xpath = f"//{tag}"
        else:
            xpath = None

        return xpath

    # names can be made more human readable by introducing some chatGPT APIs
    # add in enhancements
    def key_name(self, element, index):
        key = None
        if element.name == "a":
            if element.string and str(element.string).strip():
                key = self.snake_case_convertor(element.string)
            elif element.get("aria-label"):
                key = self.snake_case_convertor(element.get("aria-label"))
            elif element.find_all(string=True):
                children_text = element.find_all(string=True)
                for text in children_text:
                    if text and text != "\n":
                        key = self.snake_case_convertor(text)
                        break
            elif element.find_all(img=True):
                children_text = element.find_all(img=True)
                for text in children_text:
                    if text and text != "\n":
                        key = self.snake_case_convertor(text)
                        break

            if key:
                key += "_link"
            else:
                key = "link_" + str(index)
        else:
            if element.string and str(element.string).strip():
                key = self.snake_case_convertor(element.string)
            elif element.get("aria-label"):
                key = self.snake_case_convertor(element.get("aria-label"))
            elif element.find_all(string=True):
                children_text = element.find_all(string=True)
                for text in children_text:
                    if text and text != "\n":
                        key = self.snake_case_convertor(text)
                        break
            elif element.find_all(img=True):
                children_text = element.find_all(img=True)
                for text in children_text:
                    if text and text != "\n":
                        key = self.snake_case_convertor(text)
                        break

            if key:
                key += "_" + element.name
            else:
                key = element.name + "_" + str(index)

        return key

        # return element.name + "_" + str(index)

    def clean_generated_xpaths(self, xpath_dictionary):
        # There will be multiple web elements with same xpaths. For those web elements,
        # the utility will create xpaths using index

        all_xpaths = [value for value in xpath_dictionary.values() if value is not None]
        # This is the fastest way to remove duplicates from a list
        unique_xpaths = list(OrderedDict.fromkeys(all_xpaths))

        for xpath in unique_xpaths:
            index = 0
            for key, value in xpath_dictionary.items():
                if xpath == value and all_xpaths.count(xpath) > 1:
                    index += 1
                    xpath_dictionary[key] = f"({xpath})[{index}]"

        # Write xpaths in the file
        with open(new_xpath_file_path, "w", encoding="utf-8") as file:
            # Iterate over dictionary items and write them to the file
            for key, value in xpath_dictionary.items():
                file.write(f"{key} = {value}\n")

    def snake_case_convertor(self, raw_string):
        """
        This function converts a string to a valid variable name in snake case format

        This function may result in empty string when a string only contains special symbols
        """

        if not isinstance(raw_string, str):
            raw_string = str(raw_string)

        words = "".join(
            char.lower()
            for char in raw_string.strip()
            if (char.isalnum() or char == "_" or char == " ")
        )

        return words.replace(" ", "_")
