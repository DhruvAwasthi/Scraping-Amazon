import pandas as pd
from urllib import request
from bs4 import BeautifulSoup


num_reviews = 100
reviews_dir = 'data/'
base_url = 'https://www.amazon.in'
product_url = 'https://www.amazon.in/Samsung-EO-BG920BBEGIN-Bluetooth-Headphones-Black-Sapphire/dp/B01A31SHF0/ref=sr_1_1?dchild=1&keywords=headphones+level&qid=1608538861&sr=8-1'


def getPage(url):
    req = request.Request(
        url,
        headers={
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
    )
    return request.urlopen(req)


def getReviewsUrl(product_bsobj):
    try:
        reviews_url = product_bsobj.find('a', {'class': 'a-link-emphasis a-text-bold', 'data-hook': 'see-all-reviews-link-foot'}).attrs.get('href', False)
    except:
        reviews_url = False
    if not reviews_url:
        print('No reviews present for this product')
    return reviews_url


def getKeywords(bsobj):
    try:
        res = list()
        keywords = bsobj.find(id='cr-lighthut-1-').findAll('span', {'class': 'a-declarative'})
        for keyword in keywords:
            res.append(keyword.a.getText().strip())
        return res
    except:
        return list()


def getOverallRating(bsobj):
    try:
        return bsobj.find('div', {'class': 'a-fixed-left-grid AverageCustomerReviews a-spacing-small'}).span.getText()
    except:
        return ''


def getPerStarAnaytics(bsobj):
    try:
        res = list()
        rows = bsobj.find(id='histogramTable').findAll('tr')
        for row in rows:
            res.append(row.span.a.attrs['title'])
        return res
    except:
        return list()


def byFeatureRatings(bsobj):
    try:
        res = list()
        rows = bsobj.find(id='cr-summarization-attributes-list').findAll('div')
        for row in rows:
            if 'id' in row.attrs:
                res.append(row.find('div', {'class': 'a-row'}).span.getText() + ' have ' + row.find('span', {'class': 'a-icon-alt'}).getText() + ' stars')
        return list(set(res))
    except:
        return list()


def getProductIdentifier(bsobj):
    try:
        return bsobj.find(id='productDetails_detailBullets_sections1').td.getText().strip()
    except:
        try:
            for req in bsobj.find(id='detailBullets_feature_div').ul.findAll('li'):
                if req.find('span', {'class': 'a-text-bold'}).getText().lower().split()[0].strip() == 'asin':
                    for count, j in enumerate(req.span.findAll('span')):
                        if count == 1:
                            return j.getText()
        except:
            return ''


def getNumberOfRatings(bsobj):
    try:
        return bsobj.find('div', {'class': 'a-row a-spacing-medium averageStarRatingNumerical'}).span.getText().strip().split()[0]
    except:
        return ''


def addRatingsAndReviewsNumber(bsobj):
    numRatings = getNumberOfRatings(bsobj)
    numReviews = len(reviews_df['Review'])
    reviews_df.insert(5, 'Number of Ratings', pd.Series(numRatings))
    reviews_df.insert(6, 'Number of Reviews', pd.Series(numReviews))


def getReviews(reviews_bsobj):
    reviews = list()
    reviews_div = reviews_bsobj.find('div', {'id': 'cm_cr-review_list'})
    for i in reviews_div:
        if i.attrs.get('class') == ['a-section', 'review', 'aok-relative']:
            try:
                review_stars = int(i.find('a', {'class': 'a-link-normal'}).attrs.get('title', 0).split('.')[0])
            except:
                review_stars = int(i.find('a', {'class': 'a-link-normal'}).attrs.get('title', 0).split('.')[0].split()[0])
            review_date = i.find('span', {'class': 'a-size-base a-color-secondary review-date'}).getText().split('Reviewed in India on ')[-1]
            review_title = i.find('a', {'class': 'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'}).getText().strip()
            review_text = i.find('span', {'class': 'a-size-base review-text review-text-content'}).getText().strip()
            try:
                review_useful = i.find('span', {'class': 'a-size-base a-color-tertiary cr-vote-text'}).getText().split()[0]
            except:
                review_useful = '0'
            row = [review_date, review_stars, review_title, review_useful, review_text]
            reviews.append(row)
    if len(reviews) == 0:
        print('Error while finding reviews in this page')
        return False
    return reviews


def saveReviews(brand, product, reviews_dir):
    getAnalytics(product_bsobj)
    addRatingsAndReviewsNumber(product_bsobj)
    reviews_df.insert(0, 'Brand Name', pd.Series([brand] + [''] * (len(reviews_df) - 1)))
    reviews_df.insert(1, 'Product Name', pd.Series([product] + [''] * (len(reviews_df) - 1)))
    reviews_df.to_excel(brand + ' - ' + product + ' Reviews.xlsx', index=False)
    print(f'Reviews scraping done for product {product}')


def nextReviewPageUrl(brand, product, reviews_dir, reviews_bsobj):
    try:
        for i in reviews_bsobj.find(id='cm_cr-pagination_bar').children:
            try:
                next_review_page_url = i.find('li', {'class': 'a-last'}).a.attrs.get('href')
                review_url = base_url + next_review_page_url
                return review_url
            except:
                print('You are visiting the last page of reviews for this product.')
                saveReviews(brand, product, reviews_dir)
                return False
    except:
        print('Reviews are not present on this page')
        return False


def getAnalytics(product_bsobj):
    overall_rating = getOverallRating(product_bsobj)
    per_star_analytics = getPerStarAnaytics(product_bsobj)
    by_feature_ratings = byFeatureRatings(product_bsobj)
    keywords = getKeywords(product_bsobj)
    product_identifier = getProductIdentifier(product_bsobj)

    reviews_df.insert(0, 'ASIN', pd.Series(product_identifier))  # Amazon Standard Identification Number (ASIN)
    reviews_df.insert(1, 'Overall Rating', pd.Series(overall_rating))
    reviews_df.insert(2, 'Per Star Analytics', pd.Series(per_star_analytics))
    reviews_df.insert(3, 'By Feature Ratings', pd.Series(by_feature_ratings))
    reviews_df.insert(4, 'Keywords', pd.Series(keywords))


def fetchReviews(brand, product, product_url, num_reviews, reviews_dir):
    global reviews_df, product_bsobj
    reviews_df = pd.DataFrame(columns=['Date', 'Stars', 'Title', 'People found this useful', 'Review'])
    product_page = getPage(product_url)
    product_bsobj = BeautifulSoup(product_page)
    reviews_url = getReviewsUrl(product_bsobj)
    if not reviews_url:
        saveReviews(brand, product, reviews_dir)
        return
    reviews_url = base_url + reviews_url
    while reviews_url:
        print(f'Reviews URL is:\n{reviews_url}')
        reviews_page = getPage(reviews_url)
        reviews_bsobj = BeautifulSoup(reviews_page)
        reviews = getReviews(reviews_bsobj)
        if not reviews:
            saveReviews(brand, product, reviews_dir)
            return
        reviews_df = reviews_df.append(pd.DataFrame(reviews, columns=reviews_df.columns), ignore_index=True)
        if len(reviews_df) >= num_reviews:
            saveReviews(brand, product, reviews_dir)
            return
        reviews_url = nextReviewPageUrl(brand, product, reviews_dir, reviews_bsobj)


fetchReviews('Samsung', 'Wireless Headphones', product_url, num_reviews, reviews_dir)
