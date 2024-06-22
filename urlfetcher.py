#!/usr/bin/env python3

import http.client
from urllib.parse import urlparse
import ssl
from bs4 import BeautifulSoup
import re
import argparse

initial_urls=[
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=1',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=2',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=3',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=4',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=5',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=6',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=7',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=8',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=9',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=A',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=B',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=C',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=D',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=E',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=F',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=G',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=H',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=I',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=J',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=K',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=L',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=M',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=N',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=O',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=P',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=R',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=S',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=T',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=U',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=V',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=W',
'https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=Y'
]

def fetch_url(host, url, ssl_context):
    conn=http.client.HTTPSConnection(host, context=ssl_context)
    conn.request("GET", url)
    response=conn.getresponse()
    data=None
    if response.status==200:
        data=response.read()
    conn.close()
    return(data)

def extract_streets(page):
    streets=[]
    soup=BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a', attrs={'href': re.compile(r"^Streets.aspx\?Name=")}):
        streets.append(str(link.get('href')))
    return streets

def extract_parcels(page):
    parcels=[]
    soup=BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a', attrs={'href': re.compile(r"^Parcel.aspx\?pid=")}):
        parcels.append(str(link.get('href')))
    return parcels

def extract_address(page):
    soup=BeautifulSoup(page, 'html.parser')
    obj= soup.find(id='MainContent_lblLocation')
    address=obj.text
    address=address.strip()
    if address.startswith(tuple("0123456789")):
        return [address]
    else:
        return []



if __name__=='__main__':  
    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="File to write", type=str, default="addresses.txt")
    args =parser.parse_args()
    ssl_context=ssl._create_unverified_context()
    all_streets = []
    for initial_url in initial_urls:
        obj=urlparse(initial_url)
        host=obj.hostname
        path=obj.path+'?'+obj.query
        data=fetch_url(host, path, ssl_context)    
        streets=extract_streets(data)
        all_streets += streets

    print("Finished Initial URLs")
    all_parcels = []
    for street in all_streets:
        street_url='https://gis.vgsi.com/lexingtonma/'+street.replace(' ', '%20')
        obj=urlparse(street_url)
        host=obj.hostname
        path=obj.path+'?'+obj.query
        data=fetch_url(host, path, ssl_context)
        parcels=extract_parcels(data)
        all_parcels += parcels
   
    print("Finished all streets")
    count = 0
    all_addresses = []
    for parcel in all_parcels:
        parcel_url='https://gis.vgsi.com/lexingtonma/'+parcel.replace(' ', '%20')
        obj=urlparse(parcel_url)
        host=obj.hostname
        path=obj.path+'?'+obj.query
        data=fetch_url(host, path, ssl_context)
        address=extract_address(data)
        all_addresses += address
        count += 1
        if count % 100 == 0:
            print("Got address from parcel %s\n" % (parcel))

    with open(args.file, "w") as f:
        for address in all_addresses:
            f.write(address+'\n')
    

    