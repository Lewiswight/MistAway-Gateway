

import MySQLdb 

myDB = MySQLdb.connect(host="ec2-50-16-188-172.compute-1.amazonaws.com", port=3306, user="dane", passwd="WjDPqJPIl40c")

db=myDB.cursor()
db.execute("USE mistaway_channels")
db.execute("SHOW TABLES")
tables = db.fetchall()

for (table_name,) in db:
        print(table_name)



#results=cHandler.fetchall()
#print "=========================", "<br>"
#for items in results:
#   print items[0]







"""import urllib




url = "http://devbuildinglynx.apphb.com/api/gateway?checkmac=00409DFF-FF3F2E7D&dummy1=0&dummy2=1" 
         
try:
    f = urllib.urlopen(url)
except:
   print "Error opening url"

    
    
    
    
    
    
s = f.read()
print s


listenting on 2 ports 
AES 128 bit set up
key has been shared semetric key
all data must be encripted.
unique ID, timestamp, semicolon demilited 
AES 128 bit encription """





"""offset = ""
place_temp = s.find("gmt_offset")
temp_offset = s[place_temp + 12 : place_temp + 20]
for i in temp_offset:
    if i != ",":
        offset = offset + i 
    else:
        break
offset = int(offset)
print offset


dst = ""
place_dst = s.find("dst")
temp_dst = s[place_dst + 6 : place_dst + 7]
dst = temp_dst
print dst
dst = dst.strip()
if dst == "0":
    dst = False
if dst == "1":
    dst = True
print "here is your DST value"
print dst"""