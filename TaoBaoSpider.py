import requests
import re
import time
import json
import pymysql
from TB import GetCookies
from io import StringIO

def GetSession(username, password):
    return GetCookies.SessionDriver().get_session(username, password)



def DataImport(sql):
    conn=pymysql.connect(host='127.0.0.1', user='root', password='123456', db='tests', charset='utf8')
    conn.query(sql)
    conn.commit()
    conn.close()

def GetPrarms(page, keyword):
    loctime = time.time()
    lt = time.localtime(int(loctime))
    st = time.strftime('%Y%m%d', lt)
    t = str(loctime * 1000).replace('.', '_')
    cn = int(t[14:])
    params = {
        'ajax': 'true',
        '_ksTS': t,
        'callback': 'jsonp%s'%(str(cn+1)),
        'q': keyword,
        'imgfile': '',
        'js':'1',
        'stats_click': 'search_radio_all:1',
        'ie': 'utf8',
        'initiative_id': 'staobaoz_%s'% str(st),
        'bcoffset': '0',
        'ntoffset': '6',
        'p4ppushleft': '1,48',

    }
    if page == 1:
        params['data-key'] = 's,ps'
        params['data-value'] = '0,1'
    else:
        params['data-key'] = 's'
        params['data-value'] = str((page-1)*44)
        params['s'] = str((page-1)*44-44)

    return params,cn


def GetDatas(url, params, cookies,cn):
    sessions = requests.session()
    sessions.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

    try:
        res = sessions.get(url, params=params, cookies=cookies, verify=False).text
        print(res)
        redict = re.compile('jsonp%s(.*)' % (str(cn + 1)))
        content = redict.findall(res)
        data = content[0].strip('(;)')
        jsondata = json.loads(data)
        ss = jsondata['mods']['itemlist']['data']['auctions']
        for s in ss:
            name = s['raw_title']   #名称
            price = s['view_price']   #价格
            sales_vol = s['view_sales'][:-3]  #销量
            sql = "insert into taobao(name,price,sales) values('%s','%s','%s')" % (name, price, sales_vol)
            DataImport(sql)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    s = StringIO()
    url = 'https://s.taobao.com/search'
    keyword = '铅笔'
    # cookiesfile = 'mycookies.txt'
    cookiesdata = GetSession('账号', '密码')    #此处填写微博账号密码
    s.write(str(cookiesdata))
    cookies = eval(s.getvalue())
    for i in range(1, 3):   #这是页数
        print('**************第%s页数据*****************' % i)
        params = GetPrarms(page=i, keyword=keyword)
        GetDatas(url=url, cookies=cookies, params=params[0], cn=params[1])

