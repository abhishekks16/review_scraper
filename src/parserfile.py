import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd

'''
Funtion to scrape the data from the Flipkart reviews page
and store it in the list and return as 
dictionary where key is cloumn name and value is list data
'''
def scrape_flipkart_reviews(urls_with_page_num):
    
    # fake user agent to avoid getting blocked by Google
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    #Iterate through all the review pages of product "apple-iphone-14-pro-deep-purple-128-gb" from Flipkart
    # https://www.flipkart.com/apple-iphone-14-pro-deep-purple-128-gb/p/itm75f73f63239fa?pid=MOBGHWFHYGAZRWFT&fm=organic&ppt=dynamic&ppn=dynamic&ssid=fu1oussq4w0000001690715429461
    review_ratings_list = []
    review_titles_list = []
    review_comments_list = []
    review_users_name_list = []
        
    for each_review_page_url in urls_with_page_num:
        logging.info(each_review_page_url)
        response = requests.get(each_review_page_url, headers = headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        soup_all_div_reviews = soup.find_all("div",{"class":"_1AtVbE col-12-12"}) 
        soup_all_div_reviews = soup_all_div_reviews[4:-1]
        
        # Ratings
        ratings_list_data_soup = soup.find_all('div',{'class':'col _2wzgFH K0kLPL'})
        for rating in ratings_list_data_soup:
            review_user_rating = rating.find('div').select_one(":nth-child(1)")
            review_ratings_list.append(int(review_user_rating.text))
            
        # Review titles
        reviews_titles_soup = soup.find_all('p',{'class':'_2-N8zT'})
        for review_title in reviews_titles_soup:
            review_titles_list.append(review_title.text)
            
        # Review comments
        reviews_comments_soup = soup.find_all('div',{'class':'t-ZTKy'})
        for review_comments in reviews_comments_soup:
            review_user_comments = review_comments.find('div').select_one(":nth-child(1)").text
            review_comments_list.append(review_user_comments)
        
        # Review user name
        review_user_name_soup = soup.find_all('p',{'class':'_2sc7ZR _2V5EHH'})
        for review_user in review_user_name_soup:
            review_users_name_list.append(review_user.text)
            
        logging.info(f'users :{len(review_users_name_list)}, ratings : {len(review_ratings_list)}, titles : {len(review_titles_list)}, reviews : {len(review_comments_list)}')

    return {
        "User name" : review_users_name_list,
        "Ratings" : review_ratings_list,
        "Title" : review_titles_list,
        "Review" : review_comments_list 
    }

'''
Create file name based on the Product name
'''
def process_product_name_to_file_name(product_name):
    # Remove braces and empty spaces, replace with underscores
    processed_file_name = product_name.replace(" ", "_").replace("(", "").replace(")", "")

    # Add "Flipkart_" at the beginning and ".csv" at the end
    processed_file_name = "Flipkart_" + processed_file_name + ".csv"

    logging.info(f'File name is : {processed_file_name}')
    return processed_file_name


'''
    Read the CSV file and return a specific chunk of data 
    based on the page and chunk size.
'''
def read_csv_chunk(chunk_size, page, file_name):

    skip_rows = (page - 1) * chunk_size + 1
    df_chunk = pd.read_csv(f'review_files/{file_name}', skiprows=range(1, skip_rows + 1), nrows=chunk_size)
    return df_chunk
