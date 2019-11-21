#!/usr/bin/env python
# coding: utf-8

# In[19]:
#pip install splinter
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
# In[25]:

# URL of page to be scraped
url = "http://mars.nasa.gov/news/"
url

# In[28]:

#response = requests.get(url, verify=false)
response = requests.get('http://mars.nasa.gov/news/', verify=False)

# In[29]:

soup = BeautifulSoup(response.text, 'html.parser')

# In[30]:


print(soup.prettify())


# In[31]:


# title = soup.find('div', class_="content_title").find('a').text.strip()
# title

# pull titles from website
titles = soup.find_all('div', class_="content_title")
print(titles)


# In[32]:


# pull body from website
paragraph = soup.find_all('div', class_="rollover_description")
print(paragraph)


# In[33]:


# pull titles and paragraphs 
results = soup.find_all('div', class_="slide")
for result in results:
    titles = result.find('div', class_="content_title")
    title = titles.find('a').text
    paragraphs = result.find('div', class_="rollover_description")
    paragraph = paragraphs.find('div', class_="rollover_description_inner").text
    print(title)
    print(paragraph)


# In[36]:


url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
#response = requests.get(url)
response = requests.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars', verify=False)
soup = BeautifulSoup(response.text, 'html.parser')


# In[37]:


images = soup.find_all('a', class_="fancybox")
print(images)


# In[38]:


picture = []
for image in images:
    pic = image['data-fancybox-href']
    picture.append(pic)
featured_image_url = 'https://www.jpl.nasa.gov' + pic
featured_image_url


# In[40]:


url = ('https://twitter.com/marswxreport?lang=en')
response = requests.get('https://twitter.com/marswxreport?lang=en', verify=False)
#response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# In[41]:


print(soup.prettify())


# In[49]:


# Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) 
# and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather 
# report as a variable called `mars_weather`.
#content = soup.find_all("div",class_="content")
mars_weather = soup.find("div", class_="js-tweet-text-container")
print(mars_weather.text)


# In[50]:


# * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and 
# use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# * Use Pandas to convert the data to a HTML table string.
mars_facts = "https://space-facts.com/mars/"
table = pd.read_html(mars_facts)
table

# In[51]:

df = table[0]
df.columns = ["Facts", "Value"]
df.set_index(["Facts"])
df

# In[52]:

mars_html = df.to_html()
mars_html = mars_html.replace("\n","")
mars_html

# In[54]:

df.to_html('mars_table.html')

# In[ ]:
# Visit the USGS Astrogeology site 
# [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
# to obtain high resolution images for each of Mar's hemispheres.
# * You will need to click each of the links to the hemispheres in order to find the image 
# url to the full resolution image.
# * Save both the image url string for the full resolution hemisphere image, and 
# the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the 
# data using the keys `img_url` and `title`.
# * Append the dictionary with the image url string and the hemisphere title to a list. 
# This list will contain one dictionary for each hemisphere.

# In[95]:

browser = Browser('chrome', headless=False)
usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
response = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars', verify=False)
browser.visit(usgs_url)


# In[96]:


soup = BeautifulSoup(response.text, 'html.parser')
hemi_attrib_list = soup.find_all('a', class_="itemLink product-item")


# In[75]:


print(len(hemi_attrib_list))
print(hemi_attrib_list)


# In[88]:


headers=[]
titles = soup.find_all('h3')
titles


# In[89]:


for title in titles:
    headers.append(title.text)


# In[90]:


title.text


# In[97]:


one = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
two = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
three = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
four = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'
links = [one, two, three, four]


# In[99]:

a = soup.find_all('h3')
a

# In[100]:


descriptions = [h3.text.strip() for h3 in a]
descriptions

# In[101]:

hemisphere_image_urls = [{'title': description, 'img_url': link} for description, link in zip(descriptions,links)]
hemisphere_image_urls

# In[ ]: