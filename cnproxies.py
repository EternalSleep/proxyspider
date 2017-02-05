import requests
import re

def char2num(value_js):
    ''' Get char--num from js code '''
    value_str = value_js[1:]
    single_value_list = value_str.split(';')[:-1]
    ans = {}
    for single_value in single_value_list:
        char,value = single_value.split('=')
        value_num = value[1:-1]
        ans[char] = value_num
    return ans

def decode_js(char_num_dict,cur_addr):
    ''' Get port from js code '''
    ip = re.search('[\d]*.[\d]*.[\d]*.[\d]*',cur_addr).group()
    port_doc = re.search('\((.*?)\)',cur_addr).group(1)
    port_piece = port_doc.split('+')
    single_char = filter(lambda x:len(x) == 1,port_piece)
    single_num = [ char_num_dict[char_item] for char_item in single_char ]
    return ip + ':' + ''.join(single_num)


def get_cnproxies():
    ''' Get proxies from cnproxy.com '''
    cnproxies = []
    for i in range(1,11):
        link = 'http://www.cnproxy.com/proxy'+str(i)+'.html'
        r = requests.get(link)  # Maybe proxies needed

        re_js = re.compile('<SCRIPT[\s\S]*?>([\s\S]*?)</SCRIPT>')
        jsiter = re_js.finditer(r.content)
        value_js = jsiter.next().group(1)
        char_num_dict = char2num(value_js)

        td_re = re.compile('<td[\s\S]*?>([\s\S]*?)</td>')
        td_tags = td_re.findall(r.content)[4:]

        for index in range(len(td_tags)/4):
            cur_addr = td_tags[index*4]
            cur_type = td_tags[index*4+1].lower()
            aka_addr = decode_js(char_num_dict,cur_addr)
            cur_proxy = {}
            cur_proxy[cur_type] = cur_type + '://' + aka_addr
            cnproxies.append(cur_proxy)
    return cnproxies
