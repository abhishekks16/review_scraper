from flask import Flask, render_template, request,jsonify, Response, redirect, url_for
import logging
import os
import pandas as pd
import parserfile

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)


@app.route("/")
def parser():
    return render_template('search.html')


@app.route("/reviews_parser" , methods = ['POST'])
def reviews_parser():
    try:
        base_url = request.form['base_url']
        from_page = int(request.form['from_page'])
        to_page = int(request.form['to_page'])
        product_Name = request.form['product_Name']

        base_url =  "https://www.flipkart.com/apple-iphone-14-pro-deep-purple-128-gb/product-reviews/itm75f73f63239fa?pid=MOBGHWFHYGAZRWFT&lid=LSTMOBGHWFHYGAZRWFT3ZMVDX&marketplace=FLIPKART"
        #base_url = "https://www.flipkart.com/samsung-galaxy-f13-waterfall-blue-128-gb/product-reviews/itm032d1a69999cc?pid=MOBGNBFNDPGNJ7HY&lid=LSTMOBGENJWVWYAAVG5AKPCP0&marketplace=FLIPKART"
        urls_with_page_num = [f'{base_url}&page={page}' for page in range(from_page, to_page + 1)]
        logging.info(urls_with_page_num)

        reviews_data = parserfile.scrape_flipkart_reviews(urls_with_page_num)
        
        ## Create the dataframe
        df_flipkart_reivews = pd.DataFrame(reviews_data)

        file_name = parserfile.process_product_name_to_file_name(product_Name)

        # Export the data to CSV
        df_flipkart_reivews.to_csv(f'review_files/{file_name}', index= False)

        #return "Reviews scraping process is successful"
        return redirect(url_for('reviews_result',filename = file_name, page = 1))

    except Exception as ex:
        logging.error(ex)
        return render_template('error.html')
    


@app.route('/reviews_result/<string:filename>/<int:page>')
def reviews_result(filename, page = 1):
    try:
        # Set the chunk size (number of rows per page)
        chunk_size = 10
        logging.info(f'File name to review result is :{filename}')

        # Fetch the desired data chunk based on the page and chunk size.
        data_chunk = parserfile.read_csv_chunk(chunk_size, page, filename)

        return render_template('review_results.html', review_table_rows = data_chunk,filename = filename, page = page)

    except Exception as ex:
        logging.error(ex)
        return render_template('error.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000, debug=True)
