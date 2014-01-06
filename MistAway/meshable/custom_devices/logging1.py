import  httplib



    
part1 = """{"postedValue": { "data": {"MAC": "FAKE05FAKE05", "samples": [{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.outofrange","value" : "1", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.units","value" : "2", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.applicationtype","value" : "0", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.blanking","value" : "0", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.gaincontrol","value" : "1", "timestamp" : "1387392695" },{"name" : "mainMistaway_[05:13:a2:00:40:99:6a:69]!.w_h","value" : "O", "timestamp" : "1387392691" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.decimalplace","value" : "3", "timestamp" : "1387392695" },{"name" : "mainMistaway_[05:13:a2:00:40:99:6a:69]!.zip","value" : "10001", "timestamp" : "1387392691" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.pulses","value" : "16", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p2a","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p5b","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p3b","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p3a","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p1a","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.raw","value" : "283", "timestamp" : "1387392848" },{"name" : "mainMistaway_[05:13:a2:00:40:99:6a:69]!.hb","value" : "On", "timestamp" : "1387392729" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p4b","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.reading1","value" : "0", "timestamp" : "1387392844" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.filterwindow","value" : "8000", "timestamp" : "1387392695" },{"name" : "mainMistaway_[05:13:a2:00:40:99:6a:69]!.firmUpdate","value" : "file_name", "timestamp" : "1387392691" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.tempcomp","value" : "0", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.deviceaddress","value" : "1", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.averaging","value" : "1", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.volumeunits","value" : "3", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.samplerate","value" : "250", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p2b","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.reading2","value" : "11141", "timestamp" : "1387392848" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p4a","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.offset","value" : "0", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.sensitivity","value" : "75", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.maxdistance","value" : "1000", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p1b","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.p5a","value" : "0", "timestamp" : "1387392699" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.fulldistance","value" : "10", "timestamp" : "1387392695" },{"name" : "mainMistaway_[05:13:a2:00:40:99:6a:69]!.offset","value" : "-25200", "timestamp" : "1387392729" },{"name" : "mainMistaway_[05:13:a2:00:40:99:6a:69]!.w_t","value" : "60", "timestamp" : "1387392691" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.celsius","value" : "22", "timestamp" : "1387392848" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.multiplier","value" : "1013", "timestamp" : "1387392695" },{"name" : "fsapgus_[05:13:a2:00:40:9f:29:78]!.emptydistance","value" : "9000", "timestamp" : "1387392695" }] } }}"""


string = part1 
print string
print 
print

#  self.filenumber += 1



#  file = str(self.filenumber)

#  file2 = open("WEB/python/XML" + file + ".txt", "w")

#  file2.write(string)

#  file2.close()

#print "opening http post"

webservice = httplib.HTTPConnection("imistaway.com", timeout=10)
#    #print "line 1"
webservice.putrequest(unicode("POST", "utf-8" ), unicode("/api/JsonUploader", "utf-8" ), "HTTP/1.1")
#        webservice.putheader("POST", "/NumericUpDown.asmx", "" )
#    #print "line 2"
webservice.putheader(unicode("Host", "utf-8" ), unicode("imistaway.com", "utf-8" ))
#        webservice.putheader("User-Agent: ", "Python Post")
#    #print "line 3"
webservice.putheader(unicode("Content-Type", "utf-8" ), unicode("application/json", "utf-8" ))
#    #print "line 4"
webservice.putheader(unicode("Content-Length", "utf-8" ), unicode("%d", "utf-8" ) % len(string))
#   #print "line 5"
#webservice.putheader(unicode("SOAPAction", "utf-8" ), unicode("\"http://houselynx.com/webservices/XMLparser\"", "utf-8" ))
#  #print "line 6"
webservice.endheaders()
# #print "line 7"
webservice.send(unicode(string, "utf-8" ))



response = webservice.getresponse()
errcode = response.status
errmsg = response.reason
headers = response.msg
print errcode
print errmsg
print headers

webservice.close()
