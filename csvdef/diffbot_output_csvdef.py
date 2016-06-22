from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import pandas
from utils import SCRIPT_LOCATION

CSV_COLUMN_LIST = [
    "type",
    "pageUrl",
    "resolvedPageUrl",
    "title",
    "text",
    "brand",
    "offerPrice",
    "regularPrice",
    "shippingAmount",
    "saveAmount",
    "offerPriceDetails",
    "regularPriceDetails",
    "saveAmountDetails",
    "productId",
    "upc",
    "sku",
    "mpn",
    "isbn",
    "specs",
    "images",
    "url",
    "title",
    "height",
    "width",
    "naturalHeight",
    "naturalWidth",
    "primary",
    "xpath",
    "diffbotUri",
    "discussion",
    "prefixCode",
    "productOrigin",
    "humanLanguage",
    "diffbotUri",
    # Optional fields, available using fields=
    "links",
    "meta",
    "querystring",
    "breadcrumb",
    # The following fields are in an early beta stage:
    "availability",
    "colors",
    "normalizedSpecs",
    "multipleProducts",
    "priceRange",
    "minPrice",
    "maxPrice",
    "quantityPrices",
    "minQuantity",
    "price",
    "size",
]


def save_diffbot_output_data(data, output_filename):
    data_frame = pandas.DataFrame(data)
    stream_filename = output_filename

    data_frame.to_csv(
        stream_filename,
        columns=CSV_COLUMN_LIST,
        index=False,
        encoding="utf-8",
    )
