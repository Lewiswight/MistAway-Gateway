############################################################################
#                                                                          #
# Copyright (c)2008, 2009 Digi International (Digi). All Rights Reserved.  #
#                                                                          #
# Permission to use, copy, modify, and distribute this software and its    #
# documentation, without fee and without a signed licensing agreement, is  #
# hereby granted, provided that the software is used on Digi products only #
# and that the software contain this copyright notice,  and the following  #
# two paragraphs appear in all copies, modifications, and distributions as #
# well. Contact Product Management, Digi International, Inc., 11001 Bren   #
# Road East, Minnetonka, MN, +1 952-912-3444, for commercial licensing     #
# opportunities for non-Digi products.                                     #
#                                                                          #
# DIGI SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED   #
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A          #
# PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, #
# PROVIDED HEREUNDER IS PROVIDED "AS IS" AND WITHOUT WARRANTY OF ANY KIND. #
# DIGI HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,         #
# ENHANCEMENTS, OR MODIFICATIONS.                                          #
#                                                                          #
# IN NO EVENT SHALL DIGI BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,      #
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,   #
# ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF   #
# DIGI HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.                #
#                                                                          #
############################################################################

"""
iDigi Database Synchronization Module
"""

# imports

import digi_httplib as httplib
from settings.settings_base import SettingsBase, Setting
from presentations.presentation_base import PresentationBase
from common.helpers.format_channels import iso_date
from common.digi_device_info import get_platform_name
from core.tracing import get_tracer
from channels.channel_source_device_property import DPROP_PERM_GET
from common.digi_device_info import get_device_id
import threading
import digitime
import time
import cStringIO
from devices.xbee.common.addressing import *

# Because the idigi_data module can be external to Dia, we should try/except
# around it, just in case the user does not have the module for some reason.
try:
    import idigi_data
except:
    _tracer = get_tracer("idigi_db")
    _tracer.critical("Unable to import idigi_data!")
    raise

ADDRESS_A = """<gateway>"""
        
ADDRESS_B = """</gateway>"""
# constants
ENTITY_MAP = {
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    "\"": "&quot;",
    "'": "&apos;",
}

# exception classes
MAC = str(get_device_id())  #st
MAC = MAC.replace("0x0000000000000000", "")
MAC = MAC.replace("ffff", "")
MAC = MAC.upper()
print "Here is the MAC"
print MAC
# interface functions

