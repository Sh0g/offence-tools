import os
import sys
import threading
import subprocess
import dns.resolver
import aiohttp
import asyncio
from aiohttp import *
import time

uniqueDomain = []
url_404 = []
inputURL = []

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

def main():
    domain = input('Domain name of the taget [ex : hackerone.com]: ')
    file_path = input('Provide location of subdomain file to check for takeover if subfinder is not installed. [ex: /path/of/subdomain/file] (leave blank if not using file): ')
    output_file = input('Output unique subdomains of sublist3r and subfinder to text file [ex: uniqueURL.txt] (leave blank for default uniqueURL.txt): ') or 'uniqueURL.txt'
    protocol = input('Set protocol for requests. Default is "http" [ex: https] (leave blank for default http): ') or 'http'

    def getSubdomain(subData):

        try:
            stdout_string = subprocess.check_output(['subfinder', '-silent', '-version'], stderr=subprocess.STDOUT)

            try:
                stdout_string = subprocess.check_output(['sublist3r'], stderr=subprocess.STDOUT)
                print('\033[92m[-] Default http [use -p https]')
                print('\033[92m[-] Gathering Information...')
                time.sleep(2)

                print('\033[96m[-] Enumerating subdomains for '+'\033[94m'+domain)
                with Spinner():
                    os.popen('sublist3r -d '+subData+' -o sublist3r_list.txt').read()
                    os.popen('subfinder -t 15 -d  '+subData+' -silent > subfinder_list.txt').read()

            except subprocess.CalledProcessError as cpe:
                print('\033[96m[!] Sublist3r not found\033[91m !!!\n\033[93m[-] Install it or use -f with subdomain.txt file.')
                sys.exit()

            except OSError as e:
                print('\033[96m[!] Sublist3r not found\033[91m !!!\n\033[93m[-] Install it or use -f with subdomain.txt file.')
                sys.exit()

        except subprocess.CalledProcessError as cpe:
            print('\033[96m[!] Subfinder not found\033[91m !!!\n\033[93m[-] Install it or use -f with subdomain.txt file.')
            sys.exit()

        except OSError as e:
            print('\033[96m[!] Subfinder not found\033[91m !!!\n\033[93m[-] Install it or use -f with subdomain.txt file.')
            sys.exit()

        if os.path.isfile('sublist3r_list.txt'):
            pass
        else:
            fpa = open("sublist3r_list.txt", "w")
            fpa.close()

        lines1 = open("sublist3r_list.txt", "r").readlines()
        lines2 = open('subfinder_list.txt', 'r').readlines()
        data1 = []
        data2 = []

        for line in lines1:
            data1.append(line.strip())

        for line in lines2:
            data2.append(line.strip())

        if os.path.isfile('sublist3r_list.txt'):
            os.remove('sublist3r_list.txt')

        if os.path.isfile('subfinder_list.txt'):
            os.remove('subfinder_list.txt')

        for x in data1:
            uniqueDomain.append(protocol+'://'+x)

        for line_diff in data2:
            if line_diff not in data1:
                uniqueDomain.append(protocol+'://'+line_diff)

        print('\033[93m[-] Total Unique Subdomain Found: '+" "+str(sum(1 for line in uniqueDomain)))

        with open(output_file, 'w') as fp:
            for x in uniqueDomain:
                if 'http://' or 'https://' in x:
                    r = x.replace("https://", "")
                    r = r.replace("http://", "")
                    fp.write(r+"\n")
            fp.close()
        with Spinner():
            asyncio.run(getCode())
        if len(url_404) == 0:
            print('\033[94m[*] Task Completed :)')
            print('\033[91m[!] Target is not vulnerable!!!')
            sys.exit()
        cnameExtract(url_404)

    def getResponseCode(inputFile):

        try:
            data = open(inputFile, "r")
            print('\033[96m[-] Reading file '+'\033[94m'+inputFile)
            print('\033[92m[-] Gathering Information...')

            time.sleep(2)
            print('\033[93m[-] Total Unique Subdomain Found: '+" "+str(sum(1 for line in open(inputFile, 'r'))))
            time.sleep(1)
            print('\033[92m[-] Default http [use -p https] ')
            time.sleep(1)
            print('\033[92m[-] Checking response code...')

        except NameError:
            print("\n\033[91m[!] "+inputFile+" File not found...!!!\n\033[92m[-] Check filename and path.")
            sys.exit()

        except IOError:
            print("\n\033[91m[!] "+inputFile+" File not found...!!!\n\033[92m[-]Check filename and path.")
            sys.exit()

        subdomain = data.readlines()
        for line in subdomain:
            if 'http://' or 'https://' in line:
                inputURL.append(line.strip())

            else:
                inputURL.append(protocol+"://"+line.strip())

        with Spinner():
            asyncio.run(urlCode())

        if len(url_404) == 0:
            print('\033[94m[*] Task Completed :)')
            print('\033[91m[!] Target is not vulnerable!!!')
            sys.exit()

        cnameExtract(url_404)

    def cnameExtract(invalidURLs):
        print('\033[92m[-] Checking CNAME records...\n')
        for x in invalidURLs:
            if 'http://' or 'https://' in x:
                data = x.replace('https://', '')
                data = x.replace('http://', '')
            else:
                pass
            try:
                resolve = dns.resolver.query(data.strip(), 'CNAME')
                for rdata in resolve:
                    cdata = (rdata.to_text()).strip()
                    targetDomain = data.strip()
                    if targetDomain[-8:] not in cdata:
                        print('\n\033[96m[-] Vulnerability Possible on: ' + '\033[92m' + str(
                            data) + "\n\t" + '\033[94mCNAME: ' + '\033[93m' + str(rdata.to_text()))
                    else:
                        print('\n\033[92m[-] ' + str(data) + '\n' + '\033[91m \tNot Vulnerable')
            except:
                print('\n\033[92m[-] ' + str(data) + '\n' + '\033[91m \tNot Vulnerable')
        print('\033[94m[*] Task Completed :)')
        sys.exit()

        if file_path:
            if domain:
                print('\033[91m[!] Use only -f option with subdomain file')
                sys.exit()
            else:
                pass

            getResponseCode(file_path)

        else:
            pass

        if domain:
            if 'http://' in domain or 'www.' in domain or 'https://' in domain:
                domain = domain.replace('https://', '')
                domain = domain.replace('http://', '')
                domain = domain.replace('www.', '')
                getSubdomain(domain)

            else:
                getSubdomain(domain)

        else:
            print('usage: sub404.py [-d DOMAIN] [-f FILE] [-o OUTPUT] [-p PROTOCOL]')

        # check response code

    async def getCode():
        async with aiohttp.ClientSession() as session:
            await gen_tasks(session, 'random.txt')

    async def urlCode():
        async with aiohttp.ClientSession() as session:
            await gen_input_tasks(session, 'random.txt')

    async def fetch_url(session, url):
        count = 0
        try:
            async with session.get(url) as response:
                reason = response.reason
                status = response.status

                if status == 404:
                    url_404.append(url)
                    pass
                else:
                    pass

        except ClientConnectionError:
            return (url, 500)
        except ClientOSError:
            return (url, 500)
        except ServerDisconnectedError:
            return (url, 500)
        except asyncio.TimeoutError:
            return (url, 500)
        except UnicodeDecodeError:
            return (url, 500)
        except TooManyRedirects:
            return (url, 500)
        except ServerTimeoutError:
            return (url, 500)
        except ServerConnectionError:
            return (url, 500)
        except RuntimeError:
            pass
        except OSError:
            pass
        except Exception as err:
            pass

    async def gen_input_tasks(session, url_list):
        tasks = []
        print('\033[92m[-] Getting URL\'s of 404 status code...')
        for url in inputURL:
            task = asyncio.ensure_future(fetch_url(session, url))
            tasks.append(task)
        result = await asyncio.gather(*tasks)
        print('\033[93m[-] URL Checked: ' + str(len(inputURL)))
        time.sleep(1)
        return result

    async def gen_tasks(session, url_list):
        tasks = []
        print('\033[92m[-] Getting URL\'s of 404 status code...')
        for url in uniqueDomain:
            task = asyncio.ensure_future(fetch_url(session, url))
            tasks.append(task)
        result = await asyncio.gather(*tasks)
        print('\033[93m[-] URL Checked: ' + str(len(uniqueDomain)))
        time.sleep(1)
        return result

    if __name__ == "__main__":
        main()