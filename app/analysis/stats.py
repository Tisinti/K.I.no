import pandas as pd
from format import cutCovid

def getCutMedian():
    a, b = cutCovid()
    return a.median(), b.median()

