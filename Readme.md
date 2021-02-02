
# Scraping Amazon
## Overview:
- To build intelligent analytic systems, we often need to enhance data collection procedures in order to include information that is relevant for the task. This information can be used for various tasks, and build other end-to-end pipelines on top of it. Given the URL of a product available on amazon.in, it extracts all the reviews & other product information available and stores in an excel file.  

- Below table contains all the columns and their description that are stored in the excel file.  


| S.No.   | Column Name                  | Description                                                                                                      |
| :---    | :---                         | :---                                                                                                             |
| 1.      | Brand Name                   | Name of the brand.                                                                                               |
| 2.      | Product Name                 | Name of the product.                                                                                             |
| 3.      | ASIN                         | Amazon Standard Identification Number (ASIN) is unique block of 10 letters and/or numbers that identify items.   |
| 4.      | Overall Rating               | Overall rating of the product e.g., 3.6 out of 5 stars.                                                          |
| 5.      | Per Star Analytic           | Distribution of total reviews according to number of stars e.g., 47% of reviews have 5 stars.                    |
| 6.      | By Feature Ratings           | Stars given to various features of the product e.g., Bluetooth connectivity have 3.8 stars.                      |
| 7.      | Keywords                     | Keywords describing the product e.g., sound quality.                                                             |
| 8.      | Number of Ratings            | Total number of ratings given to the product e.g., 19060.                                                        |
| 9.      | Number of Reviews            | Total number of reviews extracted and stored in excel file.                                                      |
| 10.     | Date                         | Date when the review was given.                                                                                  |
| 11.     | Stars                        | Number of stars given in a particular review.                                                                    |
| 12.     | Title                        | Title of the review.                                                                                             |
| 13.     | People found this useful     | Number of people who found this review useful.                                                                   |
| 14.     | Review                       | The content of the review.                                                                                       |


## Getting Started:  
**1. Create a new environment:**  
It is always a great idea to create new environment for a new project, so you don't accidentally mess up with other projects that you are working on and requires different version of packages. The steps to create and activate environment using two most popular tools are:  

**- virtualenv**  
```
virtualenv scraping
source scraping/bin/activate
```  
To deactivate type:
```
deactivate
```
**- conda**  
```
conda create -n scraping
conda activate scraping
```
To deactivate type:
```
conda deactivate
```  

**2. Install the packages:**  
To install all the packages required for this project:
```
pip install -r requirements.txt
```  

**3. Scrape the information:**  
There are certain variables that can be used to control/guide the scraping. These are:

- `num_reviews` - Defines the number of reviews to scrape.
- `reviews_dir` - Directory in which generated excel file will be stored.
- `base_url` - URL of amazon.in
- `product_url` - URL of the product for which information needs to be scraped.  

Run the script:
```
python amazon.py
```  
The scraped information is stored in `data/` directory.


## Scenarios taken care of:  
- There may be certain cases in which no reviews or not enough reviews, as described by the variable `num_reviews`, are present. In this case, it scrapes all the product information and whatever number of reviews are present.
- In case, some information from the page is missing, it handles this gracefully and continue to scrape.
- In case, some product review page is not reachable, it exists with saving all the information scraped till then.  

## Future scope:
It can be used to fetch reviews from `amazon.com` with some minute changes.  

## Author:  
- [Dhruv Awasthi](https://www.linkedin.com/in/dhruv-awasthi/)
- [GitHub profile link](https://github.com/DhruvAwasthi)  

## License:  
```
Copyright (c) 2021 Dhruv Awasthi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
