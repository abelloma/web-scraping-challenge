# Dependencies
import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html

    #parse page
    soup = bs(html, 'html.parser')

    # Extract article title and paragraph text
    results = soup.find('div', class_='list_text')
    news_title = results.find('div', class_='content_title').text
    news_teaser = results.find('div', class_ ='article_teaser_body').text

    #get image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)

    # Go to 'more info'
    browser.click_link_by_partial_text('more info')

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = bs(html, 'html.parser')

    # Scrape the URL
    img_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{img_url}'

    #get tweet
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html = browser.html
    soup = bs(html, 'html.parser')

    # results = soup.find('div', class_='stream')

    mars_tweets = soup.find_all('div', class_='js-tweet-text-container')

    for tweet in mars_tweets:
        mars_weather = tweet.find('p').text 
        if 'sol' and 'pressure' in mars_weather:
            break
        else: 
            pass
    #get data facts
    url4 = "https://space-facts.com/mars/"
    browser.visit(url4)
    html = browser.html

    # Use Pandas to scrape the table to HTML
    dfs = pd.read_html(url4)
    mars_facts = dfs[1]
    mars_facts

    # # Rename columns
    # mars_facts.columns = ['Description','Mars']

    mars_facts.drop(['Earth'], axis=1, inplace=True)
    mars_facts.rename(columns={'Mars - Earth Comparison':'Description', 'Mars':'Value'}, inplace=True)
    mars_facts

    # Reset Index to be description
    mars_facts.set_index('Description', inplace=True)
    # mars_facts.replace('\n', '')
    mars_html = mars_facts.to_html(table_id='scrape_table')
    # (classes="table table-striped")
    
    #get hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    html = browser.html
    soup = bs(html, 'html.parser')


    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

        # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_teaser": news_teaser,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_html,
        "hemisphere_image_urls": hemisphere_image_urls}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()