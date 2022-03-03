import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import traceback


def replace_offences(X):
    if X not in ['THEFT UNDER',
                 'THEFT UNDER - BICYCLE', 'B&E', 'THEFT OF EBIKE UNDER $5000', 'PROPERTY - FOUND',
                 'THEFT FROM MOTOR VEHICLE UNDER',
                 "B&E W'INTENT", 'THEFT OVER', 'THEFT OVER - BICYCLE']:
        return 'Other offence'


def getsuburb(X):
    print(str(X.ObjectId2) + ' done')

    if 'suburb' not in allcols or not X['suburb']:
        locator = Nominatim(user_agent="myGeocoder")
        coordinates = str(X['Latitude']) + "," + str(X['Longitude'])
        location = locator.reverse(coordinates, timeout=None)

        if 'suburb' in location.raw['address']:
            return location.raw['address']['suburb']
        elif 'neighbourhood' in location.raw['address']:
            return location.raw['address']['neighbourhood']
        elif 'quarter' in location.raw['address']:
            return  location.raw['address']['quarter']
        elif 'city_district' in location.raw['address']:
            return location.raw['address']['city_district']
    else:
        return X



df = pd.read_csv('bicycleTheft_witharea.csv', sep=',')
allcols = df.columns
# df['Primary_Offence'] = df['Primary_Offence'].apply(replace_offences)
#
# df['Primary_Offence'].value_counts()
#

try:
    df['suburb'] = df.apply(getsuburb, axis=1)
except Exception as e:
    df.to_csv("bicycleTheft_witharea.csv")
    traceback.print_exc()

# df= df[df.Status != 'UNKNOWN']
df.to_csv("bicycleTheft_witharea.csv")
