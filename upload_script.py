import pycurl

# hello.

import optparse
import os
import os.path
import BeautifulSoup


HACKERTALKS_PING = 'http://localhost:5000/api/ping'

body = ''
def body_callback(buf):
    global body
    body += buf


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
        global body
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

        c = pycurl.Curl()
        c.setopt(c.URL, 'http://uploads.blip.tv/')
        c.setopt(c.HTTPPOST, [('post', '1',),
                              ('cmd', 'post',),
                              ('file', (pycurl.FORM_FILE, fn,),),
                              ('license', '4',),
                              ('title', '%s - %s'  % (speaker, name,)),
                              ('body', '%s  %s' % (name, speaker,)),
                              ('userlogin', BLIPUSER,),
                              ('password', BLIPASSWORD,),
                              ('skin', 'api',),
                             ])
        c.setopt(c.VERBOSE, 1)
        c.setopt(c.WRITEFUNCTION, body_callback)
        c.perform()
        c.close()

        print body
        
        id = BeautifulSoup.BeautifulSoup(body).find('id').renderContents()

        if not id:
            print 'failed!'
            continue

        progressfile.write('%s: %s\n' % (ap, id))
        progressfile.flush()


        c = pycurl.Curl()
        c.setopt(c.URL, HACKERTALKS_PING)
        c.setopt(c.HTTPPOST, [('id', '%s' % id,),
                              ('api_key', '%s' % APIKEY),
                             ])
        c.perform()
        c.close()

