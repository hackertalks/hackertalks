http://uploads.blip.tv/

def PostMultipart(url, fields, files):
	content_type = 'multipart/form-data; boundary=%s' % MULTIPART_BOUNDARY
	data = []
	
	for field_name, value in fields.iteritems():
		data.append('--' + MULTIPART_BOUNDARY)
		data.append('Content-Disposition: form-data; name="%s"' % field_name)
		data.append('')
		data.append(value)
		
	for (field_name, filename) in files:
		data.append('--' + MULTIPART_BOUNDARY)
		data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename))
		data.append('Content-Type: %s' % GetMimeType(filename))
		data.append('')
		data.append(open(filename).read())
		
	data.append('--' + MULTIPART_BOUNDARY + '--')
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

def GetMimeType(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def Upload(video_id, username, password, title, description, filename):
	fields = {
		"post": "1",
		"skin": "api",
		"username": "$USERNAME",
		"password": "$PASSWORD",
		"filename": "$FILENAME",
		"title": "$TITLE",
	}
	
	file_field = "file"
	fields[file_field + "_role"] = "Web"
	files = [(file_field, filename)]
	
    print "Posting to", BLIP_UPLOAD_URL
    print "Please wait..."
    status, reason, response = PostMultipart(BLIP_UPLOAD_URL, fields, files)
    print "Done."

    return response
