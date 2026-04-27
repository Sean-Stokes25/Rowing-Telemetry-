from machine import UART,Pin,SPI
import time
import GPS_Parser #I wrote this
import math
import socket
import json
import time

#import ili9341
#from xglcd_font import XglcdFont

test = UART(2,9600, bits=8, parity=None, stop=1,rx=Pin(16))


#reads gps
def read_gps(gps_config,mode):
    line = ""
    while True:
        if gps_config.any():
            x = gps_config.read()
            if x:
                try:
                    line += x.decode("utf-8", "ignore")
                    if "\n" in line:  
                        if line.startswith("$GPRMC"):     #ensures valid nmea string
                            parsed = GPS_Parser.Parse_GPRMC(line)
                            if parsed.valid:
                                print(line)
                                if mode == "speed":
                                    return(parsed.speed("kmh"))
                                elif mode == "location":
                                    return(parsed.location())
                                else:
                                    print("Invalid Arg")
                       line = ""
                #error handling
                except UnicodeError:
                    if mode == "speed":
                        return None
                    elif mode == "location":
                        return(None,None)
                    else:
                        print("Invalid Arg")

#Changes kmh into split
def kmh_to_split(kmh):
    if kmh <= 0:
        return "99:99"  # avoid divide-by-zero

    seconds = (500 * 3.6) / kmh
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:.02d}"



#used to get distance between last updated location
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # metres
        
    # convert to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def get_data():
        # Replace this with your real GPS reading
        return {
            "speed": split,
            "distance": distance
        }



past_location = (None,None)

#Makes sure past_location gets a valid location 
while past_location == (None,None):
    past_location = read_gps(test,"location")
    time.sleep(0.2)

time.sleep(1)

distance = 0

#picks address
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#opens TCP socket
s = socket.socket()
s.bind(addr)
#Enter listening mode
s.listen(1)

print("Web server running on http://192.168.4.1")

while True:
    
    #Finds the speed
    speed = read_gps(test,"speed")
    #if its less than 2kmh its seen as noise
    if speed > 2:
        split = str(kmh_to_split(speed))
    else:
        split = "00:00"
    
    
    #gets location
    current_location = read_gps(test,"location")
   
    #debugging
    print("PAST:", past_location, type(past_location))
    print("CURR:", current_location, type(current_location))

    #gets distance traveled by comparing current location and past location
    movement = haversine(past_location[0],past_location[1],current_location[0],current_location[1])
    print(movement)
    
    #checks if youve actually moved or if its just noise
    if speed is not None and speed > 1.5 and movement > 2.0:
        distance += movement
    
    print(distance)
    print(split)
    past_location = current_location

    
    cl, addr = s.accept()
    request = cl.recv(1024).decode()

    def get_data():
       
        return {
            "speed": split,
            "distance": distance
        }
    
   
    if "/data" in request:
        # Return JSON data
        data = json.dumps(get_data())
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(data)
        cl.close()
        continue

    # Serve the main webpage
    html = """
HTTP/1.1 200 OK
Content-Type: text/html
<!DOCTYPE html>

<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {
        font-family: Arial, sans-serif;
        background: #f4f4f4;
        margin: 0;
        padding: 20px;
        color: #333;
      }
      .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        max-width: 400px;
        margin: auto;
      }
      h1 {
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
      }
      .row {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
        font-size: 18px;
      }
      .row:last-child {
        border-bottom: none;
      }
      .label {
        font-weight: bold;
      }
    </style>
  </head>

  <body>
    <div class="card">
      <h1>Live GPS Data</h1>

      <div class="row">
        <span class="label">Speed:</span>
        <span id="speed">0</span>
      </div>

      <div class="row">
        <span class="label">Distance:</span>
        <span id="distance">0</span>
      </div>
    </div>

    <script>
      function update() {
        fetch('/data')
          .then(r => r.json())
          .then(d => {
            document.getElementById('speed').innerText = d.speed;
            document.getElementById('distance').innerText = d.distance;
          });
      }
      update();
      setInterval(update, 1000);
    </script>
  </body>
</html>
"""

    cl.send(html)
    cl.close()

