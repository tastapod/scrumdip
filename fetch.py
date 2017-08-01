import re

import requests
from threading import Thread
from collections import deque

DIRECTORY_URL = 'https://www.scrumalliance.org/community/certificant-directory.aspx'

CERT_COUNT_RE = re.compile(r'Displaying results \d+-\d+ \(of (\d+)\)')

CERTS = [
    'csm', 'csd', 'csp', 'cspo', 'cst', 'ctc', 'cec',
    'advcsm', 'advcspo', 'cspsm', 'csppo', 'educator', 'rep', 'author'
]

PARAMS = dict(
    firstname='',
    lastname='',
    email='',
    location='',
    company='',
    page=1,
    orderby='',
    sortdir=''
)


def extract_count(html):
    match = CERT_COUNT_RE.search(html)
    return int(match.group(1)) if match is not None else 0


def get_page(cert):
    cert_flags = dict((k, k == cert) for k in CERTS)
    args = PARAMS.copy()
    args.update(cert_flags)
    return requests.post(DIRECTORY_URL, params=args)


def get_count(cert):
    res = get_page(cert)
    return extract_count(res.text) if res.ok else 0


def get_all_counts():
    results = deque()
    threads = []

    def run(cert):
        print("Going after " + cert)
        count = get_count(cert)
        print("{} has {} people".format(cert, count))
        results.append((cert, count))

    for cert in CERTS:
        print("Starting thread for " + cert)
        t = Thread(name=cert, target=run, args=(cert,))
        t.start()
        threads.append(t)

    print("Waiting for threads")
    for t in threads:
        t.join()
        print("Thread {} finished".format(t.name))

    # At this point all the answers are in the results queue
    return list(results)


if __name__ == '__main__':
    print(get_all_counts())
