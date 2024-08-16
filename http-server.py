from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import argparse
import sys

class MyServer(BaseHTTPRequestHandler):
    solar_data = {}

    def setup(self):
        BaseHTTPRequestHandler.timeout=5
        BaseHTTPRequestHandler.setup(self)

    def do_GET(self):
        with open("startpage.html","r") as f:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            content=f.read()
            self.wfile.write(bytes(content, "utf-8"))
    
    def do_POST(self):
        content_length=int(self.headers['Content-Length'])
        post_data_bytes=self.rfile.read(content_length)

        post_data_str=post_data_bytes.decode("utf-8")
        list_of_post_data=post_data_str.split('&')

        post_data_dict={}
        for item in list_of_post_data:
            key, value = item.split('=')
            post_data_dict[key]=value.strip()
         
        key=post_data_dict['Number'].replace('+', ' ').strip() + ' '\
            +post_data_dict['Street'].replace('+', ' ').strip() + ' '\
            +post_data_dict['Suffix'].replace('+', ' ').strip()
        key=key.upper()
        print(key)
        sys.stdout.flush()
        address=key
        if key in self.solar_data:
            vals=self.solar_data[key]
            count=vals[2]
            coordinates=vals[0]+"/"+vals[1]
            low="{:,.0f}".format(float(vals[3]))
            mid="{:,.0f}".format(float(vals[4]))
            high="{:,.0f}".format(float(vals[5]))
            averagesq="{:,.0f}".format(float(count*7))
            lrgsq="{:,.0f}".format(float(count//2*21))
            aggrsq="{:,.0f}".format(float(count*14))

            plot_values=", ".join(vals[3:6])
            with open("mywebpage.html","r") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                content=f.read()
                content=content.replace('$LOW$',low)
                content=content.replace('$MID$',mid)
                content=content.replace('$HIGH$',high)
                content=content.replace('$ADDRESS$',address)
                content=content.replace('$VALUES$',str(plot_values))
                content=content.replace('$COORDINATES$',coordinates)
                content=content.replace('$AVERAGE$',str(count//3))
                content=content.replace('$LARGE$',str(count//2))
                content=content.replace('$AGGRESSIVE$',str(count//3*2))
                content=content.replace('$AVGSQFT$',averagesq)
                content=content.replace('$LRGSQFT$',lrgsq)
                content=content.replace('$AGGRSQFT$',aggrsq)
                self.wfile.write(bytes(content, "utf-8"))
        else:
            with open("errorpage.html","r") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                content=f.read()
                content=content.replace('$ADDRESS$',address)
                self.wfile.write(bytes(content, "utf-8"))
         


    def do_PUT(self):
        self.send500error()

    def do_HEAD(self):
        self.send500error()

    def do_DELETE(self):
        self.send500error()

    def send500error(self):
        self.send_respone(500)
        self.end_headers()
        self.wfile.write(bytes("Server nethod unavailable", "utf-8"))

def read_data(filename):
    data={}
    with open(filename, "r") as f:
        for line in f:
            parts=line.split('"')
            key= parts[1]
            index =key.find('#')
            if index !=-1:
                key=key[:index-1]
            values = parts[2].split()
            values[2]=int(values[2])
            for i in range(3, len(values)):
                values[i]="{:.0f}".format(float(values[i]))
            data[key]=values
    return data

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Domain to listen on", type=str, default="localhost")
    parser.add_argument("-p", "--port", help="Server Port", type=int, default=80)
    parser.add_argument("-f", "--file", help="File with solar data", type=str, default="solardata.txt.full")
    args=parser.parse_args()
    solar_data = read_data(args.file)

    MyServer.solar_data=solar_data
    webServer = ThreadingHTTPServer((args.domain, args.port), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    
if __name__=="__main__":
    main()
