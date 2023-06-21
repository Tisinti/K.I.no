import time

import requests

from MovieSearch import MovieSearch
import timeit
import pandas as pd
from datetime import datetime


def str_to_date(string):
    return datetime.strptime(string, '%d.%m.%y').date()


if __name__ == "__main__":
    requests.Session()
    print(MovieSearch("Call me by your name").most_likely_movie)
