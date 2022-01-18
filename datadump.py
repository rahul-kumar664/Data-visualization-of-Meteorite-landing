import sqlite3
import codecs

conn=sqlite3.connect('metorite.sqlite')
cur=conn.cursor()

cur.execute("select name,reclat,reclong from Metorite")
fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur:
    lat=row[1]
    lng=row[2]
    if lat==0 and lng==0: continue
    name=row[0]
    name=name.replace("'","")
    try :
        print(name, lat, lng)

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+name+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")            
