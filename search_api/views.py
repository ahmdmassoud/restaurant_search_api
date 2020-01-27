from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
import json
import math

# default response for any requests that does not match the main query
def default(request):
    return HttpResponse("PLEASE USE THE END POINT /restaurants/search/?q=[[keyword]]&lat=[[latitude]]&lon=[[longitude],example: /restaurants/search/?q=sushi&lat=60.17045&lon=24.93147 ", content_type='application/json', status=400)


# The main view for the API end point
def search(request):
    if request.method == 'GET':
        if extract_paramters(request):
            try:
                q, lon, lat = extract_paramters(request)
                results = json.dumps(extract_restaurants(q, lat, lon))
                return HttpResponse(results, content_type='application/json', status=200)
            except:
                return redirect('default')
        else:
            return redirect('default')
    else:
        return redirect('default')


# helper functions

# This function opens the JSON file parse it in a variable and return it.
def read_Json_file(filename):
    try:
        json_data = open(filename)
        data1 = json.load(json_data)
        json_data.close()
    except:
        data1 = None
    return data1


# This function checks for the get paramters in the url if they are not empty and returns them else it returns none
def extract_paramters(request):
    if(request.GET.get('q') is not None and 
       len(request.GET.get('q')) > 0 and
       request.GET.get('lon') is not None and
       request.GET.get('lat') is not None):
        try:
            q = str(request.GET.get('q'))
            lon = float(request.GET.get('lon'))
            lat = float(request.GET.get('lat'))
            return q, lon, lat
        except:
            return None
    else:
        return None


# this function calculates the distance between 2 points
def distance_calc(lat1, lon1, lat2, lon2):
    R = 6371  # earth mean radius in KM
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2-lat1)
    delta_lambda = math.radians(lon2-lon1)
    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(phi1) * \
        math.cos(phi2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

# checks the distance between 2 points and retruns true if it is less than 3 KM
def check_distance_closer3km(lat1, lon1, lat2, lon2):
    return True if distance_calc(lat1, lon1, lat2, lon2) < 3 else False


# opens the json file
# check  each restaurant for the keyword q if it is found
# it checks the distance if it is less than 3 Km
# if it passes then it adds it to the output array
def extract_restaurants(q, lat, lon):
    restaurants = read_Json_file('restaurants.json')
    selected_restaurants = []
    for restaurant in restaurants["restaurants"]:
        if q in restaurant["description"] or q in restaurant["name"] or q in restaurant["tags"]:
            if check_distance_closer3km(float(restaurant["location"][1]), float(restaurant["location"][0]), lat, lon):
                selected_restaurants.append(restaurant)
    return selected_restaurants

