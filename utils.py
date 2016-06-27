from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import collections
import csv
import os

from settings import settings

SCRIPT_LOCATION = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


CONF_CSV_QUOTING_MAP = {
    "minimal": csv.QUOTE_MINIMAL,
    "all": csv.QUOTE_ALL,
    "nonnumeric": csv.QUOTE_NONNUMERIC,
    "none": csv.QUOTE_NONE
}


def get_csv_quoting_conf():
    s = settings['csv']['quoting']
    return CONF_CSV_QUOTING_MAP[s]


def smart_true(v):
    return v.lower() in ('true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly')


def get_csv_conf():
    return {
        'sep': settings['csv']['separator'],
        'quoting': get_csv_quoting_conf(),
        'quotechar': settings['csv']['quotechar'],
        'doublequote': smart_true(settings['csv']['doublequote']),
        'escapechar': settings['csv']['escapechar'],
    }