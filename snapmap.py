#!/usr/bin/env python3
# Inspired by https://github.com/1337r00t/SnapMap/ & https://github.com/CaliAlec/snap-map-private-api/
# Created by sc1341 to be used to search the snapmap from a given address 
# 
# 
import requests, time, argparse, os, json

from geopy.geocoders import Nominatim


def parse_args():
    parser = argparse.ArgumentParser(description="Instagram OSINT tool")
    parser.add_argument("--address", help="Address", required=True)
    parser.add_argument("--radius", help="Radius of area, default is 5000", required=False, default=5000, type=int)
    return parser.parse_args()


def address_to_coordinates(address):
	coords = Nominatim(user_agent="Map").geocode(address)
	return coords.latitude, coords.longitude

def download_contents(data):
	i = 0
	l = len(data["manifest"]["elements"])
	print(f"Downloading {l} media items")
	for value in data["manifest"]["elements"]:
		filetype = value["snapInfo"]["streamingThumbnailInfo"]["infos"][0]["thumbnailUrl"].split(".")[-1]
		with open(f"{i}.{filetype}", "wb") as f:
			f.write(requests.get(value["snapInfo"]["streamingThumbnailInfo"]["infos"][0]["thumbnailUrl"]).content)
		i += 1
		time.sleep(.5)


def export_json(data):
	filename = "snapmap_data.json"
	with open(filename, "w") as f:
		f.write(json.dumps(data))
	print(f"Wrote JSON data to file {filename}")

def getEpoch():
	return requests.post('https://ms.sc-jpl.com/web/getLatestTileSet',headers={'Content-Type':'application/json'},data='{}').json()['tileSetInfos'][1]['id']['epoch']


def main():
	args = parse_args()
	os.mkdir(args.address + "-Snap-map")
	os.chdir(args.address + "-Snap-map")
	lat, lon = address_to_coordinates(args.address)
	post_data = '{"requestGeoPoint":{"lat":'+str(lat)+',"lon":'+str(lon)+'},"tileSetId":{"flavor":"default","epoch":'+str(getEpoch())+',"type":1},"radiusMeters":'+str(args.radius)+'}'
	r = requests.post("https://ms.sc-jpl.com/web/getPlaylist", headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"},data=post_data)
	export_json(r.json())
	download_contents(r.json())

if __name__ == "__main__":
	main()



