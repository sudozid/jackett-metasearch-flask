import pandas as pd
import requests
import json

apikey="" #enter api key here
domain="" #enter domain name here like http://jackett.example.com or http://120.120.120.120:9117


def indexerList(flag):
    r = requests.get(domain+"/api/v2.0/indexers/?apikey="+apikey)
    print(r)
    j = r.json()
    catList = []
    configuredIndexersList = []
    categoryList=[]
    indexers = pd.DataFrame.from_dict(j)

    for row in indexers.itertuples():
        if (row.configured == True):
            catList.append(row.caps)
            configuredIndexersList.append([row.id, row.name])
    maxCategory = max(catList, key=len)
    for x in range (0,len(maxCategory)):
        categoryList.append([maxCategory[x]['ID'], maxCategory[x]['Name']])

    #convert list of lists to list of tupples
    configuredIndexersList = [tuple(l) for l in configuredIndexersList]
    categoryList = [tuple(l) for l in categoryList]
    if flag==1:
        return categoryList
    if flag==2:
        return configuredIndexersList
    else:
        return [("error","error")]


def searchQuery(searchTerm,categoryList,indexerList):
    print(searchTerm)
    print(categoryList)
    print(indexerList)
    categoryList=",".join(categoryList)
    indexerList=",".join(indexerList)
    if(categoryList=="" and indexerList==""):
        r = requests.get(
            domain + "/api/v2.0/indexers/all/results?apikey=" + apikey + "&Query=" + searchTerm)
    elif(categoryList==""):
        r = requests.get(
            domain + "/api/v2.0/indexers/all/results?apikey=" + apikey + "&Query=" + searchTerm + "&Tracker[]=" + indexerList)
    elif(indexerList==""):
        r = requests.get(
            domain + "/api/v2.0/indexers/all/results?apikey=" + apikey + "&Query=" + searchTerm + "&Category[]=" + categoryList)
    else:
        r = requests.get(
            domain + "/api/v2.0/indexers/all/results?apikey=" + apikey + "&Query=" + searchTerm + "&Category[]=" + categoryList + "&Tracker[]="
            + indexerList)

    j=json.loads(r.text)
    #(j['Results'][0])
    resultsdf=pd.json_normalize(j['Results'])
    indexerdf=pd.json_normalize(j['Indexers'])
    if resultsdf.empty:
        return("Empty","No results found")

    resultsdf.drop(['FirstSeen','BlackholeLink','TrackerId','Guid','Category','Grabs','Description','RageID','TVDBId','Imdb','TMDb','Author','BookTitle','Poster','MinimumRatio','MinimumSeedTime','DownloadVolumeFactor','UploadVolumeFactor','Gain'],axis=1,inplace=True)

    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    for idx in resultsdf.index:
        torrenturl=resultsdf._get_value(idx,'Link')
        infohash = resultsdf._get_value(idx, 'InfoHash')
        magneturi = resultsdf._get_value(idx,'MagnetUri')
        if torrenturl is None:
            if magneturi is not None:
                resultsdf._set_value(idx,'Link',magneturi)
            elif infohash is not None:
                resultsdf._set_value(idx,'Link',"magnet:?xt=urn:btih:"+infohash.lower())
        torrenturl = resultsdf._get_value(idx, 'Link')
        resultsdf._set_value(idx,'Details',"<a href="+resultsdf._get_value(idx,'Details')+">Link</a>")
        resultsdf._set_value(idx,'Link',"<a href="+torrenturl+">Link</a>")
    resultsdf.drop(['MagnetUri','InfoHash'],axis=1,inplace=True)

    statusString=""
    for x in indexerdf.itertuples():
        if x.Status==2:
            statusString=statusString + x.Name + "(" + str(x.Results) + "), "
        if x.Status==1:
            statusString = statusString + x.Name + "('Error'), "


    statusString = statusString.rstrip(', ')
    return(resultsdf, statusString)