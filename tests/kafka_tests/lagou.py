# -*- coding: utf-8 -*-

import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from pyecharts.charts import Geo
from wordcloud import WordCloud
import re
import matplotlib
from imageio import imread

url="https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"

def data(page):
    return {
        "first": "true",
        "pn": f"{page}",
        "kd": "python",
        'sid': '4256fece2141497bb5a8e1bfa69bcee7'
    }

def get_cookies():
    headers={
        'origin': 'https://www.lagou.com',
        'referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'authority': 'www.lagou.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }
    response=requests.get('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',headers=headers)
    return response.cookies.get_dict()

cookies=get_cookies()

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    ,'host':'www.lagou.com'
    ,'origin': 'https://www.lagou.com'
    ,'referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='}

def get_data(data):
    response = requests.post(url=url, headers=headers, data=data, cookies=cookies)
    # json数据
    if not response.json()['status']:
        print(response.json())
        return
    content = response.json()['content']['positionResult']['result']
    j = 1
    companyLabelstr=''
    for i in content:
        city = i['city']
        companyFullName = i['companyFullName']
        companySize = i['companySize']
        education = i['education']
        positionName = i['positionName']
        salary = i['salary']
        workYear = i['workYear']
        companyLabelList=i['companyLabelList']

        if len(companyLabelList)>0:
            companyLabelList=''.join(companyLabelList)
        else:
            companyLabelList=''

        '''
        companyLabelstr=companyLabelList+companyLabelstr
        print(workYear,companyLabelList)
        print(companyLabelstr)
        '''

        with open('python.csv', 'a+', encoding='utf-8')as f:
            f.write(f'{city},{companyFullName},{companySize},{education},{positionName},{salary},{workYear},{companyLabelList}\n')

        print(f'第{j}条数据成功')

        j += 1

if __name__ == '__main__':
    for i in range(1, 11):
        params = data(i)
        get_data(params)


# 下面对爬取的文本进行分析
# XM返佣https://www.kaifx.cn/broker/x...

matplotlib.rcParams['font.family']='SimHei'

plt.rcParams['axes.labelsize']=16
plt.rcParams['xtick.labelsize']=14
plt.rcParams['ytick.labelsize']=14
plt.rcParams['legend.fontsize']=12
plt.rcParams['figure.figsize']=[15,9]

data=pd.read_excel(r'C:\temp\python2.xls',encoding='utf-8')

#1.学历

data['学历'].value_counts().plot(kind='bar',rot=0)

#2.工作经验

data['年限'].value_counts().plot(kind='bar',rot=0,color='g')

#3.城市分析

plt.rcParams['figure.figsize']=[15,15]

data['城市'].value_counts().plot(kind='pie',autopct='%1.2f%%',explode=np.linspace(0,1.5,18))

#4.公司待遇分析

# (1)分词操作

a=len(data['公司福利'])

str=''

for i in range(a):
    b=data['公司福利'][i]
    if type(b)==float:
        b=''
    str=str+b

jieba.add_word('五险一金')

jieba.add_word('牛B')

jieba.add_word('年底双薪')

jieba.add_word('带薪年假')

jieba.add_word('股票期权')

jieba.add_word('定期体检')

jieba.add_word('节日礼物')

words = jieba.lcut(str)

counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1

items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)

with open('词频统计',mode='w',encoding='utf-8')as f:
    for i in range(20):
        word,count=items[i]
        f.writelines('{}\t{}\n'.format(word,count))

# (2)词云图展示

with open('词频统计',mode='r',encoding='utf-8')as f:
    text=f.read()
    wc=WordCloud(font_path=r'C:\Users\2020\Desktop\simhei.ttf',background_color='white',width=1000,max_words=100,height=860,margin=2).generate(text)

plt.imshow(wc)
plt.axis('off')
plt.show()

# 5.全国工资水平分析

data2=list(map(lambda x:(data['城市'][x],eval(re.split('k|K',data['工资'][x])[0])*1000),range(len(data))))

data3=pd.DataFrame(data2,index)

data4=list(map(lambda x:(data3.groupby(0).mean()[1].index[x],data3.groupby(0).mean()[1].values[x]),range(len(data3.groupby(0)))))

geo=Geo('全国python工资布局','制作人：止疼',title_color='#fff',title_pos='left',width=1200,height=600,background_color='#404a59')

attr,value=geo.cast(data4)

geo.add('',attr,value,type='heatmap',is_visualmap=True,maptype='china',visual_range=[0,300],visual_text_color='#fff')

geo.render()


