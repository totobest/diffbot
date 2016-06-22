from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import itertools
import logging

from settings import settings

from csvdef import bing_input_csvdef, bing_output_csvdef
from csvdef.bing_input_csvdef import read_bing_input_data
from csvdef.bing_output_csvdef import save_bing_output_data
from py_bing_search import PyBingWebSearch
import os
from tqdm import tqdm

from utils import SCRIPT_LOCATION

log = logging.getLogger(__name__)


def bing_search(search_term):
    latitude = settings['bing'].get('latitude')
    longitude = settings['bing'].get('longitude')
    custom_params = {
        # 'Sources': "'" + settings['bing']['sources'] + "'",
        'Market': "'" + settings['bing']['market'] + "'",
    }
    if latitude is not None and longitude is not None:
        custom_params.update({
            'Latitude': latitude,
            'Longitude': longitude,
        })

    custom_params_str = "".join(["&" + k + "=" + v for k, v in iter(custom_params.items())])
    bing_web = PyBingWebSearch(
        settings['bing']['api_key'],
        search_term,
        web_only=False,
        custom_params=custom_params_str,
    )
    # web_only is optional, but should be true to use your web only quota instead of your all purpose quota
    return bing_web.search(limit=int(settings['bing']['results_limit']), format='json')


def convert_to_data_frame(query, bing_result):

    convert_dict = {
        bing_output_csvdef.C_QUERY: query,
        bing_output_csvdef.C_ID: bing_result.id,
        bing_output_csvdef.C_TITLE: bing_result.title,
        bing_output_csvdef.C_DESCRIPTION: bing_result.description,
        bing_output_csvdef.C_DISPLAY_URL: bing_result.url,
        bing_output_csvdef.C_URL: bing_result.url,
    }

    return convert_dict


def process_bing_result(search_term, bing_result):

    df = convert_to_data_frame(search_term, bing_result)
    return df


def process_bing_input(bing_input_row):
    search_term = bing_input_row.loc[bing_input_csvdef.C_QUERY]
    bing_results = bing_search(search_term)

    res = [process_bing_result(search_term, bing_result) for bing_result in bing_results]
    return res


import argparse

parser = argparse.ArgumentParser(description='Bing API to CSV')
parser.add_argument('-i', '--input', required=True,
                    help="CSV file that contains search terms.")
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

    bing_input_data = read_bing_input_data(input_filename)
    log.info("Read {} search terms.".format(len(bing_input_data)))
    bing_results_list = [process_bing_input(row) for (_, row) in tqdm(list(bing_input_data.iterrows()))]

    # flatten the list
    bing_results = list(itertools.chain.from_iterable(bing_results_list))

    save_bing_output_data(bing_results, output_filename)


if __name__ == "__main__":
    main()
