#!/usr/bin/env python
# coding: utf-8

# In[19]:
#pip install splinter
from splinter import Browser
from bs4 import BeautifulSoup
browser = Browser('chrome')
import requests
import pandas as pd
#from selenium import webdriver
import tweepy
import json
import time
import config
# In[25]:

# URL of page to be scraped
url = "http://mars.nasa.gov/news/"
url

# In[28]:
def scrape():
#Scraping for All Data
# ### NASA Mars News
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    html_news = browser.html
    soup_news = BeautifulSoup(html_news, 'html.parser')

    News_header = (soup_news.find('div', class_='content_title')).string
    News_article = (soup_news.find('div', class_='article_teaser_body')).string

    # ### JPL Mars Space Images - Featured Image

    url_feat = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_feat)
    browser.find_by_css('a.button').click()
    time.sleep(10)
    soup = BeautifulSoup(browser.html,'html.parser')
    end = soup.find('img',class_='fancybox-image')['src']
    JPL_image = "https://www.jpl.nasa.gov"+end

    # ### Mars Weather

    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target = "@MarsWxReport"
    weather = (api.user_timeline(target, count=1, result_type="recent"))[0]["text"]

    # ### Mars Facts

    url_facts = "https://space-facts.com/mars/"
    tables = pd.read_html(url_facts)[0]
    table_build = tables.to_html()

    # ### Mars Hemisphers
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    soup = BeautifulSoup(browser.html, 'html.parser')

    headers=[]
    titles = soup.find_all('h3')
    for title in titles:
        headers.append(title.text)

    images=[]
    count=0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count=count+1

    hemisphere_image_urls = []
    counter = 0
    for item in images:
        hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
        counter = counter+1

    data = {"News_Header":News_header,"News_Article":News_article,"JPL_Image":JPL_image,"Weather":weather,"Facts":table_build,"Hemispheres":hemisphere_image_urls}

    return data
# scrape()
# #response = requests.get(url, verify=false)
# response = requests.get('http://mars.nasa.gov/news/', verify=False)

# # In[29]:

# soup = BeautifulSoup(response.text, 'html.parser')

# # In[30]:


# print(soup.prettify())


# # In[31]:


# # title = soup.find('div', class_="content_title").find('a').text.strip()
# # title

# # pull titles from website
# titles = soup.find_all('div', class_="content_title")
# print(titles)


# # In[32]:


# # pull body from website
# paragraph = soup.find_all('div', class_="rollover_description")
# print(paragraph)


# # In[33]:


# # pull titles and paragraphs 
# results = soup.find_all('div', class_="slide")
# for result in results:
#     titles = result.find('div', class_="content_title")
#     title = titles.find('a').text
#     paragraphs = result.find('div', class_="rollover_description")
#     paragraph = paragraphs.find('div', class_="rollover_description_inner").text
#     print(title)
#     print(paragraph)


# # In[36]:


# url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
# #response = requests.get(url)
# response = requests.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars', verify=False)
# soup = BeautifulSoup(response.text, 'html.parser')


# # In[37]:


# images = soup.find_all('a', class_="fancybox")
# print(images)


# # In[38]:


# picture = []
# for image in images:
#     pic = image['data-fancybox-href']
#     picture.append(pic)
# featured_image_url = 'https://www.jpl.nasa.gov' + pic
# featured_image_url


# # In[40]:


# url = ('https://twitter.com/marswxreport?lang=en')
# response = requests.get('https://twitter.com/marswxreport?lang=en', verify=False)
# #response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')


# # In[41]:


# print(soup.prettify())


# # In[49]:


# # Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) 
# # and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather 
# # report as a variable called `mars_weather`.
# #content = soup.find_all("div",class_="content")
# mars_weather = soup.find("div", class_="js-tweet-text-container")
# print(mars_weather.text)


# # In[50]:


# # * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and 
# # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# # * Use Pandas to convert the data to a HTML table string.
# mars_facts = "https://space-facts.com/mars/"
# table = pd.read_html(mars_facts)
# table

# # In[51]:

# df = table[0]
# df.columns = ["Facts", "Value"]
# df.set_index(["Facts"])
# df

# # In[52]:

# mars_html = df.to_html()
# mars_html = mars_html.replace("\n","")
# mars_html

# # In[54]:

# df.to_html('mars_table.html')

# # In[ ]:
# # Visit the USGS Astrogeology site 
# # [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
# # to obtain high resolution images for each of Mar's hemispheres.
# # * You will need to click each of the links to the hemispheres in order to find the image 
# # url to the full resolution image.
# # * Save both the image url string for the full resolution hemisphere image, and 
# # the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the 
# # data using the keys `img_url` and `title`.
# # * Append the dictionary with the image url string and the hemisphere title to a list. 
# # This list will contain one dictionary for each hemisphere.

# # In[95]:

# browser = Browser('chrome', headless=False)
# usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
# response = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars', verify=False)
# browser.visit(usgs_url)


# # In[96]:


# soup = BeautifulSoup(response.text, 'html.parser')
# hemi_attrib_list = soup.find_all('a', class_="itemLink product-item")


# # In[75]:


# print(len(hemi_attrib_list))
# print(hemi_attrib_list)


# # In[88]:


# headers=[]
# titles = soup.find_all('h3')
# titles


# # In[89]:


# for title in titles:
#     headers.append(title.text)


# # In[90]:


# #title.text


# # In[97]:


# one = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
# two = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
# three = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
# four = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'
# links = [one, two, three, four]


# # In[99]:

# a = soup.find_all('h3')
# a

# # In[100]:


# descriptions = [h3.text.strip() for h3 in a]
# descriptions

# # In[101]:

# hemisphere_image_urls = [{'title': description, 'img_url': link} for description, link in zip(descriptions,links)]
# hemisphere_image_urls

# # In[ ]: