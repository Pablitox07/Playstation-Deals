from flask import Flask
import requests
from bs4 import BeautifulSoup
result = []

app = Flask(__name__)

@app.route('/get_all_deals')
def get_all_deals():
    url = f"https://store.playstation.com/en-us/category/dc464929-edee-48a5-bcd3-1e6f5250ae80/1"

    # Fetch the webpage content
    response = requests.get(url)

    # Parse the HTML content
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # ol psw-l-space-x-1 psw-l-line-center psw-list-style-none

    all_number_pages = soup.find_all("button", class_="psw-button psw-b-0 psw-page-button psw-p-x-3 psw-r-pill psw-l-line-center psw-l-inline psw-t-size-3 psw-t-align-c")[-1]
    real_number_pages = int(all_number_pages.get("value"))

    for x in range(1, real_number_pages+1):
        print(x)
        url = f"https://store.playstation.com/en-us/category/dc464929-edee-48a5-bcd3-1e6f5250ae80/{x}"
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        all_lis = soup.find_all("li", class_="psw-l-w-1/2@mobile-s psw-l-w-1/2@mobile-l psw-l-w-1/6@tablet-l psw-l-w-1/4@tablet-s psw-l-w-1/6@laptop psw-l-w-1/8@desktop psw-l-w-1/8@max")

        for li in all_lis:
            game_discount = li.find("span", class_="psw-body-2 psw-badge__text psw-badge--none psw-text-bold psw-p-y-0 psw-p-2 psw-r-1 psw-l-anchor")
            if game_discount == None:
                pass
            else:
                game_name = li.find("span", class_="psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2")
                game_link = li.find("a", class_= "psw-link psw-content-link")
                game_pic = li.find("img", class_="psw-top-left psw-l-fit-cover")
                all_game_platforms = li.find_all("span", class_="psw-platform-tag psw-p-x-2 psw-l-line-left psw-t-tag psw-on-graphic")
                list_game_platform = [platform.text for platform in all_game_platforms]


                game_price_with_discount = li.find("span", class_="psw-m-r-3")
                old_game_price = li.find("s", class_="psw-c-t-2")
                result.append({
                    "game_name": game_name.text,
                    "game_url": f"https://store.playstation.com/{game_link.get("href")}",
                    "game_picture_url": game_pic.get("src"),
                    "game_platforms": list_game_platform, 
                    "game_discount_percentage": game_discount.text, 
                    "game_current_price": game_price_with_discount.text,
                    "game_old_price": old_game_price.text


                })
    return result

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")