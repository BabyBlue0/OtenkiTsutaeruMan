"""
pip install beautifulsoup4
pip install parse
"""

import urllib.request
from bs4 import BeautifulSoup
from parse import *

#tenki.jpの地域別の天気予報URL
url = 'https://tenki.jp/forecast/4/20/5610/17212/' #野々市市
#url = 'https://tenki.jp/forecast/4/20/5610/17201/' #金沢市
res = urllib.request.urlopen(url)
soup = BeautifulSoup(res, 'html.parser')

#日付抜き出し　date_list = [month(int), day(int), weekday(string)]
place = search( '{}の天気', soup.find_all('h2')[0].text )[0]
full_date = soup.select_one('h3.left-style').text
date_list = list( search('{:02d}月{:02d}日({:1})', full_date ) )
print( '{}月{}日{}曜日、{}の今日の天気をお知らせします'.format(date_list[0], date_list[1], date_list[2], place) )

#本日の天気
weather_dict = {'晴':'晴れ','曇':'曇り'} #辞書登録すること！！！！！！！！！！！！！！
today_weather = soup.select_one('.weather-telop').text
print( '今日の天気は{}、'.format( weather_dict[today_weather] if today_weather in weather_dict.keys() else today_weather))

#最高気温、最低気温
max_and_min_temp = soup.select('.value')
max_temp = max_and_min_temp[0].text
min_temp = max_and_min_temp[1].text
print('最高気温は{}度、最低気温は{}度です'.format(max_temp,min_temp))

#各時間ごとの降水確率
rain_prob_table = soup.find_all('td')
rain_prob_list = [ rain_prob_table[i].text for i in range( 0, 4 )]
print('続いて降水確率のお知らせをします')
for t,p in zip( ['午前0時から午前6時', '午前6時からお昼12時', 'お昼0時から午後6時', '午後6時から深夜0時'], rain_prob_list ):
    if( p != '---' ):
        print( '{}は、{}。'.format( t, p ))
print('です')
