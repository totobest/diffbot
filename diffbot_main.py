from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import collections
import logging
import os
import urllib
import uuid
from functools import partial
from operator import is_not
from time import sleep

import diffbot
from csvdef.diffbot_input_csvdef import read_diffbot_input_data
from settings import settings
from csvdef import diffbot_input_csvdef
from csvdef.diffbot_output_csvdef import save_diffbot_output_data
from tqdm import tqdm
import requests

diffbot_client = diffbot.Client(token=settings['diffbot']['token'])

log = logging.getLogger(__name__)


def diffbot_bulk_create(url_list):
    bulk_job_id = "{}".format(uuid.uuid4()).replace('-', '')[:30]

    data_dict = {
        "token": settings['diffbot']['token'],
        "name": bulk_job_id,
        "urls": " ".join(url_list),
        "apiUrl": "http://api.diffbot.com/v3/product?fields=links,meta,querystring,breadcrumb",
     }
    data_str = urllib.parse.urlencode(data_dict)
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post("http://api.diffbot.com/v3/bulk", data=data_str, headers=headers)
    response_json = response.json()
    if response_json['response'] != "Successfully added urls for spidering.":
        raise Exception("Cannot create Bulk job.")

    return bulk_job_id


def diffbot_bulk_get_details(bulk_job_id):
    params = {
        "token": settings['diffbot']['token'],
        "name": bulk_job_id,
     }
    response = requests.get("http://api.diffbot.com/v3/bulk", params=params)

    response_json = response.json()
    jobs = response_json["jobs"]
    if len(jobs) > 0:
        return jobs[0]
    else:
        raise Exception("Bulk Job not found")


def diffbot_bulk_get_data(bulk_job_id):
    params = {
        "token": settings['diffbot']['token'],
        "name": bulk_job_id,
        "format": "json"
     }
    response = requests.get("http://api.diffbot.com/v3/bulk/data", params=params)

    return response.json()


def flatten_dict(d, parent_key='', sep='.'):
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

    base = flatten_dict(diffbot_object)

    images = diffbot_object.get('images')
    if images is not None:
        image_kv_list = [("imageUrl{}".format(index + 1), image_obj.get('url')) for index, image_obj in enumerate(images)]

        base.update(dict(image_kv_list))

    return base


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

    url_list = [row.loc[diffbot_input_csvdef.C_URL] for _, row in bing_output_data.iterrows()]
    bulk_job_id = diffbot_bulk_create(url_list)
    pbar = tqdm(total=len(url_list))
    done = 0
    while True:
        ret = diffbot_bulk_get_details(bulk_job_id)
        successes = ret['pageProcessSuccessesThisRound']
        if successes - done > 0:
            pbar.update(successes - done)
            done = successes
        message = ret['jobStatus']['message']
        pbar.set_description(message)
        status = ret['jobStatus']['status']
        if status == 9:
            break
        if status in [5, ]:
            raise Exception("Job did not succeed.")
        sleep(1)

    pbar.set_description("Getting result data.")
    diffbot_result_list = diffbot_bulk_get_data(bulk_job_id)
    diffbot_flatten_result_list = list(map(diffbot2csv, filter(partial(is_not, None), diffbot_result_list)))
    pbar.set_description("Writing output file.")
    save_diffbot_output_data(diffbot_flatten_result_list, output_filename)


if __name__ == "__main__":
    main()
