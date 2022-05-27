import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import pickle


co2_data = pd.read_csv("owid-co2-data.csv")
pan_co2 = co2_data.loc[co2_data["iso_code"] == "PAN"]
