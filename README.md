# restaurant search api
This is a quick exercise for a restaurant search API

This is an API that can be used to search for restaurants from a JSON file.

The end point is  /restaurants/search?q=Keyword&lat=latitude&lon=longitude
example: http://localhost:8000/restaurants/search/?q=sushi&lat=60.17045&lon=24.93147 


# To run the App on your machine. 
1. make sure to have python 3.5 or above. 

2. install dependancies using 

```pip install -r requirements.txt```


3. once Django is installed use the following command to run the server


`python3 manage.py runserver`

4. now go to http://localhost:8000/restaurants/search/?q=sushi&lat=60.17045&lon=24.93147


