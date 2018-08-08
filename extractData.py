import urllib.request
import time
import random
import json
import sys
import os




#http://api.dataide.eastmoney.com/data/GDZY_GD_SUM?
# pageindex=1
# &pagesize=50
# &orderby=updatedate
# &order=desc
# &jsonp_callback=var%20yhlvEXWG=(x)
# &scode=000078
# &rt=51118956

def GenRT():
    t = time.time()
    return int(round(t*1000)/30000)

def GenRandomName(num):
    str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    finalStr = ""
    for i in range(0,num):
        finalStr+=str[random.randint(0,51)]
    return finalStr

def composeURL(stockcode):
    url = "http://api.dataide.eastmoney.com/data/GDZY_GD_SUM?"
    url += "pageindex=1"
    url += "&pagesize=50"
    url += "&orderby=updatedate"
    url += "&order=desc"
    url += "&jsonp_callback=var%20"
    url += str(GenRandomName(8))
    url += "=(x)"
    url += "&scode="
    url += str(stockcode)
    url += "&rt="
    url += str(GenRT())
    return url


def main(argv=None):
    if argv is None:
        argv = sys.argv    
    
    outputFile = "output.txt"

    f = open("stockcodes.txt")
    lines = f.readlines()

    with open(outputFile,'w',encoding='utf-8') as fileobject:
        for line in lines:
            print("Processing " + line)
            stockcode = line.strip()
            response = urllib.request.urlopen(composeURL(stockcode))
            html_doc = response.read()
            # gd_name 股东名称
            # zy_count 累计质押笔数
            # data.gpsl_sum * 10000, 'w', data.gpsl_sum * 10000, 1 //累计质押股数
            # new_zy_count) //最新质押笔数
            # amtsharefrozen //剩余质押股数
            # ...其他数据参考test.html line 1412 - 1422
            json_obj = json.loads(html_doc[13:])
            
            if len(json_obj['data'])>0:
                fileobject.write('\n')
                fileobject.write('\n')
                fileobject.write(json_obj['data'][0]['sname'])
                fileobject.write('\n')

                for item in json_obj['data']:                    
                    fileobject.write(str(item['gd_name'])+'\t\t'+str(item['amtsharefrozen']) + '万元\n')

if __name__ == "__main__":
    sys.exit(main())