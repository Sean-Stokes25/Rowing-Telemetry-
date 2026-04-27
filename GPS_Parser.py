
def cleanup(input_string):
    #removes all un-printable ascii characters
    input_string = input_string.replace("\n","")
    input_string = input_string.replace("\r","")
    input_string = ''.join(ch for ch in input_string if 32 <= ord(ch) <= 126) 
   
    return input_string.strip()
    

#Function that gets the checksum value manually by XOR-ing all asciis values of string from (not including)$ to *
def calc_checksum(input_string):
    
    if input_string[:1] == "$":
        check_string = input_string[1:input_string.find("*")]
        check_sum = 0
        for char in check_string:
            check_sum ^= ord(char)
       
        return check_sum
    else:
        return 0

class Parse_GPRMC:
    def __init__(self,gps_input):
        
        gps_input = cleanup(gps_input)  #removes white space
         
        
        #compares hex value at end of string to hex value from validate function if they are eqaul the GPRMC string is not corrupt
        if calc_checksum(gps_input) == int(gps_input[gps_input.find('*')+1:gps_input.find('*')+3],16):
            self.valid = True
                
            gps_input = cleanup(gps_input)
            
            comma_position = []
            #gets index position of all commas in the string as that is how data is seprated
            for i,char in enumerate(gps_input):
                if char == ",":
                    comma_position.append(i)
            
            #Parses data from the string using comma_position
            #All values are strings
            self.TalkerID = gps_input[0:comma_position[0]]
            self.Timestamp = gps_input[comma_position[0]+1:comma_position[1]]
            self.Status = gps_input[comma_position[1]+1:comma_position[2]]
            self.Lat = gps_input[comma_position[2]+1:comma_position[3]]
            self.NS = gps_input[comma_position[3]+1:comma_position[4]]
            self.Long = gps_input[comma_position[4]+1:comma_position[5]]
            self.EW = gps_input[comma_position[5]+1:comma_position[6]]
            self.SOG = gps_input[comma_position[6]+1:comma_position[7]]
            self.COG = gps_input[comma_position[7]+1:comma_position[8]]
            self.Date = gps_input[comma_position[8]+1:comma_position[9]]
            self.MagVar = gps_input[comma_position[9]+1:comma_position[10]]
            self.MagVarDir = gps_input[comma_position[10]+1:comma_position[11]]
            self.Mode = gps_input[comma_position[11]+1:gps_input.find("*")]
            self.CheckSum = gps_input[gps_input.find("*"):]
        else:
           self.valid = False

    #speed over ground is in knots this function converts speed unit depending on arg
    def speed(self,unit):
        if not self.SOG:
            return 0
        if unit == "kmh":
            return float(self.SOG) * 1.852
        elif unit ==  "knots":
            return float(self.SOG)
        elif unit ==  "ms":
            return float(self.SOG) * 0.514444
        else:
            sys.exit(f"Invalid argument {unit}")
    #returns cordinates  
    def location(self):
        
        if not self.Lat or not self.Long:
            return (None,None)
            
        
        lat_degrees = str(self.Lat[:2])
        lat_minutes = str(self.Lat[2:])
        
        long_degrees = str(self.Long[:3])
        long_minutes = str(self.Long[3:])
        
        if self.NS == "N":
            latitude = (float(lat_degrees) + (float(lat_minutes)/60))
        else:
            latitude = (-float(lat_degrees) -(float(lat_minutes)/60))
        if self.EW == "E":
            longitude = (long_degrees + long_minutes)
        else:
            longitude = (-float(long_degrees) - (float(long_minutes)/60))
        
        return (latitude,longitude)
        
    #returns degrees from true north(course over ground)
    def direction(self):
        return(self.COG)
    
    
    
class Parse_GPGGA:
    
    def __init__(self,gps_input):
        gps_input = cleanup(gps_input)
        
        if calc_checksum(gps_input) == int(gps_input[gps_input.find('*')+1:gps_input.find('*')+3],16):
            self.valid = True
            
            comma_position = []
            #gets index position of all commas in the string as that is how data is seprated
            for i,char in enumerate(gps_input):
                if char == ",":
                    comma_position.append(i)
            
            #All values are strings
            self.TalkerID = gps_input[0:comma_position[0]]
            self.UTC = gps_input[comma_position[0]+1:comma_position[1]]
            self.Lat = float(gps_input[comma_position[1]+1:comma_position[2]])
            self.NS = gps_input[comma_position[2]+1:comma_position[3]]
            self.Long = float(gps_input[comma_position[3]+1:comma_position[4]])
            self.EW = gps_input[comma_position[4]+1:comma_position[5]]
            self.GPSQual = gps_input[comma_position[5]+1:comma_position[6]]
            self.Sats = int(gps_input[comma_position[6]+1:comma_position[7]])
            self.HDOP = gps_input[comma_position[7]+1:comma_position[8]]
            self.Altitude = gps_input[comma_position[8]+1:comma_position[9]]
            self.AltitudeVal = gps_input[comma_position[9]+1:comma_position[10]]
            self.GeoSep = gps_input[comma_position[10]+1:comma_position[11]]
            self.GeoVal = gps_input[comma_position[11]+1:comma_position[12]]
            self.DGPSRef = gps_input[comma_position[12]+1:gps_input.find("*")]
            self.Checksum = gps_input[gps_input.find("*"):]
        else:
            self.valid = False
            
    def location(self):
        latdegrees = str(self.Lat)[:2]
        latmin = str(self.Lat/60)[2:4]
        latsec = str(self.Lat/3600)[4:]
        lat_dd = latdegrees+latmin+latsec
        
        longdegrees = str(self.Long)[:2]
        longmin = str(self.Long/60)[2:4]
        longsec = str(self.Long/3600)[4:]
        long_dd = longdegrees+longmin+longsec
        
        return(lat_dd,long_dd)
    
