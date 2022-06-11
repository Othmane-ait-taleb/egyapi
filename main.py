from egybest import *
from flask import *
from waitress import serve
import os
import copy
import json,time

eb = EgyBest("https://egy.best")


def requestSeasons(show):
    seasons = show.getSeasons()

    for i in range(len(seasons)):

        print(seasons[i].title)
        episodes = seasons[i].getEpisodes()


        for j in range(len(episodes)):

            print(episodes[j].title)
            downloadSources = episodes[j].getDownloadSources()

            for src in downloadSources:
                print(str(src.quality) + ' p '+src.link)

def requestSpesficSeason(show,s,anime):
    print("you are ther ")

    seasons = show.getSeasons()
    data={}
    data['Seasontitle']=seasons[s].title
    data["epsds"]=[]
    if anime is True:
        episodes = seasons[s].getAnimeEpisodes()
    else :
        episodes = seasons[s].getEpisodes()

    for j in range(len(episodes)):


        print(episodes[j].title)
        downloadSources = episodes[j].getDownloadSources()

        for src in downloadSources:
            data["epsds"].append({"EpsdName":[episodes[j].title],"quality":str(src.quality),"link":src.link})
            #print(str(src.quality) + ' p ' + src.link)
    print(data)
    print(json.dumps(data))
    return data

def allResultforSearch(name):
    data={}
    data['info']=[]
    results = eb.search(name, includeMovies=True, includeShows=True)
    if len(results) > 0:
        for res in results:
            data['info'].append({"tile":res.title,"poster":res.posterURL,"rating":res.rating})
    return data

app = Flask(__name__)

@app.route('/show/',methods=['GET'])
def give_me_show():
    results = eb.search(str(request.args.get('name')), includeMovies=False, includeShows=True)

    if len(results) > 0:
        result = results[0]
        isShow = isinstance(result, Show)
        if isShow:
            return json.dumps(requestSpesficSeason(result,int(request.args.get('season'))-1,anime=False), ensure_ascii = False)
        else:
            return json.dumps({"err":"wyah"})


@app.route('/anime/',methods=['GET'])
def give_me_anime():
    results = eb.search(str(request.args.get('name')), includeMovies=False, includeShows=True)

    if len(results) > 0:
        result = results[0]
        isShow = isinstance(result, Show)
        if isShow:
            return json.dumps(requestSpesficSeason(result,int(request.args.get('season'))-1,anime=True), ensure_ascii = False)


@app.route('/movie/',methods=['GET'])
def home_page():
    results = eb.search(str(request.args.get('name')), includeMovies=True, includeShows=False)
    if len(results) > 0:
        result = results[0]

    downloadSources = result.getDownloadSources()
    data={}
    data["link__quality"]=[]
    for src in downloadSources:
        data["link__quality"].append({"quality":str(src.quality) + ' p ',"link":src.link})
    return json.dumps(data)


if __name__ == "__main__":
	serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))





