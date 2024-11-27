import pandas as pd
from format import cut_covid

def getCutMedian():
    a, b = cut_covid()
    return a.median(), b.median()

