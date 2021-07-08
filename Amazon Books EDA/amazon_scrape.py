# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 19:51:53 2021

@author: wenhao
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import numpy as np

# Scrape Amazon for book and sales information
# list out urls to extract top selling books from
urls = []
for year in range(2010,2021):
    urls.append(('https://www.amazon.com/gp/bestsellers/'+str(year)+'/books/ref=zg_bsar_pg_1?ie=UTF8&pg=1', year))

def get_pages_data(url):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    response = requests.get(url,headers = header)
    if response.status_code != 200:
        raise Exception("Unable to download page{}".format(url))
    page_content = response.text
    doc = BeautifulSoup(page_content, "html.parser")
    return doc

# extract information from a single book
def parse_get_information(d):
    
    # check if unavailable
    unavailable = d.find('span', attrs={'class':'a-size-large aok-inline-block zg-item-unavailable zg-text-center-align'})
    if unavailable is not None:
        return {'title':'unavailable',
           'author':'unavailable',
           'rating':0,
           'reviews':0,
           'price':0}
    
    # find title
    name = d.find('span', attrs={'class':'zg-text-center-align'})
    if name is not None:
        title = name.find_all('img', alt = True)
        title = title[0]['alt']
    else:
        title = 'no title'
    print(title)    
   
        
    # find author
    writer = d.find('a', attrs = {'class':'a-size-small a-link-child'}, href = True)
    if writer is None:
        writer = d.find('span', attrs = {'class':'a-size-small a-color-base'})
    if writer is not None:
        author = writer.get_text()
    else:
        author = 'no author'
    print(writer)
    
    # find 5-star ratings
    rate = d.find('span', attrs = {'class':'a-icon-alt'})
    if rate is not None:
        rating = float(rate.text[:3])
    else:
        rating = 0
    print(rating)
        
    # find number of reviews
    review = d.find('a', attrs = {'a-size-small a-link-normal'})
    if review is not None:
        review = int((review.text).replace(',',''))
    else:
        review = 0
    print(review)
    
    # find price
    p = d.find('span', attrs = {'p13n-sc-price'})
    if p is not None:
        price = float((p.text).replace('$',''))
    else:
        price = 0
    print(price)
    
    return{'title':title,
           'author':author,
           'rating':rating,
           'reviews':review,
           'price':price}

# extract information from all books within a single page
def get_item_information(doc):
    tags = doc.findAll('div', attrs = {'class':'a-section a-spacing-none aok-relative'})
    information = [parse_get_information(d) for d in tags]
    return information

# extract information from all books within all the pages specified within urls list
def combine_all_years(urls):
    page_book_info = []
    for i in urls:
        book_info = get_pages_data(i[0])
        book_repo = get_item_information(book_info)
        for j in book_repo:
            j['year'] = i[1]
        page_book_info.append(book_repo)
    all_books = list(itertools.chain.from_iterable(page_book_info))
    return all_books

# execute functions and save the dataframe as csv
df = pd.DataFrame(combine_all_years(urls))
df = df.sort_values('title')
df.to_csv('Amazon_best_sellers_2010_2020.csv', index = False)



# Check Google books API for book genre/category
# list out terms to search for on Google books API
#df = pd.read_csv('Amazon_best_sellers_2010_2020.csv')
df_no_dup = df.drop_duplicates('title').reset_index()
df_no_dup['search_text'] = df_no_dup['title'] + ' ' + df_no_dup['author']
df_no_dup['genre'] = np.empty((len(df_no_dup), 0)).tolist()
booklist = []
for i in range(len(df_no_dup)):
    booklist.append('https://www.googleapis.com/books/v1/volumes?q='+df_no_dup['search_text'][i])
    
# find book genre/category
def get_book_genre(booklist, df_no_dup):
    for i in range(len(booklist)):
        book = booklist[i]
        
        r = requests.get(book)
        rj = r.json()
        for j in rj['items']:
            try:
                print(j['volumeInfo']['authors'][0].lower().replace(' ','').replace('.','').replace("'","").replace(',',''), df_no_dup['author'][i].lower().replace(' ','').replace('.','').replace("'","").replace(',',''))
                if j['volumeInfo']['authors'][0].lower().replace(' ','').replace('.','').replace("'","").replace(',','') == df_no_dup['author'][i].lower().replace(' ','').replace('.','').replace("'","").replace(',',''):
                    if j['volumeInfo']['categories'][0].lower().replace('.','').replace("'","").replace(',','') not in df_no_dup['genre'][i]:
                        df_no_dup['genre'][i].append(j['volumeInfo']['categories'][0].lower().replace('.','').replace("'","").replace(',',''))
                        print(j['volumeInfo']['categories'][0])
            except:
                pass

# execute functions, update original df and save as csv
get_book_genre(booklist, df_no_dup)
df = pd.merge(df,df_no_dup[['title','genre']], how = 'left', on = 'title')
df.to_csv('Amazon_best_sellers_2010_2020_with_genre.csv', index = False)


# get dict containing all the unique genres found    
genre_dict = {}
for i in range(len(df)):
    for j in df['genre'][i]:
        try:
            if genre_dict[j] is not None:
                continue
        except:
            genre_dict[j] = j

# map new columns in df for each genre
for i in genre_dict:
    df[str(i)] = df.genre.map(set([genre_dict[str(i)]]).issubset)

# categorise books with fiction categories as 'fiction
fiction = [col for col in df.columns if 'fiction' in col and 'nonfiction' not in col]
df['fiction flag'] = df[fiction].any(axis = 'columns')

# drop all genre columns other than 'fiction flag'
df = df[['title', 'author', 'rating', 'reviews', 'price', 'year', 'fiction flag']]
df.to_csv('Amazon_best_sellers_2010_2020_fiction_flag.csv', index = False)



