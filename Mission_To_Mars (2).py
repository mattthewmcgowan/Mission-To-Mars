#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup 
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 


# In[2]:


# Set the executable path. 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images 

# In[8]:

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# In[15]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]

# we're creating a new DF from the HTML table. The pandas function read_htlm specifically searches for and returns a list of 
# tables found in the HTML. By specifying an index [0], we're telling Pandas to pull only the first table it encounters, or the 
# first item in the list. 

df.columns = ['description', 'Mars', 'Earth']

# Here we assign column to the new DF for additional clarity. 

df.set_index('description', inplace=True)

# we're turning the description column into the DF's index. inplace=true means that the updated index will remain in place,
#without having to reassign the DF to a new variable.

df


# In[16]:


# Convert the DF back into HTML-ready code. 
df.to_html()


# In[17]:


browser.quit()


# In[ ]:




