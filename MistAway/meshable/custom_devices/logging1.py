import  httplib


volts = 12.85 #12.50
timestamp = 1375287776

with open("data.txt") as f:
    pressure = f.readlines()

for x in range(0, 228):
    
    NewVolts = str((volts - (x * .001)))
    NewTimestamp = str((timestamp + (x * 3600))) 
    press = str(pressure[x])
    
    part1 = """{'postedValue':'<gateway>999999999999<idigi_data><sample><name>tt_[00:00:00:00:00:00:00:11]!.press</name><value>%s</value><unit></unit><timestamp>%s</timestamp></sample>""" % (press, NewTimestamp)
    part2 = """<sample><name>mainMistaway_[99:99:99:99:99:99:11:09]!.hb</name><value>On</value><unit></unit><timestamp>%s</timestamp></sample>"""  % (NewTimestamp)
    part3 = """<sample><name>tt_[00:00:00:00:00:00:00:11]!.temp</name><value>14.2</value><unit></unit><timestamp>%s</timestamp></sample>"""  % (NewTimestamp)
    part4 = """<sample><name>tt_[00:00:00:00:00:00:00:11]!.low</name><value>2.00</value><unit></unit><timestamp>%s</timestamp></sample>"""  % (NewTimestamp)
    part5 = """<sample><name>tt_[00:00:00:00:00:00:00:11]!.high</name><value>10.00</value><unit></unit><timestamp>%s</timestamp></sample>"""  % (NewTimestamp)
    part6 = """<sample><name>tt_[00:00:00:00:00:00:00:11]!.volt</name><value>%s</value><unit></unit><timestamp>%s</timestamp></sample>"""  % (NewVolts, NewTimestamp)
    end = """</idigi_data></gateway>'}"""


    string = part1 + part2 + part3 + part4 + part5 + part6 + end   
    print string
    print 
    print
    
    #  self.filenumber += 1
    
    
    
    #  file = str(self.filenumber)
    
    #  file2 = open("WEB/python/XML" + file + ".txt", "w")
    
    #  file2.write(string)
    
    #  file2.close()
    
    #print "opening http post"

    webservice = httplib.HTTPConnection("devbuildinglynx.apphb.com", timeout=10)
    #    #print "line 1"
    webservice.putrequest(unicode("POST", "utf-8" ), unicode("/api/fromGateway", "utf-8" ), "HTTP/1.1")
    #        webservice.putheader("POST", "/NumericUpDown.asmx", "" )
    #    #print "line 2"
    webservice.putheader(unicode("Host", "utf-8" ), unicode("devbuildinglynx.apphb.com", "utf-8" ))
    #        webservice.putheader("User-Agent: ", "Python Post")
    #    #print "line 3"
    webservice.putheader(unicode("Content-Type", "utf-8" ), unicode("application/json; charset=\"UTF-8\"", "utf-8" ))
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
