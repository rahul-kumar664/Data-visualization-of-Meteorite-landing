import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import ssl

def year(y):
    pieces=y.split('T')
    date=pieces[0]
    dpiece=date.split('-')
    cdate=dpiece[2]+'/'+dpiece[1]+'/'+dpiece[0]+'T'
    time=pieces[1]
    tpiece=time.split(':')
    if (tpiece[0]=='00'):
        tpiece[0]='12'
    ctime=tpiece[0]+':'+tpiece[1]+':'+tpiece[2]
    return cdate+ctime


conn=sqlite3.connect('metorite.sqlite')
cur=conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Metorite(id INTEGER PRIMARY KEY UNIQUE, name TEXT,
 recclass TEXT, mass_g INTEGER, year INTEGER, reclat INTEGER, reclong INTEGER)''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url='https://data.nasa.gov/resource/gh4g-9sfh.json'

connection=urllib.request.urlopen(url, context=ctx)
data=connection.read().decode()

print('data reterived',len(data))

try:
    js = json.loads(data)
except:
    print(data)

count=0
for entry in js:
    count+=1
    #print(count)
    try:
        name=entry['name']
        recclass=entry['recclass']
        mass=entry['mass']
        date=year(entry['year'])
        reclat=entry['reclat']
        reclong=entry['reclong']
    except:
        (name, recclass, mass, date, reclat, reclong)=(None, None, None, None, None, None)
    #print(count)
    if (name==None):
        continue
    #print(count)
    cur.execute('''select id from Metorite where
    (name,recclass,mass_g,year,reclat,reclong)=(?,?,?,?,?,?)
    limit 1''',(name, recclass, mass, date, reclat, reclong))
    try:
        row=cur.fetchone()[0]
        if row is not None:
            print('found in database')
            continue
    except:
        pass

    print(name, recclass, mass, date, reclat, reclong)

    cur.execute('''insert or ignore into Metorite (name, recclass, mass_g, year, reclat, reclong)
    values (?,?,?,?,?,?)''',(name, recclass, mass, date, reclat, reclong) )
    conn.commit()
