from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import pandas
import utils
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
    "offerPriceDetails.text",
    "offerPriceDetails.amount",
    "offerPriceDetails.symbol",
    "regularPriceDetails.text",
    "regularPriceDetails.amount",
    "regularPriceDetails.symbol",
    "saveAmountDetails.text",
    "saveAmountDetails.amount",
    "saveAmountDetails.symbol",
    "productId",
    "upc",
    "sku",
    "mpn",
    "isbn",
    "specs",
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
    "normalizedSpecs.brand",
    "normalizedSpecs.depth",
    "normalizedSpecs.height",
    "normalizedSpecs.shippingWeight",
    "normalizedSpecs.width",
    # "normalizedSpecs.brand.cleanLiteral",
    # "normalizedSpecs.depth.unit",
    # "normalizedSpecs.depth.value",
    # "normalizedSpecs.depth.cleanLiteral",
    # "normalizedSpecs.height.unit",
    # "normalizedSpecs.height.value",
    # "normalizedSpecs.height.cleanLiteral",
    # "normalizedSpecs.shippingWeight.unit",
    # "normalizedSpecs.shippingWeight.value",
    # "normalizedSpecs.shippingWeight.cleanLiteral",
    # "normalizedSpecs.width.unit",
    # "normalizedSpecs.width.value",
    # "normalizedSpecs.width.cleanLiteral",
    "multipleProducts",
    "priceRange.minPrice",
    "priceRange.maxPrice",
    "quantityPrices.minQuantity",
    "quantityPrices.price",
    "size",
    "imageUrl1",
    "imageUrl2",
    "imageUrl3",
    "imageUrl4",
    "imageUrl5",
]


def save_diffbot_output_data(data, output_filename):
    data_frame = pandas.DataFrame(data)
    stream_filename = output_filename

    csv_conf = utils.get_csv_conf()

    data_frame.text.replace(to_replace=csv_conf['sep'], value=" ", inplace=True, regex=True)
    data_frame.text.replace(to_replace='\n', value=" ", inplace=True, regex=True)
    data_frame.to_csv(
        stream_filename,
        columns=CSV_COLUMN_LIST,
        index=False,
        encoding="utf-8",
        **csv_conf
    )
