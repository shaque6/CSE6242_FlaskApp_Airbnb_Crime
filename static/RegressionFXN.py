from sklearn import linear_model
import sklearn.metrics as metrics
import pandas as pd
import os
import numpy as np
import statsmodels.api as sm
from statistics import mean

pd.options.display.max_columns = 100


def get_price(city, room_type, accommodates, bathrooms, beds, neighbourhood):
    # Read csv for specified city
    qw = pd.read_csv("./Data/{}-Listings-Clean-for-model.csv".format(city), dtype="unicode")

    # Convert data types as necessary
    qw['accommodates'] = qw['accommodates'].astype(int)
    qw['bathrooms_text'] = qw['bathrooms_text'].astype(float)
    qw['beds'] = qw['beds'].astype(int)
    qw['price'] = qw['price'].astype(float)

    # Create dummy variables for categorical feature data, and create df for response variable 'price'
    X = pd.get_dummies(qw[['room_type', 'accommodates', 'bathrooms_text', 'beds', 'neighbourhood_cleansed']],
                       drop_first=True)
    y = qw['price']
    X = sm.add_constant(X)

    # Create regression model and fit it to X and y
    regr = sm.OLS(y, X).fit()

    # Identify cook's distance
    np.set_printoptions(suppress=True)
    influence = regr.get_influence()
    cooks = influence.cooks_distance
    cooks_df = pd.Series(cooks[0])
    cooks_mean = cooks_df.mean()

    # Create new dataframe that eliminates any rows with cook's distance > 2 times mean cook's distance
    qw['cooks'] = cooks_df
    qw2 = qw.loc[qw['cooks'] < 2 * cooks_mean]

    # Repeate steps above to create new regression model for dataset with outliers removed

    # Create dummy variables for categorical feature data, and create df for response variable 'price'
    X2 = pd.get_dummies(qw2[['room_type', 'accommodates', 'bathrooms_text', 'beds', 'neighbourhood_cleansed']],
                        drop_first=True)
    y2 = qw2['price']
    X2 = sm.add_constant(X2)

    # Create regression model and fit it to X and y
    regr2 = sm.OLS(y2, X2).fit()

    # Create df for user inputs, to use for price prediction
    user_input = X.iloc[:0, :].copy()
    user_input['accommodates'] = [accommodates]
    user_input['bathrooms_text'] = [bathrooms]
    user_input['beds'] = [beds]
    if 'room_type_{}'.format(room_type) in user_input.columns:
        user_input['room_type_{}'.format(room_type)] = 1
    else:
        pass
    if 'neighbourhood_cleansed_{}'.format(neighbourhood) in user_input.columns:
        user_input['neighbourhood_cleansed_{}'.format(neighbourhood)] = 1
    else:
        pass
    user_input = user_input.fillna(0)

    # Predict price based upon user inputs
    price = regr.predict(user_input)[0]

    return price

if __name__ == "__main__":
    price = get_price('Boston', 'Entire home/apt', 2, 1, 1, 'East Boston')
