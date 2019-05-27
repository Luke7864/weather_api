# -*- coding: utf-8 -*-
from urllib.request import urlopen
import urllib
import bs4
from flask import *

app=Flask(__name__)

@app.route('/', methods= ['get'])
def api():
    try:
        location=request.args.get('region') #인자 입력받음
        enc_location = urllib.parse.quote(location + '+날씨') #날씨정보 크롤링
        url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location
        req = urllib.request.Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html,'html.parser')
        temp = str(soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text)
        weather= str(soup.find('ul', class_='info_list').find('p', class_="cast_txt").text)

        jsondict={
            'temp':temp,
            'weather':weather
        }
        jsonstr=json.dumps(jsondict, ensure_ascii=False)
        res=make_response(jsonstr)
        res.headers['Content-Type']='application/json'
        return res

    except:
        return "ERROR"

if __name__=='__main__':
    app.run(host='0.0.0.0',port=7003,debug=False)