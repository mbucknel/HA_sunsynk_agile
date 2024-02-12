import sys
import requests
import json
import datetime
from requests.auth import HTTPBasicAuth
#loginurl = ('https://api.sunsynk.net/oauth/token')
# API call to get realtime inverter related information
#plant_id_endpoint = ('https://api.sunsynk.net/api/v1/plants?page=1&limit=10&name=&status=')
#plant_id_endpoint = ('https://api.sunsynk.net/api/v1/plant/262605?lan=en&id=262605')
#plant_rate_update = ('https://api.sunsynk.net/api/v1/plant/262605/income')
@service
def octoagile(my_user_email=None, my_user_password=None, chargerate=0.20, dischargerate=0.50, serialno=000000, region=2 ):
    global loginurl
    loginurl = ('https://api.sunsynk.net/oauth/token')
    # API call to get realtime inverter related information
    global plant_id_endpoint
    global plant_rate_update
    global payload
    plant_id_endpoint = ('https://api.sunsynk.net/api/v1/plant/262605?lan=en&id=262605')
    plant_rate_update = ('https://api.sunsynk.net/api/v1/plant/262605/income')
    payload = {"username": my_user_email, "password": my_user_password, "grant_type":"password", "client_id":"csp-web"}
    """hello_world example using pyscript."""
    log.info(f"octoagile: user {my_user_email} pass {my_user_password} charge rate {chargerate} discharge {dischargerate}")
    headers = {
    'Content-type':'application/json', 
    'Accept':'application/json'
    }
    #raw_data = requests.post(loginurl, json=payload, headers=headers).json()
    raw_data = task.executor(requests.post, loginurl, json=payload, headers=headers).json()
    # Your access token extracted from response
    my_access_token = raw_data["data"]["access_token"]
    global the_bearer_token_string
    the_bearer_token_string = ('Bearer '+ my_access_token)
    log.info(f"octoagile: bearer {the_bearer_token_string} ")
    # Build out the request to update the settings
    headers_and_token = {
    'Content-type':'application/json', 
    'Accept':'application/json',
    'Authorization': the_bearer_token_string
    }
    p = {"id":serialno,"currency":366,"invest":12000,"charges":[{"price":0,"type":"3","startRange":"","endRange":""}],"products":[{"direction":1,"ratesThreshold":round(chargerate*100,2),"provider":1,"regionId":region},{"direction":0,"ratesThreshold":round(dischargerate*100,2),"provider":1,"regionId":2}]}
    #r = requests.get(plant_id_endpoint, headers=headers_and_token)
    log.info(f"octoagile: p data = {p} ")
    r = task.executor(requests.post, plant_rate_update,data=json.dumps(p), headers=headers_and_token)
    log.info(f"octoagile: r data = {r} ")
    return r