class Parse_GPVTG:

    def __init__(self,gps_input):
        gps_input = cleanup(gps_input)
        
        if calc_checksum(gps_input) == int(gps_input[gps_input.find('*')+1:gps_input.find('*')+3],16):
            self.valid = True
            
            comma_position = []
            #gets index position of all commas in the string as that is how data is seprated
            for i,char in enumerate(gps_input):
                if char == ",":
                    comma_position.append(i)
            
            self.TalkerID = gps_input[0:comma_position[0]]
            self.Course = gps_input[comma_position[0]+1:comma_position[1]]
            self.Refrence = gps_input[comma_position[1]+1:comma_position[2]]
            self.Degrees = gps_input[comma_position[2]+1:comma_position[3]]
            self.SOG = gps_input[comma_position[3]+1:comma_position[4]]
            self.kn = gps_input[comma_position[4]+1:comma_position[5]]
            self.SOGkmh = gps_input[comma_position[5]+1:comma_position[6]]
            self.kmh =gps_input[comma_position[6]+1:comma_position[7]]
            self.Mode = gps_input[comma_position[7]+1:gps_input.find("*")]
            self.Checksum = gps_input[gps_input.find("*"):]
        else:
            self.valid = False
            
    def speed(self,unit):
        if not self.SOG:  #if there is no sog value in string
            return None
        if unit == "kmh":
            return float(self.SOG) * 1.852
        elif unit ==  "knots":
            return float(self.SOG)
        elif unit ==  "ms":
            return float(self.SOG) * 0.514444
        else:
            sys.exit(f"Invalid argument {unit}")
            
class Parse_GPGLL:
    
    def __init__(self,gps_input):
        gps_input = cleanup(gps_input)
        if calc_checksum(gps_input) == int(gps_input[gps_input.find('*')+1:gps_input.find('*')+3],16):           
            self.valid = True
            
            comma_position = []
            #gets index position of all commas in the string as that is how data is seprated
            for i,char in enumerate(gps_input):
                if char == ",":
                    comma_position.append(i)

            self.TalkerID = gps_input[0:comma_position[0]]
            self.Lat = gps_input[comma_position[0]+1:comma_position[1]]   
            self.NS = gps_input[comma_position[1]+1:comma_position[2]]
            self.Long = gps_input[comma_position[2]+1:comma_position[3]]
            self.EW = gps_input[comma_position[3]+1:comma_position[4]]
            self.UTC = gps_input[comma_position[4]+1:comma_position[5]]
            self.Status = gps_input[comma_position[5]+1:comma_position[6]]
            self.Mode = gps_input[comma_position[0]+1:gps_input.find("*")]
            self.Checksum = gps_input[gps_input.find("*"):]
        else:
            self.valid = False
    
    
    def location(self):
        latdegrees = str(self.Lat)[:2]
        latmin = str(self.Lat/60)[2:4]
        latsec = str(self.Lat/3600)[4:]
        lat_dd = latdegrees+latmin+latsec
        
        longdegrees = str(self.Long)[:2]
        longmin = str(self.Long/60)[2:4]
        longsec = str(self.Long/3600)[4:]
        long_dd = longdegrees+longmin+longsec
        
        return(lat_dd,long_dd)            
    
class Parse_GPGSA:
   
    
    def __init__(self,gps_input):
        gps_input = cleanup(gps_input)
        
        if calc_checksum(gps_input) == int(gps_input[gps_input.find('*')+1:gps_input.find('*')+3],16):
            self.valid = True
            
            comma_position = []
            #gets index position of all commas in the string as that is how data is seprated
            for i,char in enumerate(gps_input):
                if char == ",":
                    comma_position.append(i)
            
            self.TalkerID = gps_input[0:comma_position[0]]
            self.Mode1 = gps_input[comma_position[0]+1:comma_position[1]]
            self.Mode2 = gps_input[comma_position[1]+1:comma_position[2]] 
            self.IDs = []
            self.IDs = [gps_input[x+1:x+3] if x+1 < len(gps_input) and gps_input[x+1] != "," else "" for x in comma_position[3:14]]
                                
            self.PDOP = gps_input[comma_position[13]+1:comma_position[14]]
            self.HDOP = gps_input[comma_position[14]+1:comma_position[15]]
            self.VDOP = gps_input[comma_position[15]+1:gps_input.find("*")]
            self.Checksum = gps_input[gps_input.find("*"):]
        else:
            self.valid = False
