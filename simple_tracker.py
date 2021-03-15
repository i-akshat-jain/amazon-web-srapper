from amazon_config import (
    get_web_driver_options,
    get_chrome_with_web,
    set_browser_as_incognito,
    set_ignore_certificate_error,
    NAME, CURRENCY, FILTERS, BASE_URL,
    DIRECTORY
    )

from selenium.webdriver.common.keys import Keys
import time

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, search_term, filters, base_url,currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_with_web(options)
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"


    def run(self):
        print("Start Scripting")
        print("Looking for {self.search_term} products...")
        link = self.get_product_links()
        time.sleep(2)
        if not link:
            print("Stopped Scripting")
            return
        print(f'Got {len(links)} links to products...')
        print("Getting info about the products")
        products = self.get_product_links(links)
        print(f"Got info about {len(products)} products...")
        self.driver.quit()
        return products


    def get_product_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)

    def get_single_product_info(self, asin):
        print("Product ID: {asin} - getting data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get the title of the product - {self.driver.current_url}")
            return none

    def get_seller(self):
        try:
            return self.driver.find_element_by_id('merchant-info').text
        except Exception as e:
            print(e)
            print(f"Can't get the seller of the product - {self.driver.current_url}")
            return none

    def get_price(self):
        return '$20000 '




    def shorten_url(self, asin):
        return self.base_url + '/dp' + asin


    def get_asins(self, links):
        return [self.get_asin(links) for link in lisks]

    def get_asin(self, product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]





    def get_product_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_id("twotabsearchtextbox")
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)
        result_list = self.driver.find_element_by_class_name('s-result-list')

        links= []
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return links


if __name__ == '__main__':
    print("hello")
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    print(amazon.price_filter)
    amazon.run()