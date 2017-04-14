# -*- coding: utf-8 -*-

import urllib2
import sys
from bbdata.dbj import b64d, msg, gts, db
import conf
from bbdata import topic

#addr = 'ii ' + conf.URL

BL = set(open('%s/blacklist.txt' % conf.DATA).read().splitlines())

def getrepto(s):
    if 'repto/' in s:
        start = s.split('repto/')[1]
        return start.split('/')[0]
    else:
        return ''


def ii_acceptmsg(msgid, tmsg, newecho=''):
    t = tmsg.splitlines()
    repto = getrepto(t[0])
    if '.' in msgid:
        print 'this is echo'
        return
    if len(msgid) != 20:
        print 'wrong msgid %s' % msgid
        return
    if repto and len(repto) != 20:
        print 'wrong repto %s in %s' % (repto, msgid)
        return
    jd = {
        'mid': msgid,
        'echoarea': newecho or t[1],
        'txt': '\n'.join(t[8:]),
        'repto': repto,
        'msgfrom': t[3],
        'msgto': t[5],
        'title': t[6],
        'addr': t[4],
        'date': int(t[2]),
        'accepted': gts()
    }
    if topic.check_title(t[6]):
        topic.add_to_topic(topic.check_title(t[6]).encode('utf-8'),msgid)
    msg.save(msg(**jd))


def getf(l):
    print 'fetch %s' % l
    from StringIO import StringIO
    import gzip
    request = urllib2.Request(l)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        f = gzip.GzipFile(fileobj=StringIO(response.read()))
    else:
        f = response
    return f.read()


def sep(l, step=20):
    for x in range(0, len(l), step):
        yield l[x:x+step]


def debundle(ea, s, newecho=''):
    for n in s.splitlines():
        mid, kod = n.split(':', 1)
        msgbody = b64d(kod)
        msgbody = msgbody.decode('utf-8')
        ii_acceptmsg(mid, msgbody, newecho)


def fetch(ea, url):
    if ':' in ea:
        ea, newecho = ea.split(':')
    else:
        ea, newecho = ea, ea
    out = getf('%su/e/%s' % (url, ea))
    prev = set([x.mid for x in msg.select().where(msg.echoarea == newecho)])
    dllist = out.splitlines()
    dllist = [x for x in dllist if x not in prev and not '.' in x and len(x) == 20 and x not in BL]
    db.begin()
    for dl in sep(dllist, 40):
        if ''.join(dl):
            s = getf('%su/m/%s' % (url, '/'.join(dl)))
            debundle(ea, s, newecho)
    db.commit()

url = 'http://%s/' % sys.argv[1]

db.autocommit=False
for n in sys.argv[2:]:
    fetch(n, url)
