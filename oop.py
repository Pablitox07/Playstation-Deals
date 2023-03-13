from bs4 import BeautifulSoup
import requests
import pandas


class Ps_deals:
    def __init__(self, file):
        self.link_disc = "https://store.playstation.com/en-us/category/43d66fe8-36d7-4c2a-8071-a6b85e034df1/"
        self.req_to_all = requests.get(self.link_disc)
        self.page_all_disc = BeautifulSoup(self.req_to_all.text, 'html.parser')
        self.num_disc = self.page_all_disc.find_all(name="span", class_="psw-fill-x")
        self.number_of_pages = int(self.num_disc[29].getText())
        self.Discounts = {
            "Names": [],
            "Prices": []
        }
        self.file = file

    def get_discounts(self):
        for x in range(1, self.number_of_pages + 1):
            new_link = f"{self.link_disc}{str(x)}"

            link_for_pages = requests.get(new_link)
            page_all_disc = BeautifulSoup(link_for_pages.text, 'html.parser')

            prices = page_all_disc.find_all(name="span", class_="psw-m-r-3")
            names = page_all_disc.find_all(name="span", class_="psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2")

            names_temp = [x.getText() for x in names]
            prices_temp = [x.getText() for x in prices[0:len(names_temp)]]

            self.Discounts["Names"].extend(names_temp)
            self.Discounts["Prices"].extend(prices_temp)

        df = pandas.DataFrame(self.Discounts)

        if self.file.lower() == "json":
            df.to_json("Deals.json")
        elif self.file.lower() == "csv":
            df.to_csv("Deals.csv")

