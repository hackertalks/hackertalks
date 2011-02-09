import pycurl

# hello.

import optparse
import os
import os.path
import BeautifulSoup


body = ''
def body_callback(buf):
    body += buf


if __name__ == '__main__':
    writtenfiles = ''
    try:
        writtenfiles = open('hackertalks-progress.txt', 'r').read()
    except Exception, e:
        print e
        pass
    progressfile = open('hackertalks-progress.txt', 'a')

    parser = optparse.OptionParser()
#    parser.add_option('-m', '--manual-metadata', help="do not parse metadata from file names, expect input for them instead")

    (opts, args) = parser.parse_args()

    dirname = args[0] if len(args)>0 else '.'

    for rn in os.listdir(dirname):
        body = ''
        fn = os.path.join(dirname, rn)
        print fn

        ap = os.path.realpath(fn)

        (name, extension) = rn.rsplit('.',1)

        if extension not in ('mp4','mpeg',):
            print 'skipping %s' % fn
            continue

        c = pycurl.Curl()
        c.setopt(c.URL, 'http://uploads.blip.tv/')
        c.setopt(c.HTTPPOST, [('post', '1',),
                              ('file', (pycurl.FORM_FILE, fn,),),
                              ('license', '4',),
                              ('title', name),
                             ])
        c.setopt(c.VERBOSE, 1)
        c.setopt(c.WRITEFUNCTION, body_callback)
        c.perform()
        c.close()

        progressfile.append('%s\n' % ap)
        progressfile.flush()

        id = BeautifulSoup.BeautifulSoup(body).find('id')

        c = pycurl.Curl()
        c.setopt(c.URL, HACKERTALKS_PING)
        c.setopt(c.HTTPPOST, [('id', id,),
                              ('auth_key', AUTHKEY,),
                             ])
        c.perform()
        c.close()
        
        
