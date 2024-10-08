# solarlex
Repository for the code to calculate Lexington's solar potential

The first step to building the website was to create a file containing
all the addresses in Lexington. I did this by using the http client
python library and the beautiful soup library to fetch and parse the
contents of this website:
https://gis.vgsi.com/lexingtonma/Streets.aspx?Letter=1. This website
contains almost all of the addresses in Lexington, although there are
a few quirks in it that will have to be solved later. I then took all
the addresses I had fetched and wrote them into a new file called
addresses.txt. The code for this part of the process is in
urlfetcher.py.

The next step was to clean up the file by making sure to get rid of
duplicates and sort the file. After that, I had to use Google's
geocoding API in order to find the latitude and longitude coordinates
for each address. Then using Google's solar API, I utilized the
coordinates found from before to search through Google's solar data
and then loaded the results into a JSON string. From there I could
find the data for solar potential of each address and extract it. I
finished by writing the addresses with their new data into a file
called solardata.txt. After editing the file a little bit to account
for duplicates and other formatting problems that came from the
website the addresses were on, the final file I was using was
solardata.txt.full.

The final step of this process was creating the website. Using html
code, I created three different pages. One page only contains the form
to enter an address, called startpage.html. errorpage.html contains
the same content as the start page but an error message is added at
the bottom, telling the user the address they typed in was not
found. Finally, mywebpage.html has the results found from whatever
address the user entered. It has a few placeholders that are replaced
with the actual data of whatever address was inputted, as well as a
graph that was written using java script. The code to run the server
is found in http-server.py. When it is run, whenever it receives an
address, it will check if it is found within solardata.txt.full. If
not, it will send back the error page. If it is found, then the code
will go through the data for that address and assign them to a
variable called vals. I can then replace the placeholders in the html
page with the actual values from my data, and the webpage will now
display it.
