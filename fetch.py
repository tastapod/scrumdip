import re

import requests

'''
https://www.scrumalliance.org/community/certificant-directory.aspx
?firstname=
&lastname=
&email=
&location=
&company=
&csm=False
&csd=True
&csp=False
&cspo=False
&cst=False
&ctc=False
&cec=False
&advcsm=False
&advcspo=False
&cspsm=False
&csppo=False
&educator=False
&rep=False
&author=False
&page=1
&orderby=
&sortdir=
'''

DIRECTORY_URL = 'https://www.scrumalliance.org/community/certificant-directory.aspx'

SEARCH = re.compile(r'Displaying results \d+-\d+ \(of (\d+)\)')

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


def extract_total(html):
    '''scan html for total value'''
    match = SEARCH.search(html)
    return int(match.group(1)) if match is not None else 0


def get_page(cert):
    cert_flags = dict((k, k == cert) for k in CERTS)
    args = PARAMS.copy()
    args.update(cert_flags)
    return requests.post(DIRECTORY_URL, params=args)


def get_total(cert):
    r = get_page(cert)
    return extract_total(r.text) if r.ok else 0


if __name__ == '__main__':
    print(', '.join(CERTS))
    cert = input("Enter certificate type: ")
    print(cert, get_total(cert))
