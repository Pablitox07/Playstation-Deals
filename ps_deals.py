from bs4 import BeautifulSoup
import requests
import pandas

def get_deals():
    link_disc = "https://store.playstation.com/en-us/category/43d66fe8-36d7-4c2a-8071-a6b85e034df1/"
    req_to_all = requests.get(link_disc)

    page_all_disc = BeautifulSoup(req_to_all.text, 'html.parser')

    num_disc = page_all_disc.find_all(name="span", class_ = "psw-fill-x")

    number_of_pages = int(num_disc[29].getText())

    Discounts = {
        "Names": [],
        "Prices": []
    }

    for x in range(1, number_of_pages+1):
        new_link = f"{link_disc}{str(x)}"

        link_for_pages = requests.get(new_link)
        page_all_disc = BeautifulSoup(link_for_pages.text, 'html.parser')

        prices = page_all_disc.find_all(name="span", class_="psw-m-r-3")
        names = page_all_disc.find_all(name="span", class_="psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2")

        names_temp = [x.getText().encode('ascii', 'ignore')  for x in names]
        prices_temp = [x.getText() for x in prices[0:len(names_temp)]]

        Discounts["Names"].extend(names_temp)
        Discounts["Prices"].extend(prices_temp)

    print(Discounts)
    df = pandas.DataFrame(Discounts)

    df.to_json("ps_deals.json")


get_deals()
