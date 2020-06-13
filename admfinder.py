#!/usr/bin/env python
import argparse
from os import system, name
from time import sleep

import requests
from clint.textui import colored, puts

def banner():
    system('cls' if name == 'nt' else 'clear')
    puts(colored.white("""  
██████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗███████╗██╗███╗   ██╗██████╗ ███████╗██████╗   
██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗ 
███████║██║  ██║██╔████╔██║██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝ 
██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗ 
██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║ 
╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝ v0.1 
Little tool for searching admin panel login forms                  [Author]: fu11p0w3r """))
    sleep(2)

def scan_mode():
    system('cls' if name == 'nt' else 'clear')
    puts(' ADMINFINDER v0.1')
    puts('[>]Checking...')

def init():
    global FOLDERS
    tmp = []
    with open('wordlist.txt') as f:
        for _ in f:
            tmp.append(_.strip('\n'))
    FOLDERS = tuple(tmp)
def check(query):
    result = []
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) ' \
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    session.max_redirects = 5
    puts(colored.green('<><><><><><><><><><><><><><><><><><><><><><>'))
    for url in FOLDERS:
        try:
            req_status = session.get(query + url, timeout=args.t).status_code
        except KeyboardInterrupt:
            puts(colored.yellow('[V]Byeeee!'))
            exit(0)
        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.ReadTimeout:
            puts(colored.yellow(f'[!] {query + url} => сonnection timeout, please set a larger timeout using the -t argument'))
            puts(colored.yellow(f' Please set a larger timeout using the -t argument'))
            continue
        if (req_status == 200):
            scan_mode()
            puts(colored.green(f'[200] {query + url}'))
            result.append(query + url)
        else:
            scan_mode()
            puts(colored.red(f'[{req_status}] {query + url}'))
        for i in result:
            puts(colored.green(f'[200] {i}'))
    return result

if __name__ == '__main__':
    init()
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, metavar='url', help='Url address for scanning. For example: http://target.com')
    parser.add_argument('-t', type=float, metavar='sec', help='Timeout for your request. By default 0.5 seconds', default=0.3)
    args = parser.parse_args()
    result = check(args.u)
    if args.u is not None:
        if len(result) != 0:
            banner()
            puts(colored.green('<><><><><><><><><><><><><><><><><><><><><>'))
            for i in result:
                puts(colored.green('[200] ' + i))
        else:
            puts(colored.yellow('[:(]Admin forms not found, try another site'))
            exit(0)
    else:
        puts(colored.red("[Error] Please specify the url address to scan using the -u argument or use -h to call for help"))
        exit(0)
