import requests
import smtplib, ssl
import os
import datetime as DT
import pw


today = DT.date.today()
week_ago = today - DT.timedelta(days=7)

#fetch
newsapi_apikey=pw.newsapi_apikey
keyword='nintendo'
url='https://newsapi.org/v2/everything?'\
    f'q={keyword}'\
    f'&from=2{week_ago}'\
    '&sortBy=publishedAt'\
    '&language=en'\
    f'&apiKey={newsapi_apikey}'

r=requests.get(url)
r_dict=r.json()
article_list=[i for i in r_dict['articles'] if i['source']['name'] != '[Removed]'] #remove articles that are [removed]

message=f"Subject: {keyword.capitalize()}'s news from last week\n"
for i in article_list[:20]:
    message += i['title'] + '\n' + i['description'] + '\n' + i['url'] + '\n\n'
message = message.encode('utf-8')


#send email
host = 'smtp.gmail.com'
port = 465
context = ssl.create_default_context()
username=pw.username
password=pw.password
receiver=pw.receiver

with smtplib.SMTP_SSL(host,port,context=context) as server:
    server.login(username,password)
    server.sendmail(username,receiver,message)
    print('Email sent!')
