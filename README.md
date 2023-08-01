# Flipkart review scraper
* This is an review scraper app, which scrapes the Flipkart reviews page.
* This app is built using Python and Flask as UI framework.

## Homepage
* After running `python app.py`, the app can be accessbile at `http://127.0.0.1:8000` in local environment.
* The homepage form consists of below fields :
<img width="443" alt="image" src="https://github.com/abhishekks16/review_scraper/assets/133478875/a2c0ae37-946c-4c6e-bae0-b95add110fba">

```
 * "Product Name" : Name of the product. Ex : `APPLE iPhone 14 Pro (Deep Purple, 128 GB) Reviews`      
 * "Flipkart review page Url" : Url of the Flipkart review page. Ex : "https://www.flipkart.com/apple-iphone-14-pro-deep-purple-128-gb/product-reviews/itm75f73f63239fa?pid=MOBGHWFHYGAZRWFT&lid=LSTMOBGHWFHYGAZRWFT3ZMVDX&marketplace=FLIPKART"
 * "From Page" : Start of the review page in Integer.    
 * "To Page" : End of the review page in Integers.
```
**Note : `From Page` should be less than `To page`**
* Once `Submit` is clicked, scrapes the reviews and store it in CSV file . Ex : `Flipkart_APPLE_iPhone_14_Pro_Deep_Purple,_128_GB_Reviews.csv`

## Review results
* After processing the results, it will redirect to `reviews_result` page .
* The parsed reviews are stored in CSV file, here in this page it is diplayed in the table.
* The table is enabled with pagination.
<img width="647" alt="image" src="https://github.com/abhishekks16/review_scraper/assets/133478875/0fe24b50-e8ca-4c77-bd74-6b29c9787bc4">


## Error page
* While sraping or saving data to csv if any error occurs. It will redirects to error page.
* All the logs are logged inside `scarrper.log` file.
<img width="607" alt="image" src="https://github.com/abhishekks16/review_scraper/assets/133478875/28836784-4e2a-44fa-b56f-941618d2d881">
