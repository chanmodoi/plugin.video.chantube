import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import urllib, json
import requests
from lib import youtube

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])


addon	   = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
#xbmcgui.Dialog().ok(addonname, sys.argv[0], sys.argv[1], sys.argv[2])

args = urlparse.parse_qs(sys.argv[2][1:])


xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)


url = "https://dl.dropboxusercontent.com/u/44344736/data.json" 
response = urllib.urlopen(url);
data = json.loads(response.read())
#xbmc.log(str(data["catalogues"]))


if mode is None:
	for cat in data["catalogues"]:
		foldername=cat["name"].encode('utf-8')
		#xbmc.log(cat["name"].encode('utf-8'))
		url = build_url({'mode': 'folder', 'foldername': foldername, "id":str(cat["id"])})
		li = xbmcgui.ListItem(foldername, iconImage='DefaultFolder.png')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	#url = build_url({'mode': 'folder', 'foldername': 'Folder Two'})
	#li = xbmcgui.ListItem(url, iconImage='DefaultFolder.png')
	#xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
	#						   listitem=li, isFolder=True)

	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
	id=int(args.get('id', None)[0])
	for chan in data["catalogues"][id]["channels"]:
		#xbmc.log("chan:"+str(chan))
		#xbmc.log("chan ID:"+chan["id"])	
		url = build_url({'mode': 'view_list_videos', "id":chan["id"].encode('utf-8')})		
		li = xbmcgui.ListItem(chan["name"].encode('utf-8'))		
		xbmcplugin.addDirectoryItem(handle=addon_handle , url=url, listitem=li, isFolder=True)
elif mode[0] == 'view_list_videos':
	id = args.get('id', None)[0]
	links = youtube.getListVideos("https://www.youtube.com/"+id+"videos")
	#xbmc.log(str(html))
	for l in links:
		li = xbmcgui.ListItem(l.title)
		li.setThumbnailImage(l.img)
		url=build_url({'mode': 'view_link', "link":l.link})	
		xbmcplugin.addDirectoryItem(handle=addon_handle , url=url, listitem=li)
elif mode[0] == 'view_link':
	link = args.get('link', None)[0]
	links = youtube.getLinkFromKeepVid(link)
	xbmc.Player().play(links[0])			
	#xbmc.log(str(links))
	
xbmcplugin.endOfDirectory(addon_handle)