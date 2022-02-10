# 根据染色体位置，坐标，和基因组版本，爬取NCBI dbsnp库rsID编号
import requests

requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup


def choice_result(pos, limit, soup):
    str = ':' + pos + '\n(' + limit + ')'
    flag = False
    all_result = soup.find_all(style="float:left")
    all_text = soup.find_all(class_='rprt')
    all_choice = soup.find_all('dl')  # 几种出现结果的详细信息
    # print(len(all_text))
    index = []
    for i in range(len(all_text)):
        if all_text[i].text.find('has merged into') != -1:
            index.append(i)
    # print(index)
    for i in range(len(index)):
        if i == 0:
            del all_choice[index[i]]
            num = 0
        else:
            num += 1
            del all_choice[index[i] - num]
    # print(len(all_choice))
    for i in range(len(all_choice)):
        for string in all_choice[i].stripped_strings:
            # print(string)
            # print('------------')
            if flag == False:
                if string == str:
                    real_choice = all_result[i].find('a').text
                    return real_choice
                elif string == pos:
                    flag = True
                    continue
                else:
                    continue
            else:
                if string == '(' + limit + ')':
                    real_choice = all_result[i].find('a').text
                    return real_choice


def get_rsID(chr, pos, limit):
    url = 'https://www.ncbi.nlm.nih.gov/snp/?term=' + chr + '%3A' + pos
    r = requests.get(url, timeout=60, verify=False)
    raw_html = r.text
    soup = BeautifulSoup(raw_html, 'html.parser')
    all_result = soup.find_all(style="float:left")
    if len(all_result) == 1:
        result = all_result[0].find('a').text
    elif len(all_result) > 1:
        print('共有{}种可能的结果'.format(len(all_result)))  # 因为搜索出来可能有多个条目，需要根据基因组版本号判断
        result = choice_result(pos, limit, soup)
    else:
        result = ''
    return result


# 指定chr,pos,GRCh来爬取SNP rsID,利用for循环可批量爬取

result = get_rsID('2', '27730940', 'GRCh37')
print(result)

