#!/usr/bin/env python
import aiohttp
import asyncio
import time

from os import system, name
from clint.textui import colored, puts
from progress.spinner import Spinner


class AdminFinder(object):

    def __init__(self):
        self._banner()
        self._url = None
        self._dir_list = []
        self._status_200 = []
        self.redirected = []
        self._scanned_dirs_count = 0
        self._bar = Spinner()

    def _banner(self):
        self._clear_console()
        self._clintprint("""  
    ██████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗███████╗██╗███╗   ██╗██████╗ ███████╗██████╗   
    ██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗ 
    ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝ 
    ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗ 
    ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║ 
    ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝ v0.2 
    Little tool for searching admin panel login forms                  [Author]: fu11p0w3r """)

    def _mini_banner(self):
        self._clintprint('  /==[ ADMINFINDER ]==\\ \n')

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
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, enable_cleanup_closed=True),
                                         requote_redirect_url=False, ) as session:
            try:
                response = await session.get(url, allow_redirects=False)
            except aiohttp.ClientConnectorError:
                self._clintprint('\n[ERROR] Connection error, request timeout for connection to this site!', 'red')
                exit()
            else:
                self._scanned_dirs_count += 1
                if response.status == 200:
                    self._status_200.append(url)
                elif response.status == (300 or 301 or 302):
                    self.redirected.append(url)

                self._clear_console()

                self._mini_banner()

                if self._status_200:
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
            self._clintprint('[INFO] Founded with redirect:')
            for url in self.redirected:
                self._clintprint(f'[!] {url} ', 'yellow')

    def _print_total_info(self, elapsed_time):
        self._clear_console()
        self._mini_banner()
        self._clintprint(f'[INFO] Total scanned dirs: {self._scanned_dirs_count}')
        if elapsed_time > 60:
            self._clintprint(f'[INFO] Total elapsed time: {elapsed_time // 60} min {elapsed_time % 60} sec\n')
        else:
            self._clintprint(f'[INFO] Total elapsed time: {elapsed_time} sec\n')
            self._print_current_founded()

    def load_dir_list(self, path):
        try:
            file = open(path, 'r')
        except FileNotFoundError:
            self._clintprint('[ERROR] Directory list not found. Pls put dirlist file to program root directory!', 'red')
            exit()
        else:
            for line in file:
                self._dir_list.append(line.strip('\n'))
            file.flush()
            file.close()
            self._clintprint('\n[INFO] Directory list loaded!')
            self._clintprint('[INFO] Starting your scan, pls wait...')

    def run(self):
        start_time = time.time()
        if name == 'nt':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)

        loop = asyncio.get_event_loop()
        full_urls = [self._url + str(dir) for dir in self._dir_list]
        tasks = [self._scan(url) for url in full_urls]
        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except KeyboardInterrupt:
            self._mini_banner()
            self._clintprint('[CTRL+C] Byeeee!!!', 'yellow')
        else:
            self._bar.finish()
            total_elapsed_time = int(time.time() - start_time)
            self._print_total_info(total_elapsed_time)

    def set_url(self, url):
        self._url = url


if __name__ == '__main__':
    finder = AdminFinder()
    finder.set_url(str(input('[=>] Enter url for scan: ')))
    finder.load_dir_list('dirlist.txt')
    finder.run()
