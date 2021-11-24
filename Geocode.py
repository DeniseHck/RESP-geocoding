#import all necessary libraries
import geopy
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from csv import reader

def geocode(filename):
    
    """
    Define a function that parses through a list of place names an returns 
    coordinates via geopy Python package.
    
    Input:
    -----------
    filename: .csv
        a file that contains a list of place names
        
    Output:
    -----------
    lista: .csv
        a csv of place names and their coordinates ready to be loaded in qgis.
        
    """
    data = pd.read_csv(filename) 

    # open file in read mode
    with open(filename, 'r') as read_obj:
       
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        
        #skip first 2 lines (title and blank)
        next(csv_reader, None)

        lista=[[], []]
        
        #parse through each row
        for row in read_obj:

            geolocator = Nominatim(user_agent="my_app")
            location = geolocator.geocode(row, timeout=10000)

            if location == None:
                lista[0].append("None")
                lista[1].append("None")
            else:
                lista[0].append(location.latitude)
                lista[1].append(location.longitude)
    
    #create 2 new dataframe columns
    data["latitude"] = pd.Series(lista[0])
    data["longitude"] = pd.Series(lista[1])
    
    #drop empty columns
    data.dropna(how='all', axis=1, inplace=True)
    print(data)

    data.to_csv (r'lista.csv', index = False, header=True)
    
if __name__ == "__main__":
  geocode("AC_list.csv")
  
  
#Aberdeen is in Hong Kong...
#Amisfield is in NZ...
#etc.
