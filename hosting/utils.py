import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from geopy import distance
from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib

CNtower = [43.642567, -79.387054]

def getDistance(input_distance):
    coordinates_to = [input_distance['Latitude'], input_distance['Longitude']]
    distance_geopy = distance.distance(CNtower, coordinates_to).km
    # print('distance using geopy: ', distance_geopy)

    distance_geopy_great_circle = distance.great_circle(CNtower, coordinates_to).km
    # print('distance using geopy great circle: ', distance_geopy_great_circle)
    return round(distance_geopy_great_circle, 4)


def replace_division(div):
    if div in ['D14', 'D52', 'D51', 'D53', 'D55']:
        return div
    else:
       return 'Others'

def replace_neighbourhood(neighbourhood):
    if neighbourhood in ['Waterfront Communities-The Island (77)', 'Bay Street Corridor (76)',
                         'Church-Yonge Corridor (75)', 'Niagara (82)', 'Annex (95)']:
        return neighbourhood
    else:
       return 'Others'

def replace_premises(prem):
  if prem in ['Outside', 'Apartment', 'House', 'Commercial', 'Other']:
        return prem
  else:
       return 'Other'

def replace_location(loc):
  if loc in ['Apartment (Rooming House, Condo)', 'Streets, Roads, Highways (Bicycle Path, Private Road)',
              'Single Home, House (Attach Garage, Cottage, Mobile)', 'Parking Lots (Apt., Commercial Or Non-Commercial)',
              'Other Commercial / Corporate Places (For Profit, Warehouse, Corp. Bldg']:
        return loc
  else:
       return 'Others'

def replace_make(make):
  if make in ['OT', 'UK', 'GI', 'OTHER', 'TR']:
        return make
  else:
       return 'OTHER'

def replace_model(model):
  if model in ['UNKNOWN', 'HYBRID', 'ESCAPE', 'SIRRUS', 'MOUNTAIN BIKE']:
        return model
  else:
        return 'Others'


def modify_biketype(input_type):
    if input_type in ['MT', 'RG', 'OT', 'RC', 'EL']:
        return input_type
    else:
        return 'Others'


def modify_bikecolour(color):
    if color in ['BLK', 'BLU', 'GRY', 'WHI', 'RED']:
        return color
    else:
        return 'Others'
# In[372]:

def modify_month(month):
    if month in ['January', 'February', 'March', 'April', 'May', 'June']:
        return "First Half"
    else:
        return "Second Half"


class NumericalTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, cols):
        self.cols = cols

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X.loc[:, 'distance_from_cn'] = X.apply(getDistance, axis=1)
        X.loc[:, 'Cost_of_Bike'] = X.loc[:, 'Cost_of_Bike'].replace(0, X.loc[:, 'Cost_of_Bike'].median())
        self.cols.append('distance_from_cn')
        return X[['Bike_Speed', 'Cost_of_Bike', 'distance_from_cn']]


class CategoricalTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, cols):
        self.cols = cols

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X.loc[:, 'Division'] = X.loc[:, 'Division'].apply(replace_division)
        X.loc[:, 'NeighbourhoodName'] = X.loc[:, 'NeighbourhoodName'].apply(replace_neighbourhood)
        X.loc[:, 'Premises_Type'] = X.loc[:, 'Premises_Type'].apply(replace_premises)
        X.loc[:, 'Location_Type'] = X.loc[:, 'Location_Type'].apply(replace_location)
        X.loc[:, 'Bike_Make'] = X.loc[:, 'Bike_Make'].apply(replace_make)
        X.loc[:, 'Bike_Model'] = X.loc[:, 'Bike_Model'].apply(replace_model)
        X.loc[:, 'Bike_Type'] = X.loc[:, 'Bike_Type'].apply(modify_biketype)
        X.loc[:, 'Bike_Colour'] = X.loc[:, 'Bike_Colour'].apply(modify_bikecolour)
        X.loc[:, 'Report_Month'] = X.loc[:, 'Report_Month'].apply(modify_month)
        X.loc[:, 'Occurrence_Month'] = X.loc[:, 'Occurrence_Month'].apply(modify_month)

        return X[self.cols]
