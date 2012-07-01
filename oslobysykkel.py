import collections
import urllib.request, urllib.error, urllib.parse
from xml.dom.minidom import parseString
import html.parser

last_rack = 111

Rack = collections.namedtuple("Rack", "description latitude longitude online bikes locks")

def get_racks():
    url = "http://smartbikeportal.clearchannel.no/public/mobapp/maq.asmx/getRacks"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode()
    dom = parseString(data.replace("&gt;", ">").replace("&lt;", "<"))

    racks = []
    for a in dom.firstChild.childNodes:
        if a.nodeType != a.ELEMENT_NODE:
            continue

        racks.append(int(a.firstChild.data))

    return racks

def get_rack(rack_id):
    url = "http://smartbikeportal.clearchannel.no/public/mobapp/maq.asmx/getRack?id=%d" % rack_id

    with urllib.request.urlopen(url) as f:
        data = f.read()

    dom = parseString(data)
    xml_string = dom.getElementsByTagName("string")[0].toxml()

    data = html.parser.HTMLParser().unescape(xml_string).replace("&", " og ")
    dom = parseString(data)
    dom_station = dom.getElementsByTagName("station")[0]

    try:
        description = "-".join(dom_station.getElementsByTagName("description")[0].firstChild.nodeValue.split("-")[1:]).strip()
        locks = int(dom_station.getElementsByTagName("empty_locks")[0].firstChild.nodeValue)
        bikes = int(dom_station.getElementsByTagName("ready_bikes")[0].firstChild.nodeValue)
    except:
        raise IndexError("No such rack")

    latitude = 0
    longitude = 0
    online = False

    try:
        latitude = float(dom_station.getElementsByTagName("latitude")[0].firstChild.nodeValue)
        longitude = float(dom_station.getElementsByTagName("longitute")[0].firstChild.nodeValue)
        online = bool(dom_station.getElementsByTagName("online")[0].firstChild.nodeValue)
    except:
        pass

    return Rack(description, latitude, longitude, online, bikes, locks)


if __name__ == "__main__":
    print("  F   L")
    for rack in get_racks():
        try:
            r = get_rack(rack)
        except IndexError:
            print("SKIPPED! --> ", rack)
            continue

        print("{2:3d} {3:3d}   {1} ({0})".format(rack, r.description, r.bikes, r.locks))
