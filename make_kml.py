"""
Traverse current folder and all subfolders to make KML file of all flight tracks
"""
import os
import simplekml

kml = simplekml.Kml()
linestrings = {}
folders = {}
subfolders = {}

for root, dirs, files in os.walk(os.getcwd()):
    this_folder = os.path.basename(root)
    for name in files:
        if name.endswith('.csv') and name.startswith('data_'):
            print(this_folder)
            if this_folder not in folders:
                folders[this_folder] = kml.newfolder(name=this_folder)
                subfolders = {}
                linestrings = {}
            this_file_name = os.path.join(root,name)
            print(this_file_name)
            with open(this_file_name) as f:
                for this_line in f:
                    #print(this_line.strip())
                    fields = this_line.strip().split(',')
                    if len(fields)!=7:
                        continue
                    #print(fields)
                    if len(fields[5])==0:
                        continue
                    else:
                        lon = float(fields[5])
                    if len(fields[4])==0:
                        continue
                    else:
                        lat = float(fields[4])
                    if len(fields[3])==0:
                        continue
                    else:
                        altitude = float(fields[3])*0.3048
                    hexident = fields[0]
                    if hexident not in subfolders:
                        subfolders[hexident] = folders[this_folder].newfolder(name=hexident)
                        linestrings[hexident] = {}
                    callsign = fields[6]
                    if callsign not in linestrings[hexident]:
                        linestrings[hexident][callsign] = subfolders[hexident].newlinestring(name=callsign,
                                                                                             coords=[(lon,
                                                                                                      lat,
                                                                                                      altitude)])
                        linestrings[hexident][callsign].altitudemode = simplekml.AltitudeMode.absolute
                        linestrings[hexident][callsign].linestyle.color = simplekml.Color.rgb(0,
                                                                                              int(255 - altitude*255/15000),
                                                                                              int(altitude*255/15000))
                    else:
                        linestrings[hexident][callsign].coords.addcoordinates([(lon,
                                                                       lat,
                                                                       altitude)])
kml.save('adsb.kml')
