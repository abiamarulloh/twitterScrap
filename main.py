#import packages
#snscrape
import snscrape.modules.twitter as sntwitter
import csv
import pandas as pd
import datetime

#1 Using TwitterSearchScraper to scrape data and append tweets to list
result = []
currentDate = datetime.datetime.now()

def export_to_csv(data):
    fieldnames = ['user_name', 'content', 'lang', 'url', 'source', 'likeCount', 'retweetCount']
    rows = data

    with open('asset/csv/twitterScrap-' + str(currentDate) + '.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def export_to_excel(data):
    # creating the DataFrame
    user_names = []
    contents = []
    langs = []
    sources = []
    likeCounts = []
    retweetCounts = []
    for i, item in enumerate(data):
        user_names.append(item.get('user_name'))
        contents.append(item.get('content'))
        langs.append(item.get('lang'))
        sources.append(item.get('source'))
        likeCounts.append(item.get('likeCount'))
        retweetCounts.append(item.get('retweetCount'))
    
    twits_data = pd.DataFrame(
                {
                    'user_name': user_names,
                    'content': contents,
                    'lang': langs,
                    'source': sources,
                    'likeCount': likeCounts,
                    'retweetCount': retweetCounts
                })
  
    # writing to Excel
    dataToExcel = pd.ExcelWriter('asset/excel/twitterScrap-' + str(currentDate) + '.xlsx')
    
    # write DataFrame to excel
    twits_data.to_excel(dataToExcel)
    
    # save the excel
    dataToExcel.save()
    print('DataFrame is written to Excel File successfully.')

def get_data(exportType, querySearch, howMuch, since, until):
    if exportType != 'excel' and exportType != 'csv':
        print('=== Export type not support! ====')
        return

    print("Getting data "+ exportType +" from Twitter, please wait... ")
    for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(querySearch + ' since:' + since + ' until:' + until ).get_items()):
        if i >= howMuch: 
            break

        data = {
            "user_name": tweet.user.username,
            "content": tweet.content,
            "lang": tweet.lang,
            "url": tweet.url,
            "source": tweet.source,
            "likeCount": tweet.likeCount,
            'retweetCount': tweet.retweetCount
        }
        result.append(data)

    if exportType == 'csv':
        export_to_csv(result)
    elif exportType == 'excel':
        export_to_excel(result)

def main(exportType, querySearch, howMuch, since, until):
    # Get data From Twitter by search query 
    get_data(exportType, querySearch, howMuch, since, until)
    

# ExportType, QuerySearch, HowMuch, since, until
main('excel', 'sepak bola', 100, '2022-01-01', '2022-12-30')
