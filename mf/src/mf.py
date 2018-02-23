#import json
import math
import re
import pylast
import argparse
from collections import defaultdict
#import mysql.connector
#from mysql.connector import errorcode

#config = {
#    'user': 'root',
#    'password' : 'bike',
#    'host' : '127.0.0.1', #FIXME
#    #'port' : 8123,
#    'database' : 'mdb'
#}

N          = 10
topperiod  = '1month'
taglimit   = 5
user       = 'leperboi'
playlist   = []

API_KEY = 'REDACTED'
API_SECRET = 'REDACTED'

#TODO tag/similar weight to allow


network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
userobj = network.get_user(user)
#library = pylast.Library(user=user,network=network)

topArt  = userobj.get_top_artists(period=topperiod, limit=N)
recent  = userobj.get_recent_tracks(limit=N)

tags    = defaultdict(float)
simart  = []
simtrk  = []

for i in range(1,N):
    if topArt[i]:
        #weight check
        simart += topArt[i].item.get_similar()
        for at in topArt[i].item.get_top_tags(limit=taglimit):
            tags[at.item.name+' count'] += 1
            tags[at.item.name] += float(at.weight)/100
    if recent[i]:
        #weight check
        simtrk += recent[i].track.get_similar()
        for rt in recent[i].track.get_top_tags(limit=taglimit):
            tags[rt.item.name+' count'] += 1
            tags[rt.item.name] += float(rt.weight)/100

#for sa in simart:
#    if any(sa.item.name == x.item.artist for x in simtrk):
#        continue
#    else:
#        for t in sa.get_top_tags(limit=int(N/10)):

f = open('out','w+')
#for k,v in sorted(tags, key=tags.get, reverse=True):
for k,v in sorted(tags.items()):
    if re.match(".* count$", k):
        pass
    elif v/tags[k+' count'] > tags[k+' count']/2 and tags[k+' count'] != v:
        print(str(k) + ' : ' + str(v))
        f.write(str(k) + ' : ' + str(v))
    else:
        tags.pop(k)
        tags.pop(k+' count')

for k,v in sorted(tags.items()):
    if re.match(".* count$", k):
        pass
    else:
        f.write(str(k)+' : '+str(v))
        tag = network.get_tag(k)
        for art in tag.get_top_artists(limit=15):
            #if any(art.item.name == x.item.name for x in simart) or \
            #   any(art.item.name == x.item.artist for x in simtrk):
            #    continue
            tagscore = 0
            for at in art.item.get_top_tags(limit=taglimit):
                if at.item.name in tags.keys():
                    tagscore += tags[at.item.name]
            if tagscore >= math.ceil(taglimit/2):
                simart += art

print('hello')
for i in simart:
    if not any(i.item.name == x.item.name for x in topArt):
        f.write(str(i.item.name))
        print(str(i.item.name))
    else:
        f.write('X '+str(i.item.name))
        print('X '+str(i.item.name))
for i in simtrk:
    if not any(i.item== x.track for x in recent):
        f.write(str(i.item.name))
        print(str(i.item.name))
    else:
        f.write('X '+str(i.item.name))
        print('X '+str(i.item.name))

#try:
#    con = mysql.connector.connect(**config)
#    cursor = con.cursor()
#    cursor.execute('SELECT * FROM MDB.TEST')
#    row = cursor.fetchone()
#    while row is not None:
#        f.write(row)
#        row = cursor.fetchone()
#except mysql.connector.Error as e:
#    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#        f.write("creds are no go")
#    elif e.errno == errorcode.ER_BAD_DB_ERROR:
#        f.write("db is no go")
#    else:
#        f.write(e)
#else:
#    f.write('nice')
#    con.close()

f.write('finished')
f.close()
