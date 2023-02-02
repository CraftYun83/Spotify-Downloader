from requests_html import HTMLSession
import os, threading
import bs4

headers = {
    'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
}

s = HTMLSession()
response = s.get("https://open.spotify.com/playlist/37i9dQZF1DX6bnzK9KPvrz", headers=headers)
response.html.render()

soup = bs4.BeautifulSoup(response.content, "html.parser")
results = soup.findAll("div", {"data-testid" : "track-row"})

albumInfo = {
    "name": soup.findAll("h1")[0].text,
    "songs": []
}

for song in results:
    albumInfo["songs"].append({
        "name": song.findAll("a")[0].text,
        "artist": song.findAll("a")[1].text,
    })

removedName = ''.join(e for e in albumInfo["name"] if e.isalnum())

if (not os.path.exists(removedName)):
    os.mkdir(removedName)

os.chdir(removedName)

def downloadThread(song):
    os.system(f'youtube-dl -x "ytsearch1:{song["name"]} by {song["artist"]}"')

for song in albumInfo["songs"]:

    threading.Thread(target=downloadThread, args=(song,)).start()

response.close()

s.close()