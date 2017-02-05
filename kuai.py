'''kuai proxies'''
import requests
import re

def kuaiproxies():
    headers = {'Host': 'www.kuaidaili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Cookie': '_ga=GA1.2.1164191173.1486264808; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1486264808; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1486267087; channelid=0; sid=1486264179483975; _gat=1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                }

    kuai_link = 'http://www.kuaidaili.com/proxylist/'
    proxies = []
    for i in range(1,11):
        cur_link = kuai_link + str(i) + '/'
        s = requests.session()
        r = s.get(cur_link,headers = headers)
        td_re = re.compile('<td[\s\S]*?>([\s\S]*?)</td>')
        tds = td_re.findall(r.content)
        for index in range(10):
            cur_proxy = {}
            ip = tds[index*8]
            port = tds[index*8+1]
            con_type = tds[index*8+3].split(',')
            con_type = [item.lower() for item in con_type]
            for proxy_type in con_type:
                cur_proxy[proxy_type] = proxy_type + '://' + ip + ':' + port
            proxies.append(cur_proxy)
    return proxies
