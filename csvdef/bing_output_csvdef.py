from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import pandas
from utils import SCRIPT_LOCATION

C_QUERY = "Query"
C_ID = "ID"
C_TITLE = "Title"
C_DESCRIPTION = "Description"
C_DISPLAY_URL = "DisplayUrl"
C_URL = "Url or Media URL (if media query for instance)"

CSV_COLUMN_LIST = [
    C_QUERY,
    C_ID,
    C_TITLE,
    C_DESCRIPTION,
    C_DISPLAY_URL,
    C_URL,
]


def save_bing_output_data(data, output_filename):
    data_frame = pandas.DataFrame(data, columns=CSV_COLUMN_LIST)
    stream_filename = output_filename

    data_frame.to_csv(
        stream_filename,
        columns=CSV_COLUMN_LIST,
        index=False,
        encoding="utf-8",
    )
