import requests, sys, time

check_url = 'https://coding.net/u/Katsue/p/check/git/raw/master/working.txt'
#check_url = 'https://raw.githubusercontent.com/itsuwari/SocksProxyChecker/master/am_I_working.txt'

class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width
    def move(self, plus):
        self.count += plus
    def log(self, s):
        sys.stdout.write(' ' * (self.width + 9) + '\r')
        sys.stdout.flush()
        print(s)
        progress = int(self.width * self.count / self.total)
        sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        if progress == self.width:
             sys.stdout.write('\n')
        sys.stdout.flush()



def test_proxy(proxies, country_filter=None, isp_filter=None, speed_filter=2, timeout=10, speed_timeout=3):
    bar = ProgressBar(total=len(proxies))
    working = []
    for proxy in proxies:
        socks = {
                'http': 'socks5://%s' % proxy,
                'https': 'socks5://%s' % proxy
        }
        try:
            ip_info = requests.get('http://ip-api.com/json/%s' % proxy.split(':')[0], timeout=5).json()
            country_code = ip_info['countryCode']
            isp = ip_info['isp']
            bar.log('Country: %s ISP: %s' % (country_code, isp))
            time.sleep(1)
            if country_filter:
                if not country_code in country_filter:
                    continue
            if isp_filter:
                if not isp in isp_filter:
                    continue
            if requests.get(check_url, timeout=timeout, proxies=socks).text == 'Works':
                open(out_file, 'a').write('%s\n' % proxy)
                working.append(proxy)
                bar.log('%s is working!' % proxy)
                speed = speedtest([proxy], speed_filter, timeout=speed_timeout)
                open(out_file, 'a').write('%s\n' % str(speed))
                bar.move(1)
        except Exception:
            bar.log('Oops, not working')
            bar.move(1)

    return working

def speedtest(proxies, filter=5, file='http://repos.lax-noc.com/speedtests/10mb.bin', timeout=10):
    bar = ProgressBar(total=len(proxies))
    for proxy in proxies:
        socks = {
                'http': 'socks5://%s' % proxy,
                'https': 'socks5://%s' % proxy
        }
        try:
            seconds = requests.get(file, timeout=timeout, proxies=socks).elapsed.total_seconds()
            bar.log('%s mb/s' % str(10/seconds))
            bar.move(1)
            return 10/seconds
        except Exception:
            bar.log('Oops, timeout')
            bar.move(1)
            return -1


asia = ['TW', 'CN', 'KR', 'JP', 'HK']


in_file = 'asia.txt'
out_file = 'asia_out.txt'

with open(in_file) as f:
    proxies = f.readlines()
proxies = [x.strip() for x in proxies]

test_proxy(proxies, asia, speed_filter=5)

in_file = 'us.txt'
out_file = 'us_out.txt'

with open(in_file) as f:
    proxies = f.readlines()
proxies = [x.strip() for x in proxies]

us_isp = ['Google', 'Apple', 'Akamai Technologies', 'Amazon Technologies', 'Microsoft Corp']
test_proxy(proxies, ['US'], us_isp, speed_filter=20, speed_timeout=2)
