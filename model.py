import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import pickle


co2_data = pd.read_csv("owid-co2-data.csv")
pan_co2 = co2_data.loc[co2_data["iso_code"] == "PAN"]


# Data preprocessing for annual CO2 emissions.
years_after_1989 = pan_co2["year"] >= 1990

co2_X, co2_y = (
    np.array(pan_co2["year"].loc[years_after_1989]).reshape(-1, 1),
    pan_co2["co2"].loc[years_after_1989],
)

co2_X_train, co2_X_test, co2_y_train, co2_y_test = train_test_split(
    co2_X, co2_y, test_size=0.2, random_state=42
)


# Create linear regression for annual CO2.
co2_linreg = make_pipeline(StandardScaler(), LinearRegression())
co2_linreg.fit(co2_X_train, co2_y_train)


# Export the model with pickle.

with open(r"pan_co2_linear_model.pkl", "wb") as model_file:
    pickle.dump(co2_linreg, model_file)
