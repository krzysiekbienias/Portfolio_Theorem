import numpy as np
import pandas as pd


def portfolioValue(weights,positions):
    value=0
    for i in range(len(weights)):
        value+=weights[i]*positions[i]
    return value
