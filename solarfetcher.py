import googlemaps
from googlemaps import geocoding
import argparse
import http.client
import ssl
import json
import sys

def estimateKWH(panellist):
    numpanels=len(panellist)
    lowi=numpanels//3
    midi=numpanels//2
    highi=lowi*2
    alli=numpanels
    low=0.0
    mid=0.0
    high=0.0
    all=0.0
    for i in range(0, lowi):
        panel =panellist[i]
        low+=float(panel['yearlyEnergyDcKwh'])
    mid=low
    for i in range(lowi, midi):
        panel =panellist[i]
        mid+=float(panel['yearlyEnergyDcKwh'])
    high=mid
    for i in range(midi, highi):
        panel =panellist[i]
        high+=float(panel['yearlyEnergyDcKwh'])
    all=high
    for i in range(highi, alli):
        panel =panellist[i]
        all+=float(panel['yearlyEnergyDcKwh'])
    low*=0.85
    mid*=0.85
    high*=0.85
    all*=0.85
    return(low, mid, high, all)


def fetch_url(host, url, ssl_context):
    data=None
    try:
        conn=http.client.HTTPSConnection(host, context=ssl_context)
        conn.request("GET", url)
        response=conn.getresponse()
        if response.status==200:
            data=response.read()
    except http.client.HTTPException as e:
        print("HTTP error", e, url)
    except Exception as e:
        print("error", e, url)
    finally:
        if conn:
            conn.close()
        return data
       
     

def google_solar_data(latitude, longitude, key, ssl_context):
    host = "solar.googleapis.com"
    prefix_url="/v1/buildingInsights:findClosest?"
    final_url=prefix_url+"location.latitude="+str(latitude)+"&location.longitude="+str(longitude)+"&key="+key
    result=fetch_url(host, final_url, ssl_context)
    if result is None:
        return None
    d=json.loads(result)
    if 'solarPotential' in d and 'solarPanels' in d['solarPotential']:
        panellist=d['solarPotential']['solarPanels']
        numpanels=len(panellist)
        (low, mid, high, all)=estimateKWH(panellist)
        return (numpanels, low, mid, high, all)
    else:
        return None

def get_geo_data(address, client):
    address=address+" ,LEXINGTON, MA"
    result=geocoding.geocode(client, address=address)
    d=result[0]
    (lat, long) = (0, 0)
    if 'geometry' in d and 'location' in d['geometry']:
        ll=d['geometry']['location']
        if 'lat' in ll and 'lng' in ll:
            lat=ll['lat']
            long=ll['lng']
            return (lat, long)
        else:
            return None
    else:
        return None
    
    

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("-k", "--key", help="API Key for Geocoding", type=str, default="")
    parser.add_argument("-i", "--inputfile", help="Input File", type=str, default="uniqueaddresses.txt")
    parser.add_argument("-o", "--outputfile", help="Output File", type=str, default="solardata.txt")
    args=parser.parse_args()
    
    ssl_context=ssl._create_unverified_context()

    client=googlemaps.Client(key=args.key)

    with open(args.inputfile, "r") as f1:
        with open(args.outputfile, "w") as f2:
            for line in f1:
                line=line.strip()
                value=get_geo_data(line, client)
                if value is None:
                    continue
                (lat, lon)=value
                value=google_solar_data(lat, lon, args.key, ssl_context)
                if value is None:
                    continue
                (numpanels, low, mid, high, all)=value
                outputstring=format("%s %f %f %d %f %f %f %f\n" % (line, lat, lon, numpanels, low, mid, high, all))
                print(outputstring)               
                f2.write(outputstring)
                sys.stdout.flush()

    
    


