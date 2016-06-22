from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import collections
import logging
import os
from functools import partial
from operator import is_not

import diffbot
from csvdef.diffbot_input_csvdef import read_diffbot_input_data
from settings import settings
from csvdef import diffbot_input_csvdef
from csvdef.diffbot_output_csvdef import save_diffbot_output_data
from tqdm import tqdm

diffbot_client = diffbot.Client(token=settings['diffbot']['token'])

log = logging.getLogger(__name__)


def diffbot_product(url):
    return diffbot_client.product(
        url,
        fields=[
            "links",
            "meta",
            "querystring",
            "breadcrumb"
        ],
        discussion=False
    )


def flatten_dict(d, parent_key='', sep='_'):
    if d is None:
        return {}
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def diffbot2csv(diffbot_object):

    base = {
        'type': diffbot_object.get('type'),
        'pageUrl': diffbot_object.get('pageUrl'),
        'resolvedPageUrl': diffbot_object.get('resolvedPageUrl'),
        'title': diffbot_object.get('title'),
        'text': diffbot_object.get('text'),
        'brand': diffbot_object.get('brand'),
        'offerPrice': diffbot_object.get('offerPrice'),
        'regularPrice': diffbot_object.get('regularPrice'),
        'shippingAmount': diffbot_object.get('shippingAmount'),
        'saveAmount': diffbot_object.get('saveAmount'),
        'offerPriceDetails': diffbot_object.get('offerPriceDetails'),
        'regularPriceDetails': diffbot_object.get('regularPriceDetails'),
        'saveAmountDetails': diffbot_object.get('saveAmountDetails'),
        'productId': diffbot_object.get('productId'),
        'upc': diffbot_object.get('upc'),
        'sku': diffbot_object.get('sku'),
        'mpn': diffbot_object.get('mpn'),
        'isbn': diffbot_object.get('isbn'),
        'specs': diffbot_object.get('specs'),
        'discussion': diffbot_object.get('discussion'),
        'prefixCode': diffbot_object.get('prefixCode'),
        'productOrigin': diffbot_object.get('productOrigin'),
        'humanLanguage': diffbot_object.get('humanLanguage'),
        'diffbotUri': diffbot_object.get('diffbotUri'),
        # Optional fields, available using fields=
        'links': diffbot_object.get('links'),
        'meta': flatten_dict(diffbot_object.get('meta')),
        'querystring': diffbot_object.get('querystring'),
        # 'breadcrumb': diffbot_object.get('breadcrumb'),
        # The following fields are in an early beta stage:
        'availability': diffbot_object.get('availability'),
        'colors': diffbot_object.get('colors'),
        'normalizedSpecs': diffbot_object.get('normalizedSpecs'),
        'multipleProducts': diffbot_object.get('multipleProducts'),
        'priceRange.minPrice': diffbot_object.get('priceRange.minPrice'),
        'priceRange.maxPrice': diffbot_object.get('priceRange.maxPrice'),
        'quantityPrices.minQuantity': diffbot_object.get('quantityPrices.minQuantity'),
        'quantityPrices.price': diffbot_object.get('quantityPrices.price'),
        'minQuantity': diffbot_object.get('minQuantity'),
        'price': diffbot_object.get('price'),
        'size': diffbot_object.get('size'),
    }

    if diffbot_object.get('images') is not None:
        image_list = map(lambda image_obj: {
            'url': image_obj.get('url'),
            'title': image_obj.get('title'),
            'height': image_obj.get('height'),
            'width': image_obj.get('width'),
            'naturalHeight': image_obj.get('naturalHeight'),
            'naturalWidth': image_obj.get('naturalWidth'),
            'primary': image_obj.get('primary'),
            'xpath': image_obj.get('xpath'),
            'diffbotUri': image_obj.get('diffbotUri'),
        }, diffbot_object.get('images'))

    base = flatten_dict(diffbot_object)
    return base


def process_bing_output(row_index, row):

    url = row.loc[diffbot_input_csvdef.C_URL]
    log.info("Processing row={} url={}".format(row_index, url))
    diffbot_json = diffbot_product(url)
    try:
        diffbot_object = diffbot_json['objects'][0]
    except KeyError:
        log.warn("URL {} yields to not result from Diffbot".format(url))
        return None
    diffbot_dict = diffbot2csv(diffbot_object)
    return diffbot_dict

import argparse

parser = argparse.ArgumentParser(description='Diffbot API to CSV')
parser.add_argument('-i', '--input', required=True,
                    help="CSV file that contains URLs.")
parser.add_argument('-o', '--output', required=True,
                    help="CSV file to write results to.")


def main():

    logging.basicConfig(
        filename='{}.log'.format(os.path.basename(__file__)),
        level=logging.DEBUG
    )

    args = parser.parse_args()
    input_filename = args.input
    output_filename = args.output

    bing_output_data = read_diffbot_input_data(input_filename)
    log.info("Read {} URLs.".format(len(bing_output_data)))

    diffbot_result_list = [
        process_bing_output(row_index, row) for (row_index, row) in tqdm(list(bing_output_data.iterrows()))
    ]
    save_diffbot_output_data(list(filter(partial(is_not, None), diffbot_result_list)), output_filename)


if __name__ == "__main__":
    main()
