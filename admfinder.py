#!/usr/bin/env python
import argparse
import os
import requests
from clint.textui import colored, puts


def banner():
    puts(colored.white("""  
██████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗███████╗██╗███╗   ██╗██████╗ ███████╗██████╗   
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗ 
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝ 
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗ 
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║ 
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝ v0.1 
This is a tool that helps you find the admin panel on the site     [Author]:fu11p0w3r """))


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
                puts(colored.yellow('  [ ! ] Connection timeout error, please set the -t argument to more'))
                continue
            if (req_status == 200):
                puts(colored.green('  [200] {}'.format(query + url)))
                result.append(query + url)
            else:
                puts(colored.red('  [{}] {}'.format(req_status, query + url)))
    f.close()


if __name__ == '__main__':
    os.system('clear')
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, metavar='url', help='Url address for scanning. For example: http://target.com')
    parser.add_argument('-t', type=float, metavar='sec', help='Timeout for your request. By default 0.5 seconds', default=0.5)

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
        puts(colored.red("  [Error] Please specify the url address to scan using the -u argument or use -h to call for help"))
        exit(0)
