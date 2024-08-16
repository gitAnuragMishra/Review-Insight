import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import yaml

with open('proxylist.yaml', 'r') as file:
    config_proxy = yaml.safe_load(file)




proxies={
    "http": config_proxy['http'],
    "https": config_proxy['https']
}       
    
 



pg = 1
productUrl = 'https://www.amazon.in/HP-15-6inch-Micro-Edge-Anti-Glare-15s-Eq2143au/dp/B09R1MMMTH/'
reviewUrl = productUrl.replace('dp', 'product-reviews') + f'?pageNumber={pg}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
def extractReviews(reviewUrl, pg):
    resp = requests.get(reviewUrl, headers=headers, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.findAll('div', {'data-hook': 'review-body'})
    return reviews

def main():
    reviews = extractReviews(reviewUrl, pg)
    print(reviews)

if __name__ == '__main__':
    main()


#For the time being, we shall work with the html file