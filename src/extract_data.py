import requests

# (E)TL
def extract_data(url):
  try:
    response = requests.get(url).json()
    neo = response['near_earth_objects']
    return neo
  except Exception as e:
    print(e)