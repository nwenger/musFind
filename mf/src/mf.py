#import json
import math
import re
import pylast
#import argparse
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

N          = 50
topperiod  = '1month'
taglimit   = 5
user       = 'leperboi'
playlist   = []

API_KEY = 'REDACTED'
API_SECRET = 'REDACTED'

#TODO tag/similar weight to accept


network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
userobj = network.get_user(user)
library = pylast.Library(user=user,network=network)
allArt  = library.get_artists(limit=None)

topArt  = userobj.get_top_artists(period=topperiod, limit=N)
recent  = userobj.get_recent_tracks(limit=N)

tags    = defaultdict(float)
simart  = []
simtrk  = []

print('[LOG] This will take a while')
for i in range(0,N-1):
    #parallelize A
    if len(topArt) >= i:
        #weight check
        simart += [ a.item for a in topArt[i].item.get_similar() \
                    if not any(a.item.name == x.item.name for x in allArt) ]
        for at in topArt[i].item.get_top_tags(limit=taglimit):
            tags[at.item.name+' count'] += 1
            tags[at.item.name] += float(at.weight)/100
    #parallelize A
    if len(recent) >= i:
        #weight check
        simtrk += recent[i].track.get_similar()
        for rt in recent[i].track.get_top_tags(limit=taglimit):
            tags[rt.item.name+' count'] += 1
            tags[rt.item.name] += float(rt.weight)/100

#for sa in simart:
#    if any(sa.item.name == x.item.artist for x in simtrk):
#        #adjust weight
#        continue
#    else:
#        for t in sa.get_top_tags(limit=int(N/10)):

log = open('out','w+')
#for k,v in sorted(tags, key=tags.get, reverse=True):
for k,v in sorted(tags.items()):
    if re.match(".* count$", k):
        pass
    #FIXME
    elif v/tags[k+' count'] > tags[k+' count']/2 and tags[k+' count'] != v:
        #print(str(k) + ' : ' + str(v))
        log.write(str(k) + ' : ' + str(v))
    else:
        tags.pop(k)
        tags.pop(k+' count')

for k,v in sorted(tags.items()):
    if re.match(".* count$", k):
        pass
    else:
        log.write(str(k)+' : '+str(v))
        tag = network.get_tag(k)
        for art in tag.get_top_artists(limit=N):
            #if any(art.item.name == x.item.name for x in simart) or \
            #   any(art.item.name == x.item.artist for x in simtrk):
            #    continue
            tagscore = 0
            for at in art.item.get_top_tags(limit=taglimit):
                if at.item.name in tags.keys():
                    tagscore += tags[at.item.name]
            if tagscore >= 0:#math.ceil(taglimit/2):
                #FIXME inconsistent typing in simart
                simart += art

print('\n=== Finished retrieving similar artists ===\n')

print('\n=== simart ===\n')
#parallelize B
#TODO check for 0x90 "nil state"
for i in simart:
    try:
        if any(i.name == x.item.name for x in allArt):
            #log.write('XX '+str(i.item.name))
            #print('XX '+str(i.item.name))
            continue
        if not any(i.name == x.item.name for x in topArt):
            log.write(str(i.name))
            print(str(i.name))
        else:
            pass
            #log.write('X '+str(i.item.name))
            #print('X '+str(i.item.name))
    except AttributeError:
        print('[LOG] Wrong var type, retrying...')
        try:
            if any(i.item.name == x.item.name for x in allArt):
                continue
            if not any(i.item.name == x.item.name for x in topArt):
                log.write(str(i.item.name))
                print(str(i.item.name))
            print('[LOG] Retry successful')
        except AttributeError:
            print('[ERR] I give up : '+str(i))
print('\n=== simtrk ===\n')
#parallelize B
for i in simtrk:
    try:
        if any(i.item.artist == x.item.name for x in allArt):
            #log.write('XX '+str(i.item.name))
            #print('XX '+str(i.item.name))
            pass
        elif not any(i.item.name == x.track.name for x in recent):
            log.write(str(i.item.name))
            print(str(i.item.name))
        else:
            pass
            #log.write('X '+str(i.item.name))
            #print('X '+str(i.item.name))
    except AttributeError:
        print('[LOG] Wrong var type, retrying...')
        try:
            if any(i.artist == x.item.name for x in allArt):
                #log.write('XX '+str(i.name))
                #print('XX '+str(i.name))
                pass
            elif not any(i.name == x.track.name for x in recent):
                log.write(str(i.name))
                print(str(i.name))
            else:
                pass
                #log.write('X '+str(i.item.name))
                #print('X '+str(i.item.name))
            print('[LOG] Retry successful')
        except AttributeError:
            print('[ERR] I give up : '+str(i))

#try:
#    con = mysql.connector.connect(**config)
#    cursor = con.cursor()
#    cursor.execute('SELECT * FROM MDB.TEST')
#    row = cursor.fetchone()
#    while row is not None:
#        log.write(row)
#        row = cursor.fetchone()
#except mysql.connector.Error as e:
#    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#        log.write("creds are no go")
#    elif e.errno == errorcode.ER_BAD_DB_ERROR:
#        log.write("db is no go")
#    else:
#        log.write(e)
#else:
#    log.write('nice')
#    con.close()

log.write('[LOG] Finished')
log.close()
