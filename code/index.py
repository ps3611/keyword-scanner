from urllib.request import urlopen, Request
import pandas as pd
from bs4 import BeautifulSoup
import os
import datetime
import ssl
print('Starting keyword scraper script...')

urls_df = pd.read_excel('../input/input_websites.xlsx')
keywords_df = pd.read_excel('../input/model.xlsx')
output_df = {'website':[],'score':[],'key_words':[]}

n_urls = len(urls_df['urls'])
# n_urls = 5

for url in urls_df['urls'][0:n_urls]:
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        openedUrl = urlopen(req)
        soup = BeautifulSoup(openedUrl, 'html.parser')
        soup = soup.encode('ascii').decode("ISO-8859-1")

        key_words = []
        score = 0
        for i in range(keywords_df.shape[0]):
            word = keywords_df.iloc[i]['key_words']
            weight = keywords_df.iloc[i]['weight']
            if word in soup:
                key_words.append(word)
                score += weight

        output_df['website'].append(url)
        output_df['score'].append(score)
        output_df['key_words'].append(key_words)
        print(url + ' ===> ' + str(score))

    except:
        print('----',url,'failed... going onto the next url!')

output_df = pd.DataFrame(output_df).sort_values(by='score',ascending=False)
output_df = output_df[['website','score','key_words']]
output_path = '../output/output_'+str(datetime.datetime.now())+'.csv'
output_df.to_csv(output_path, sep=',')
print('Output saved as... ' + output_path + ' in output/ folder!')
