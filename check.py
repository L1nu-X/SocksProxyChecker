import requests, sys

check_url = 'https://coding.net/u/Katsue/p/check/git/raw/master/working.txt'

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

in_file = 'in.txt'
out_file = 'out.txt'

with open(in_file) as f:
    proxies = f.readlines()
proxies = [x.strip() for x in proxies]
bar = ProgressBar(total=len(proxies))
for proxy in proxies:
    socks = {
            'http': 'socks5://%s' % proxy,
            'https': 'socks5://%s' % proxy
    }
    try:
        if requests.get(check_url, timeout=15, proxies=socks).text == 'Works':
            open(out_file, 'a').write('%s\n' % proxy)
            bar.log('%s is working!' % proxy)
            bar.move(1)
    except Exception:
        bar.log('Oops, not working')
        bar.move(1)