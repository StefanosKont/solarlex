from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse

def read_data(filename):
    data={}
    with open(filename, "r") as f:
        for line in f:
            print(line)
            parts=line.split('"')
            key= parts[1]
            index =key.find('#')
            if index !=-1:
                key=key[:index-1]
            values = parts[2].split()
            for i in range(3, len(values)):
                values[i]="{:.2f}".format(float(values[i]) /1000.0)
            data[key]=values
    return data

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Domain to listen on", type=str, default="localhost")
    parser.add_argument("-p", "--port", help="Server Port", type=int, default=80)
    parser.add_argument("-f", "--file", help="File with solar data", type=str, default="solardata.txt.full")
    args=parser.parse_args()
    solar_data = read_data(args.file)
    print(solar_data)
    
if __name__=="__main__":
    main()
