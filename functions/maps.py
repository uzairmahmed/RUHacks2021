import googlemaps

key = "AIzaSyCRkKthGv2FIGs6JG6OD67Nd1ZXVfZwNkM"

gmaps = googlemaps.Client(key = key)

def streetAndMapsView(locationName):
    query = locationName.replace(" ", "+")
    urlMap = "https://maps.googleapis.com/maps/api/staticmap?center="+query+"&markers="+query+"&size=600x600&key="+key
    urlStreetView = "https://maps.googleapis.com/maps/api/streetview?size=600x600&location="+query+"&key="+key
    return urlMap, urlStreetView

def placeInfo(locationName):
    placeResult  = gmaps.find_place(input=locationName, input_type = "textquery", fields=['rating','opening_hours','formatted_address'])
    return placeResult

name = "Cineplex Dundas"
urlMap, urlStreetView = streetAndMapsView(name)
placeResult = placeInfo(name)
print("map view is: "+urlMap)
print("street view is: "+urlStreetView)
print(placeResult.items())
