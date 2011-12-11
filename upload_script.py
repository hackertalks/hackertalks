import os
import os.path
import optparse

import pycurl
import BeautifulSoup

import re


HACKERTALKS_PING = 'http://hackertalks.org/api/ping'

body = ''
def body_callback(buf):
    global body
    body += buf

def ping_hackertalks(id):
    c = pycurl.Curl()
    c.setopt(c.URL, HACKERTALKS_PING)
    c.setopt(c.HTTPPOST, [('id', '%s' % id,),
                          ('api_key', '%s' % APIKEY),
                         ])
    c.perform()
    c.close()

def try_get_description(fn):
    try:
        descfile = re.sub(r'\....$', '.txt', fn)
        return "\n".join(open(descfile).readlines())
    except e:
        print e
        return None

def upload_blip(fn, speaker, name, BLIPUSER, BLIPASSWORD):
    global body

    description = try_get_description(fn) or '%s  %s' % (name, speaker,)

    c = pycurl.Curl()
    c.setopt(c.URL, 'http://uploads.blip.tv/')
    c.setopt(c.HTTPPOST, [('post', '1',),
                          ('cmd', 'post',),
                          ('file', (pycurl.FORM_FILE, fn,),),
                          ('license', '4',),
                          ('title', '%s - %s'  % (speaker, name,)),
                          ('body', description),
                          ('userlogin', BLIPUSER,),
                          ('password', BLIPASSWORD,),
                          ('skin', 'api',),
                         ])
    c.setopt(c.VERBOSE, 1)
    c.setopt(c.WRITEFUNCTION, body_callback)
    c.perform()
    c.close()

    print body

    return BeautifulSoup.BeautifulSoup(body).find('id').renderContents()


if __name__ == '__main__':
    writtenfiles = ''
    try:
        writtenfiles = open('.hackertalks-progress.txt', 'r').readlines()
    except Exception, e:
        print e
        pass
    progressfile = open('.hackertalks-progress.txt', 'a')

    parser = optparse.OptionParser()
    parser.add_option('-u', '--user', help="your blip.fm user")
    parser.add_option('-p', '--password', help="your blip.fm password")
    parser.add_option('-k', '--apikey', help="your hackertalks.org api key")

    (opts, args) = parser.parse_args()
    APIKEY = opts.apikey
    BLIPUSER = opts.user
    BLIPASSWORD = opts.password

    dirname = args[0] if len(args)>0 else '.'

    for rn in os.listdir(dirname):
        body = ''

        fn = os.path.join(dirname, rn)
        ap = os.path.realpath(fn)

        cancel = False
        for line in writtenfiles:
            if line.startswith(ap):
                print 'skipping %s because it has already been uploaded' % rn
                cancel = True
                break
        if cancel:
            continue

        (name, extension) = rn.rsplit('.',1)


        if extension not in ('mp4','mpeg','mov',):
            print 'skipping %s' % fn
            continue


        (speaker, name) = name.rsplit(' - ', 1)

        id = upload_blip(fn, speaker, name, BLIPUSER, BLIPASSWORD)

        if not id:
            print 'failed!'
            continue

        progressfile.write('%s: %s\n' % (ap, id))
        progressfile.flush()


        ping_hackertalks(id)

