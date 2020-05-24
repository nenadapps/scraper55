from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import re
from time import sleep
import cfscrape

def get_html(url):
    
    html_content = ''
    try:
        scraper = cfscrape.create_scraper()
        page_content = scraper.get(url).content
        html_content = BeautifulSoup(page_content, "lxml")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        title = html.select('.product_title')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None     
    
    try:
        price = html.select('.woocommerce-Price-amount')[0].get_text().strip()
        price = price.replace('$', '').strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
       
    try:
        raw_text = html.select('#tab-description')[0].get_text().strip()
        raw_text = raw_text.replace(u'\xa0', u' ')
        raw_text = re.sub(' +', ' ', raw_text).strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None 
        
    try:
        category = html.select('.woocommerce-breadcrumb a')[1].get_text().strip()
        stamp['category'] = category
    except:
        stamp['category'] = None        
        
    try:
        subcategory = html.select('.woocommerce-breadcrumb a')[2].get_text().strip()
        stamp['subcategory'] = subcategory
    except:
        stamp['subcategory'] = None   
        
    try:
        number = html.select('.stock')[0].get_text().strip()
        number = number.replace('in stock', '').strip()
        stamp['number'] = number
    except:
        stamp['number'] = None  
        
    try:
        tags = []
        tag_items = html.select('.product_meta a')
        for tag_item in tag_items:
            tag = tag_item.get_text().strip()
            if tag not in tags:
                tags.append(tag)
            
        stamp['tags'] = tags         
        
    except:
        stamp['tags'] = None         
        
    stamp['currency'] = 'AUD'
    
    stamp['category'] = category
    stamp['subcategory'] = subcategory
    
    images = []                    
    try:
        image_items = html.select('.wp-post-image')
        for image_item in image_items:
            img = image_item.get('src')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url 
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url
    
    try:
        for item in html.select('.re_product_price'):
            item_link = item.select('a')[0].get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass

    try:
        next_url_cont = html.select('a.next')[0]
        next_url = next_url_cont.get('href')
    except:
        pass
    
    shuffle(items)
    
    return items, next_url

def get_subcategories(url):
    
    items = []

    try:
        html = get_html(url)
    except:
        return items
    
    try:
        for widget_item in html.select('.s_widget_tittle'):
            widget_text = widget_item.get_text().strip()
            if widget_text == 'Stamp Categories':
                subcat_cont = widget_item.find_next('ul')
                for subcat_item in subcat_cont.select('li a'):
                    item = subcat_item.get('href')
                    if item not in items:
                        items.append(item)
                 
    except:
        pass
    
    shuffle(items)
    
    return items

item_dict = {
"Canada Stamps": "https://www.donsclassicstamps.com/stamp-category/canada-canadian-classic-rare-old-vintage-stamps/",
"British Commonwealth Stamps": "https://www.donsclassicstamps.com/stamp-category/british-commonwealth-stamps/",
"World Stamps": "https://www.donsclassicstamps.com/stamp-category/world/"
    }
    
for key in item_dict:
    print(key + ': ' + item_dict[key])  

selection = input('Choose category: ')

selected_category = item_dict[selection]

subcategories = get_subcategories(selected_category)
for subcategory in subcategories:
    page_url = subcategory
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            stamp = get_details(page_item)     
       
