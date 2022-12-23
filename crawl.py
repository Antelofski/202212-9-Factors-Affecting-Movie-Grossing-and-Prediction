# coding gbk
# -*-utf-8-*-
from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup


def crawlRankYear(url, headers, year):
    print("crawlRankYear:" + url)
    res = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(res, 'lxml')
    movieTable = soup.find('div', {'class': 'a-section imdb-scroll-table-inner'})
    movieRowList = movieTable.find_all('tr')[1:]
    for row in movieRowList:
        info = row.find_all('td')
        rank = info[0].text
        title = info[1].text
        sublink = info[1].find('a').get('href')
        worldwide = info[2].text
        tconst = crawlTconst(sublink, headers)
        pageLink = f'https://www.imdb.com/title/{str(tconst)}/'
        dic = {
            'rank': rank,
            'year': year,
            'title': title,
            'page': pageLink,
            'tconst': tconst,
            'worldwide': worldwide,
        }
        print(dic)
        resList.append(dic)
    sleep(0.1)


def crawlTconst(suburl, headers):
    print("crawlTconst:" + suburl)
    res = requests.get(url=f'https://www.boxofficemojo.com/{str(suburl)}/', headers=headers).text
    soup = BeautifulSoup(res, 'lxml')
    try:
        tconst = \
            soup.find('a', {'class': 'a-link-normal mojo-title-link refiner-display-highlight'}).get("href").split('/')[
                2]
    except AttributeError:
        tconst = ''
    sleep(0.1)
    return tconst

def saveAsCsv(path):
    print("len resList: " + str(len(resList)))
    df = pd.DataFrame(resList)
    df.to_csv(path, encoding='utf-8', index=False)


if __name__ == '__main__':
    resList = []
    myCookie = "aws-ubid-main=687-7727701-5785554; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6ImFmY2M3ZGEzLWQyNWMtNGNmMC04ZTdkLWEzOGMyOTlhNTUxNSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiTWppbUtVd3JQaXI0VFYyNWJVZDFUWGh2MXhCRHVaN2lFSXNHQ0pmUUFNYz0iLCJhcm4iOiJhcm46YXdzOmlhbTo6NDE1NjMxMDM0OTg5OnJvb3QiLCJ1c2VybmFtZSI6Imppbmd0aWFuemhhbmcifQ.7jI-2DTe3zo5C8Z50EXA43V0ptuSftiK2ejtwySlCHA1wgF42YTDAL_z_CUqbsMS2EZs8PoZRWTGHnwGEYyaWcnk1lt_fF64i2_bzrU0_ZKBLQktFA6q-8mj2bQskUGR; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A415631034989%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22jingtianzhang%22%2C%22keybase%22%3A%22MjimKUwrPir4TV25bUd1TXhv1xBDuZ7iEIsGCJfQAMc%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Cookie': myCookie,
        'Host': 'www.boxofficemojo.com'
    }
    for year in range(2022, 2009, -1):  # 2021
        url = f'https://www.boxofficemojo.com/year/world/{str(year)}/'
        crawlRankYear(url, headers, year)

    saveAsCsv('crawl.dataset.csv')
