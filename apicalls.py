import requests
import json

def getVehicleInfo(plate):
    apiUrl = "https://opendata.rdw.nl/resource/m9d7-ebf2.json?kenteken="
    rawData = requests.get(apiUrl + plate)
    return rawData.text

def getFuelInfo(plate):
    apiUrl = "https://opendata.rdw.nl/resource/8ys7-d773.json?kenteken="
    rawData = requests.get(apiUrl + plate)
    return rawData.text