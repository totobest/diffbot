from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import pandas

C_URL = "Url"

CSV_COLUMN_LIST = [
    C_URL,
]


def read_diffbot_input_data(input_filename):
    stream_filename = input_filename

    data = pandas.read_csv(
        stream_filename,
        encoding='utf-8',
        names=CSV_COLUMN_LIST,
        header=0,
        dtype=object,
        na_filter=False,
        parse_dates=False,
        error_bad_lines=True,
        converters={
        }
    )
    return data
