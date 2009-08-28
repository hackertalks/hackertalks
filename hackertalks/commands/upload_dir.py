from paste.script.command import Command
import getpass
import httplib
import mimetypes
import os
import re
import sys
import urllib2
import urlparse
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape


class Upload_Dir(Command):
        # Parser configuration
        summary = "--NO SUMMARY--"
        usage = "--NO USAGE--"
        group_name = "hackertalks"
        parser = Command.standard_parser(verbose=False)
  
        BLIP_UPLOAD_URL = "http://blip.tv/file/post"
        
        MULTIPART_BOUNDARY = "-----------$$SomeFancyBoundary$$"
        
        def PostMultipart(self, url, fields, files):
            """@brief Send multi-part HTTP POST request
            
            @param url POST URL
            @param fields A dict of {field-name: value}
            @param files A list of [(field-name, filename)]
            @return Status, reason, response (see httplib.HTTPConnection.getresponse())
            """
            content_type = 'multipart/form-data; boundary=%s' % self.MULTIPART_BOUNDARY
            data = []
            for field_name, value in fields.iteritems():
                data.append('--' + self.MULTIPART_BOUNDARY)
                data.append('Content-Disposition: form-data; name="%s"' % field_name)
                data.append('')
                data.append(value)
            for (field_name, filename) in files:
                data.append('--' + self.MULTIPART_BOUNDARY)
                data.append('Content-Disposition: form-data; name="%s"; filename="%s"'
                            % (field_name, filename))
                data.append('Content-Type: %s' % self.GetMimeType(filename))
                data.append('')
                data.append(open(filename).read())
            data.append('--' + self.MULTIPART_BOUNDARY + '--')
            data.append('')
            data = "\r\n".join(data)
        
            host, selector = urlparts = urlparse.urlsplit(url)[1:3]
            h = httplib.HTTPConnection(host)
            h.putrequest("POST", selector)
            h.putheader("content-type", content_type)
            h.putheader("content-length", len(data))
            h.endheaders()
            h.send(data)
            response = h.getresponse()
            return response.status, response.reason, response.read()    
        
        def GetMimeType(self, filename):
            return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        def Upload(self, video_id, username, password, title, description, filename):
            """@brief Upload to blip.tv
            
            @param video_id Either the item ID of an existing post or None to upload
                a new video
            @param username, password
            @param title New title of the post
            @param description New description of the post
            @param filename Filename of the video to upload (if a @a video_id is specified),
                this file is uploaded as an additional format to the existing post)
            @return Response data
            """
            fields = {
                "post": "1",
                "skin": "xmlhttprequest",
                "userlogin": "%s" % username,
                "password": "%s" % password,
                "item_type": "file",
                "title": "%s" % title.encode("utf-8"),
                "description": "%s" % description.encode("utf-8"),
                }
            if video_id:    # update existing
                fields["id"] = "%s" % video_id
                file_field = "file1"
            else:           # new post
                file_field = "file"
            if filename:
                fields[file_field + "_role"] = "Web"
                files = [(file_field, filename)]
            else:
                files = []
            
            print "Posting to", self.BLIP_UPLOAD_URL
            print "Please wait..."
            status, reason, response = self.PostMultipart(self.BLIP_UPLOAD_URL, fields, files)
            print "Done."
        
            return response

        def AskForDir(self):
            viddir = None
            while viddir is None:
                viddir = raw_input("Enter a directory for upload: ") 
                if os.path.isdir(viddir):
                    return viddir + '/'
                else:
                    print "Invalid directory"
            return viddir
        
        
        def AskYesNo(self, question, default=True):
            while True:
                if default == True:
                    options = "[Y/n]"
                else:
                    options = "[y/N]"
                yes_no = raw_input(question + " " + options + " ")
                if not yes_no:
                    return default
                elif yes_no in ["Y", "y"]:
                    return True
                elif yes_no in ["N", "n"]:
                    return False
                    
        def GetTextFromDomNode(self, node):
            rc = ""
            for n in node.childNodes:
                if n.nodeType == node.TEXT_NODE or n.nodeType == node.CDATA_SECTION_NODE:
                    rc = rc + n.data
            return rc
        
        def GetVideoInfo(self, video_id):
            """@brief Return information about the video
            
            @param video_id blip.tv item ID
            @return A tuple of
                @a title (string),
                @a description (string),
                @a link (URL to video as a string),
                @a embed_code (HTML <embed> code as a string),
                @a embed_id (the part of the <embed> code that's used with the Drupal filter,
                    e.g., "AbCcKIuEBA"),
                @a existing_mime_types (a dict of {mime_type: list_of_file_urls}
                    containing the URLs that are currently part of the post)
            """
            url = 'http://blip.tv/file/%(video_id)s?skin=rss' % locals()
            print "Loading", url, "..."
            xml_code = urllib2.urlopen(url).read()
            rss = parseString(xml_code)
            channel = rss.getElementsByTagName("channel")[0]
            item = channel.getElementsByTagName("item")[0]
            title = self.GetTextFromDomNode(item.getElementsByTagName("title")[0])
            description = unescape(self.GetTextFromDomNode(item.getElementsByTagName("blip:puredescription")[0]))
            link = self.GetTextFromDomNode(item.getElementsByTagName("link")[0])
            embed_code = self.GetTextFromDomNode(item.getElementsByTagName("media:player")[0])
            embed_id = None
            m = re.search(r"http://blip.tv/play/(\w+)", embed_code)
            if m:
                embed_id = m.group(1)
        
            existing_mime_types = {}
            media_group = item.getElementsByTagName("media:group")[0]
            for content in media_group.getElementsByTagName("media:content"):
                existing_mime_types.setdefault(content.attributes["type"].value, []).append(
                    content.attributes["url"].value)
                
            return title, description, link, embed_code, embed_id, existing_mime_types
        
        def DisplayVideoInfo(self, title, link, embed_code, embed_id, existing_mime_types):
            print "Title           =", title
            print "Link            =", link
            if embed_id:
                print "Embed ID        =", embed_id
            else:
                print "Embed ID        = <The video hasn't been converted to Flash yet>"
            if existing_mime_types:
                print "Files           ="
                for urls in existing_mime_types.itervalues():
                    for url in urls:
                        print "    " + url
        
        def ConvertToOggTheora(self, filename):
            out_filename = os.path.splitext(filename)[0] + os.extsep + "ogg"
            cmd = 'ffmpeg2theora -o "%(out_filename)s" "%(filename)s"' % locals()
            print "Running", cmd, "..."
            exit_code = os.system(cmd)
            if exit_code:
                print "Error: Command returned with code %r" % (exit_code,)
                sys.exit(1)
            return out_filename
        
        def GetDescription(self, default):
            if os.path.exists("description.txt"):
                print ''
                print 'Taking description from file "description.txt"...'
                default = open("description.txt").read()
            print "Current description:\n  {{{%s}}}" % default
            print ""
            desc = raw_input(
                'Type a new one-line description or press RETURN to keep the current one\n'
                '  (If you need more than one line, press Ctrl+C to abort,\n'
                '  create a file named "description.txt" and run again): ')
            return desc or default
        
        
        def command(self):
            video_id = None
            viddir = None
            if len(sys.argv) > 2:
                if os.path.isdir(sys.argv[2]):
                    viddir = sys.argv[2]
                else:
                    print('Invalid Directory!')
                return 1
            else:
                viddir = self.AskForDir()
            username = None
            password = None
            for f in os.listdir(viddir):
                m = re.match(r'(.*)\.(avi|mp4|ogg|mov)$', f)
                if m:
                    filename = viddir + f
                    title = m.group(1)
                    mime_type = self.GetMimeType(filename)
                    if os.path.exists(viddir + title + ".txt"):
                        description = open(viddir + title + ".txt").read()
                    else:
                        description = ''
                    print ("about to upload %s with title %s and description %s") % (filename, title, description)
                    if not username:
                        username = raw_input("blip.tv Username: ")
                        password = getpass.getpass("blip.tv Password: ")
                    response = self.Upload(video_id, username, password, title, description, filename)
                    print ("%s uploaded with server responce %s") % (filename, response)
            return 0
