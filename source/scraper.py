import csv
import time
from logmaster import WriteLogger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException

class MercariScraper(object):
    def __init__(self):
        self.record = WriteLogger()

        try:
            input_path = "../userdir.txt"
            with open(input_path, "r") as f:
                user_dir = f.read().strip()
        except FileNotFoundError as e:
            self.record.logger.critical(e)
            self.record.logger.critical(f"FileNotFoundError occurred, please check the Path in {input_path}")
            raise e

        user_dir = user_dir.replace("\\", "\\\\")
        profile_dir = "Default"
        self.driver_path = "../driver/msedgedriver.exe"

        self.options = webdriver.EdgeOptions()
        self.options.add_argument(f"user-data-dir={user_dir}")
        self.options.add_argument(f"profile-directory={profile_dir}")
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])

    def init_driver(self):
        self.driver = webdriver.Edge(service=Service(executable_path=self.driver_path), options=self.options)
        self.driver.implicitly_wait(15)
        return self.driver

    def get_url(self, url:str):
        self.driver.get(url=url)
        return self.driver

    def quit(self):
        self.driver.quit()

    def get_shipping_dict(self) -> list:
        self.get_url("https://jp.mercari.com/todos")
        self.record.logger.info("--------------------------------------")
        self.record.logger.info("　　　自動で発送する商品を取得します　　　")
        self.record.logger.info("--------------------------------------")
        
        shipping_dict = {}
        count = 1
        
        while True:
            try:
                # 商品情報
                products_detail = self.driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[2]/main/div[2]/div[{count}]/div[2]/a/mer-information-row").text

                # 商品URL
                products_url = self.driver.find_element(By.XPATH, f'//*[@id="main"]/div[2]/div[{count}]/div[2]/a').get_attribute('href')
                
                # 商品情報をkeyに値を辞書形式で格納する
                shipping_dict[products_detail] = products_url
                count += 1
                self.record.logger.info(products_detail)
                time.sleep(2)
            except:
                self.record.logger.info("発送する商品を全て取得しました")
                break
        
        # 発送する商品のみを取得
        for key in list(shipping_dict.keys()):
            if "発送をお願いします" not in key:
                del shipping_dict[key]
        
        self.record.logger.info("商品情報を取得しました")
        
        # 商品URLのみを返す
        shipping_url_list = list(shipping_dict.values())
        return shipping_url_list
    

    def get_buyer_information(self, products_url: str) -> list:
        try:
            self.get_url(products_url)
        except Exception as e:
            self.record.logger.error(f"Failed to get URL: {e}")
            return []

        try:
            # shadow-rootの読み込み
            shadow_host_selector = "#main > div > div.sc-a6b7d8a7-2.hjAQSh > div > div > div.merList.border__17a1e07b > div > div.content__884ec505 > a > mer-item-object"
            shadow_host_element = self.driver.find_element(By.CSS_SELECTOR, shadow_host_selector)
            
            # shadowRoot要素を取得
            shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", shadow_host_element)
        except Exception as e:
            self.record.logger.error(f"Failed to execute shadow_root: {e}")
            return []

        try:
            # 商品タイトルを取得
            title = shadow_root.find_element(By.CSS_SELECTOR, "div").text
        except Exception as e:
            self.record.logger.error(f"Failed to find title element: {e}")
            return []
        
        base_xpath = "/html/body/div/div/div[2]/main/div/div[1]/div/div/div[4]/div/div[2]/span/div"
        elements = self.driver.find_elements(By.XPATH, f"{base_xpath}/p[1]")

        # If elements list is empty, it means that the element was not found.
        if not elements:
            # ゆうゆうメルカリ便の場合、商品名とURL以外を空で返す
            post_address, primary_address, secondary_address, name = "", "", "", ""
            return [title, post_address, primary_address, secondary_address, name, products_url]

        post_address = elements[0].text
        primary_address = self.driver.find_element(By.XPATH, f"{base_xpath}/p[2]").text
        secondary_address = self.driver.find_element(By.XPATH, f"{base_xpath}/p[3]").text

        elements = self.driver.find_elements(By.XPATH, f"{base_xpath}/p[4]")
        if not elements:
            name, secondary_address = secondary_address, ""
        else:
            name = elements[0].text

        return [title, post_address, primary_address, secondary_address, name, products_url]

    def replace_non_shift_jis(self, text: str) -> str:
        return text.encode('shift_jis', 'replace').decode('shift_jis').replace('?', '-')

    def add_to_csv(self, *data_list: str):
        try:
            input_path = "../output.csv"
            with open(input_path, "a", encoding="shift_jis", newline="") as f:
                csv_writer = csv.writer(f)
                replaced_data_list = [self.replace_non_shift_jis(item) for item in data_list]
                csv_writer.writerow(replaced_data_list)
        except FileNotFoundError as e:
            self.record.logger.critical(e)
            self.record.logger.critical(f"FileNotFoundError occurred, please check the Path in {input_path}")
            raise e

    def read_csv_column_f(self, file_path: str) -> list:
        urls = []
        try:
            with open(file_path, "r") as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    urls.append(row[5])
            return urls
        except FileNotFoundError as e:
            self.record.logger.critical(e)
            self.record.logger.critical(f"FileNotFoundError occurred, please check the Path in {file_path}")
            raise e
        
    def process_urls(self, urls: list):
        for url in urls:
            self.get_url(url)
            try:
                self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/form/div").click()
                self.driver.find_element(By.XPATH, "/html/body/mer-dialog/div[2]/div[2]").click()
                self.record.logger.info(f"発送した商品 : {url}")
            except NoSuchElementException:
                self.record.logger.error("Error: NoSuchElementException was encountered. The element could not be found.")
                self.record.logger.error(f"この商品は発送できる状態ではありません : {url}")
            time.sleep(3)