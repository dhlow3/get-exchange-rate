# -*- coding: utf-8 -*-
"""Get exchange rate fro Google and Fixer.io."""
import json
import os
import requests

from datetime import datetime
from lxml import html


def get_google_rate(pair):
    """Get exchange rate from Google by parsing a webpage for a span class.

    Parameters
    ----------
    pair: list
        A single currency pair with the base currency at index zero.

    Returns
    ----------
    google_rate: float
        The exchange rate from the base currency to the target currency.
    """
    assert isinstance(pair, list)

    page = requests.get(
        'https://finance.google.com/finance/converter'
        '?a=1&from={}&to={}'.format(pair[0], pair[1])
    )

    tree = html.fromstring(page.content)
    google_rate = tree.xpath('//span[@class="bld"]/text()')[0].split(' ')[0]
    google_rate = float(google_rate)

    return google_rate


def get_fixer_rate(pair):
    """Get exchange rate from fixer.io by parsing json on a webpage.

    Parameters
    ----------
    pair: list
        A single currency pair with the base currency at index zero.

    Returns
    ----------
    fixer_rate: float
        The exchange rate from the base currency to the target currency.
    """
    assert isinstance(pair, list)

    page = ('https://api.fixer.io/latest'
            '?symbols={},{}&base={}'.format(pair[0], pair[1], pair[0]))

    r = requests.get(page)
    j = json.loads(r.text)
    fixer_rate = j['rates'][pair[1]]

    return fixer_rate


def main():
    # Directory is relative to the location of this script
    MAIN_DIR = os.path.dirname(__file__)
    OUTPUT = os.path.join(MAIN_DIR, 'exchange_rate.txt')

    # Delete output file if it exists
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)

    # If there is an error getting rate fro Google, get rate from fixer.io
    try:
        # Get rates from google
        USD_CAD = get_google_rate(['USD', 'CAD'])
        CAD_USD = get_google_rate(['CAD', 'USD'])
        source = 'google'

    except Exception:
        # On exception get rates from fixer
        USD_CAD = get_fixer_rate(['USD', 'CAD'])
        CAD_USD = get_fixer_rate(['CAD', 'USD'])
        source = 'fixer'

    # Store values in dict
    d = {'date': datetime.today().strftime('%Y%m%d'),
         'USD_CAD': USD_CAD,
         'CAD_USD': CAD_USD,
         'source': source}

    # Write values to output file
    with open(OUTPUT, 'w') as f:
        f.write('{}\t{}\t{}\t{}'.format(
                d['date'], d['USD_CAD'], d['CAD_USD'], d['source']))


if __name__ == '__main__':
    main()