# classes
class Uploader(PresentationBase, threading.Thread):

    """
    This class extends one of our base classes and is intended as an
    example of a concrete, example implementation, but it is not itself
    meant to be included as part of our developer API. Please consult the
    base class documentation for the API and the source code for this file
    for an example implementation.
    """

    def __init__(self, name, core_services):

        self.__name = name
        self.__core = core_services
        self.__stopevent = core_services
        self.offset = None
        self.update = False

        self.__tracer = get_tracer(name)

         # Settings
         # initial_upload: is the number of seconds before the first initial
         #     upload.  If it is not specified, initial upload is disabled.
         # interval: is the maximum interval in seconds that this module waits
         #     before sending data to the iDigi Manager Database.  If it is
         #     equal to 0, the feature is disabled.
         # sample_threshold: is the mininum number of samples required before
         #     sending data to the iDigi Manager Database.  If it is equal to
         #     0, the feature is disabled.
         # collection: is the collection on the database where the data will
         #     be stored.
         # file_count: the number of unique files we will keep on iDigi.
         # filename: the name of the xml file we will push to iDigi, with
         #     a number appended to the end (cycling from 1 to file_count)
         # channels: is the list of channels the module is subscribed to.
         #     If no channels are listed, all channels are subscribed to.
         # compact_xml: (when set to True) will produce output XML with the
         #     information stored as attributes to the sample node instead of
         #     separately tagged, resulting in smaller XML output.

        settings_list = [
           Setting(
              name='initial_upload', type=int, required=False,
              default_value=None),
           Setting(
              name='interval', type=int, required=False,
              default_value=60),
           Setting(
              name='sample_threshold', type=int, required=False,
              default_value=10),
           Setting(
              name='collection', type=str, required=False,
              default_value=""),
           Setting(
              name="channels", type=list, required=False,
              default_value=[]),
           Setting(
              name='file_count', type=int, required=False,
              default_value=20),
           Setting(
              name='filename', type=str, required=False,
              default_value="sample"),
           Setting(
              name='secure', type=bool, required=False,
              default_value=True),
           Setting(
              name='compact_xml', type=bool, required=False,
              default_value=False),
        ]

        PresentationBase.__init__(self, name=name,
                                   settings_list=settings_list)
        self.__stopevent = threading.Event()
        threading.Thread.__init__(self, name=name)
        threading.Thread.setDaemon(self, True)

    def start(self):

        # Verify that the user has a reasonable iDigi host set on their device.
        if hasattr(idigi_data, 'get_idigi_values'):
            host, token, path, port, secureport = idigi_data.get_idigi_values()
            if host == None or host == "" or host == " ":
                self.__tracer.error("iDigi Host '%s' is not a valid value. " +
                      "Please check your device and set the Host value " +
                      "appropriately", host)
                raise ValueError("name must be a non-empty string")

        # Start by appending 1 to filename of pushed data
        self.__current_file_number = 1

        # Event to use for notification of meeting the sample threshold
        self.__threshold_event = threading.Event()

        # Count of samples since last data push
        self.__sample_count = 0

        # Here we grab the channel publisher
        channels = SettingsBase.get_setting(self, "channels")
        cm = self.__core.get_service("channel_manager")
        cp = cm.channel_publisher_get()

        # And subscribe to receive notification about new samples
        # as long as sample_threshold is not 0
        sample_threshold = SettingsBase.get_setting(self, "sample_threshold")
        if sample_threshold:
            if len(channels) > 0:
                for channel in channels:
                    cp.subscribe(channel, self.receive)
            else:
                cp.subscribe_to_all(self.receive)

        threading.Thread.start(self)
        self.apply_settings()
        return True


    def stop(self):
        self.__stopevent.set()
        return True

    def upload_data(self):
        self.update = True

    def apply_settings(self):

        SettingsBase.merge_settings(self)
        accepted, rejected, not_found = SettingsBase.verify_settings(self)

        if len(rejected) or len(not_found):
            # There were problems with settings, terminate early:
            self.__tracer.error("Settings rejected/not found: %s %s",
                                rejected, not_found)
            return (accepted, rejected, not_found)

        SettingsBase.commit_settings(self, accepted)
        return (accepted, rejected, not_found)

    def receive(self, channel):
        # Check how many samples it takes to meet the sample threshold
        sample_threshold = SettingsBase.get_setting(self, "sample_threshold")
        self.__sample_count += 1
        # self.__tracer.info("idigi_db (%s): Received sample %i", \
        #       self.__name, self.__sample_count)

        # If we have exceeded the sample threshold, notify the thread
        # responsible for pushing up data
        if self.__sample_count >= sample_threshold:
            self.__tracer.debug("Reached threshold of %i, setting event flag",
                               sample_threshold)
            self.__sample_count = 0
            self.__threshold_event.set()

    def run(self):
        
        while self.offset is None:
            try:
                time.sleep(30)
                self.getOffest()
            except:
                pass

        interval = SettingsBase.get_setting(self, "initial_upload")
        if interval is None:
            interval = SettingsBase.get_setting(self, "interval")
        self.__last_upload_clock = 0
        self.__last_upload_time = 0
        while not self.__stopevent.isSet():
            try:
                # 32 bit modulo math to account for an NDS bug :-(
                now = int(digitime.real_clock()) & 0xffffffff
                time_passed = (now - self.__last_upload_clock) & 0xffffffff
                interval_met = (interval > 0 and
                                time_passed > interval)
                threshold_met = self.__threshold_event.isSet()
                if interval_met:
                    self.update = False
                    interval = SettingsBase.get_setting(self, "interval")
                    self.__sample_count = 0
                    self.__threshold_event.clear()
                    self.__upload_data()
                elif threshold_met:
                    self.update = False
                    interval = SettingsBase.get_setting(self, "interval")
                    self.__threshold_event.clear()
                    self.__upload_data()
                elif self.update == True:
                    self.update = False
                    interval = SettingsBase.get_setting(self, "interval")
                    self.__threshold_event.clear()
                    self.__upload_data()
                digitime.sleep(1)
            except Exception, e:
                self.__tracer.error("exception while uploading: %s", str(e))

        self.__tracer.warning("Out of run loop.  Shutting down...")

        # Clean up channel registration
        cm = self.__core.get_service("channel_manager")
        cp = cm.channel_publisher_get()
        cp.unsubscribe_from_all(self.receive)

    
    
    def convert_timestamp(self, timestamp):
        
        """if self.first_upload == True:
            self.first_upload = False
            self.offset = self.getOffest()"""
            
        sec_time = int(timestamp)
        time_here = sec_time + self.offset 
        return time_here
            
    def getOffest(self):
        cm = self.__core.get_service("channel_manager")
        cdb = cm.channel_database_get()
        main_addr = "mainMistaway_" + gw_extended_address()
        timezone = cdb.channel_get(main_addr + ".offset")
        timezone = timezone.get()
        timezone = timezone.value
        self.offset = int(timezone)
    
    
    def __upload_data(self):

        xml = cStringIO.StringIO()

        #xml.write("<?xml version=\"1.0\"?>")
        compact_xml = SettingsBase.get_setting(self, "compact_xml")
        if compact_xml:
            xml.write("<idigi_data compact=\"True\">")
        else:
            xml.write("""{ "data": {"MAC": "%s", "samples": [""" % str(MAC) )

        cm = self.__core.get_service("channel_manager")
        cdb = cm.channel_database_get()

        channel_list = SettingsBase.get_setting(self, "channels")
        if len(channel_list) == 0:
            channel_list = cdb.channel_list()

        new_sample_count = 0

        for channel_name in channel_list:
            try:
                channel = cdb.channel_get(channel_name)
                if not (channel.perm_mask() & DPROP_PERM_GET):
                    # skip ungettable things
                    continue
                sample = channel.get()
                if sample.timestamp >= self.__last_upload_time and sample.timestamp >= 1315351499.0 and sample.unit != "1":
                    self.__tracer.debug("Channel %s was updated since last " +
                           "push", channel_name)
                    new_sample_count += 1
                    compact_xml = SettingsBase.get_setting(self, "compact_xml")
                    if compact_xml:
                        xml.write(self.__make_compact_xml(channel_name,
                                                          sample))
                    else:
                        xml.write(self.__make_xml(channel_name, sample))
                else:
                    self.__tracer.debug("Channel %s was not updated since " +
                          "last push", channel_name)
            except Exception, e:
                # Failed to retrieve the data
                self.__tracer.warning("Exception in getting sample data: %s",
                                    str(e))

  



        xml2 = xml.getvalue()
        xml2 = xml2[:-1]
        xml2 = xml2 + "] }" 

        if new_sample_count > 0:
            self.__tracer.debug("Starting upload to iDigi")
            # Due to an NDS issue, clock may roll over, we'll just
            # keep track modulo 32-bit to allow for that.
            self.__last_upload_clock = int(digitime.real_clock()) & 0xffffffff
            self.__last_upload_time = digitime.time()

            success = self.__send_to_idigi(xml2)
            if success == True:
                self.__tracer.debug("Finished upload to iDigi")
            else:
                self.__tracer.debug("Upload failed to iDigi")
        else:
            self.__tracer.debug("No new Sample data to send to iDigi")

        xml.close()

    def __make_xml(self, channel_name, sample):
        
        
        data = "{"
        data += """"name" : "%s","""
        data += """"value" : "%s","""
        data += """ "timestamp" : "%s" """
        data += "},"

        return data % (channel_name, self.__escape_entities(sample.value),
                        self.convert_timestamp(sample.timestamp))


    def __make_compact_xml(self, channel_name, sample):

        data = "<sample name=\"%s\" value=\"%s\" unit=\"%s\" timestamp=\"%s\" />"

        return data % (channel_name, self.__escape_entities(sample.value),
                       sample.unit, self.convert_timestamp(sample.timestamp))


    def __send_to_idigi(self, data):

        success = True
        
        Message = data 
        
        
        print "message compiled" 
        
  
       
        send_error1 = "error sending message to Dane's web service"


        try:
       
            string = """{'postedValue': '%s }' }}""" % Message
            
            print string
            
         
          #  self.filenumber += 1
            
            
            
          #  file = str(self.filenumber)
            
          #  file2 = open("WEB/python/XML" + file + ".txt", "w")
            
          #  file2.write(string)
            
          #  file2.close()

            print "opening http post"
            webservice = httplib.HTTPConnection("devbuildinglynx.apphb.com", timeout=10)
            #    print "line 1"
            webservice.putrequest(unicode("POST", "utf-8" ), unicode("/api/JsonUploader", "utf-8" ), "HTTP/1.1")
            #        webservice.putheader("POST", "/NumericUpDown.asmx", "" )
            #    print "line 2"
            webservice.putheader(unicode("Host", "utf-8" ), unicode("devbuildinglynx.apphb.com", "utf-8" ))
            #        webservice.putheader("User-Agent: ", "Python Post")
            #    print "line 3"
            webservice.putheader(unicode("Content-Type", "utf-8" ), unicode("application/json; charset=\"UTF-8\"", "utf-8" ))
            #    print "line 4"
            webservice.putheader(unicode("Content-Length", "utf-8" ), unicode("%d", "utf-8" ) % len(string))
            #   print "line 5"
            #webservice.putheader(unicode("SOAPAction", "utf-8" ), unicode("\"http://houselynx.com/webservices/XMLparser\"", "utf-8" ))
            #  print "line 6"
            webservice.endheaders()
            # print "line 7"
            webservice.send(unicode(string, "utf-8" ))
            
            
            response = webservice.getresponse()
            errcode = response.status
            errmsg = response.reason
            headers = response.msg
            print errcode
            print errmsg
            print headers
            
            webservice.close()
            print "close http post"
            
            """
            statuscode, statusmessage, header = webservice.getreply()
            print "Response: ", statuscode, statusmessage
            print "headers: ", header
            res = webservice.getfile().read()
            print res"""
        except:
            return False
        return success

    def __escape_entities(self, sample_value):

        if not isinstance(sample_value, str):
            return sample_value
        for ch in ENTITY_MAP:
            sample_value = sample_value.replace(ch, ENTITY_MAP[ch])

        return sample_value
