#!/usr/bin/env python
import aiohttp
import asyncio
import time

from os import system, name
from clint.textui import colored, puts
from progress.spinner import Spinner

#бес не заебуй xD

class AdminPanelSearchTool(object):

    def __init__(self):
        self._banner()
        self._url = None
        self._wordlist = []
        self._status_200 = []
        self.redirected = []
        self._scanned_dirs_count = 0
        self._bar = Spinner()

    def _banner(self):
        self._clear_console()
        self._clintprint("""
                   _              _ 
    __ _ _ __  ___| |_ ___   ___ | |
   / _` | '_ \/ __| __/ _ \ / _ \| |
  | (_| | |_) \__ \ || (_) | (_) | |  [Author]: fu11p0w3r
   \__,_| .__/|___/\__\___/ \___/|_|  [Version]: 0.2
        |_|                         
  Admin panel search tool
  """)

    @staticmethod
    def _clear_console():
        system('cls' if name == 'nt' else 'clear')

    @staticmethod
    def _clintprint(text, color=None):
        if color == 'green':
            puts(colored.green(text))
        elif color == 'red':
            puts(colored.red(text))
        elif color == 'yellow':
            puts(colored.yellow(text))
        else:
            puts(colored.white(text))

    async def _scan(self, url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),
                                         requote_redirect_url=False) as session:
            try:
                async with session.get(url, allow_redirects=False) as response:
                    self._scanned_dirs_count += 1
                    if response.status == 200:
                        self._status_200.append(url)
                    elif response.status == (300 or 301 or 302):
                        self.redirected.append(url)
                        
            except aiohttp.ClientConnectorError:
                self._clintprint('[ERROR] Connection error, trying next...', 'red')
                
            except aiohttp.InvalidURL:
                self._clintprint('\n[ERROR] Incorrect url address, please enter a correct url!', 'red')
                exit()
                
            except ConnectionResetError:
                self._clintprint('\n[ERROR] The remote host has forcibly dropped the connection!', 'red')
                exit()
                
            except aiohttp.ClientOSError:
                self._clintprint('\n[ERROR] The remote host is no longer available!', 'red')
                exit()
                
            else:
                self._banner()
                self._print_current_founded()
         
                self._clintprint(' ')
                self._bar.next()
                self._clintprint(f' Scanning...')
                self._clintprint(f'==> {url}', 'red')

    def _print_current_founded(self):
        if self._status_200:
            self._clintprint('[INFO] Founded with status code 200:')
            for url in self._status_200:
                self._clintprint(f'[+] {url} ', 'green')
        if self.redirected:
            self._clintprint('[INFO] Found with possible redirect:')
            for url in self.redirected:
                self._clintprint(f'[!] {url} ', 'yellow')

    def _print_total_info(self, elapsed_time):
        self._banner()
        self._clintprint(f'[INFO] A total of {self._scanned_dirs_count} possible locations were enumerated')
        if elapsed_time > 60:
            self._clintprint(f'[INFO] A total spent time: {elapsed_time // 60} min {elapsed_time % 60} sec\n')
        else:
            self._clintprint(f'[INFO] A total spent time: {elapsed_time} sec\n')
            self._print_current_founded()

    def load_wordlist(self, path):
        try:
            file = open(path, 'r')
        except FileNotFoundError:
            self._clintprint('[ERROR] The wordlist with locations was not found. \n'
                             '        Please put the wordlist in the root of this', 'red')
            exit()
        else:
            for line in file:
                self._wordlist.append(line.strip('\n'))
            file.flush()
            file.close()
            self._clintprint('\n[INFO] List with possible page locations loaded!')
            time.sleep(1)
            self._clintprint('[INFO] Start scanning, please wait...')
            time.sleep(1)

    def run(self):
        start_time = time.time()
        if name == 'nt':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)

        loop = asyncio.get_event_loop()
        full_urls = [self._url + str(_) for _ in self._wordlist]
        tasks = [self._scan(url) for url in full_urls]
        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except KeyboardInterrupt:
            self._banner()
            self.print_byee_and_exit()
        except aiohttp.ClientOSError:
            self._clintprint('[ERROR] The specified host is no longer available')
            exit()
        else:
            self._bar.finish()
            total_elapsed_time = int(time.time() - start_time)
            self._print_total_info(total_elapsed_time)

    def input_url(self):
        try:
            self._banner()
            self._clintprint('Example: http://google.com')
            self._url = str(input('[=>] Enter the full URL to start: '))
        except KeyboardInterrupt:
            self.print_byee_and_exit()

    def print_byee_and_exit(self):
        self._clintprint('\n[!] CTRL+C pressed, Byeeee!!!', 'yellow')
        exit()


if __name__ == '__main__':
    finder = AdminPanelSearchTool()
    finder.input_url()
    finder.load_wordlist('wordlist.txt')
    finder.run()
