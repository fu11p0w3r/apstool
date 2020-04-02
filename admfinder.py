#!/usr/bin/env python
import argparse
import os

import requests
from clint.textui import colored, puts


def banner():
    puts(colored.white("""  
█████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗███████╗██╗███╗   ██╗██████╗ ███████╗██████╗   
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗ 
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝ 
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗ 
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║ 
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝ v0.1 
That tool may can help u for search admin page of our site         [Author]:fu11p0w3r """))


def check(query):
    puts(colored.green('<><><><><><><><><><><><><><><><><><><><><><>'))
    with open('wordlist.txt') as f:
        for url in f:
            try:
                url = url.strip('\n')
                req_status = requests.get(query + url, timeout=args.t).status_code
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                puts(colored.yellow('  [ ! ] Connection timeout error, please set a -t sec so large'))
                continue
            if (req_status == 200):
                puts(colored.green('  [200] {}'.format(query + url)))
                result.append(query + url)
            else:
                puts(colored.red('  [{}] {}'.format(req_status, query + url)))
    f.close()


if __name__ == '__main__':
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, metavar='url', help='Url for scan without ex http://targer.com without /')
    parser.add_argument('-t', type=float, metavar='sec', help='A timeout of your request, default 0.5 sec', default=0.5)

    args = parser.parse_args()
    if args.u is not None:
        result = []
        check(args.u)
        if len(result) != 0:
            os.system('clear')
            banner()
            puts(colored.green('<><><><><><><><><><><><><><><><><><><><><><>'))
            for i in result:
                puts(colored.green('  [FOUND] ' + i))
        else:
            exit(0)
    else:
        puts(colored.red("  [Error] Please write a url for scan with -u or write -h for help"))
        exit(0)
