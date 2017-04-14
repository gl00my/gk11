# -*- coding: utf-8 -*-

import conf, dbj, os


def get_topics():
    topiclist, lst = [], []
    for n in os.listdir(conf.DATA):
        if n.startswith('topic-'):
            topiclist.append([os.path.getmtime('%s/%s' % (conf.DATA, n)),n])
    for k,v in reversed(sorted(topiclist)):
        b = []
        b.append(int(k))
        b.append(v[6:])
        b = b + open('%s/%s' % (conf.DATA, v)).read().decode('utf-8').splitlines()
        lst.append(b)
    return lst

def get_topic(tid,flag):
    lst = open('%s/topic-%s' % (conf.DATA, tid)).read().decode('utf-8').splitlines()
    title = lst[0]
    lst = lst[1:]
    if flag!='rev':
        lst.reverse()
    if flag =='last':
        lst = lst[:30]
    return ':'.join(lst), title

def check_title(s):
    if s.lower().startswith('re:'):
        s = s[3:]
    s = s.strip()
    if s.startswith('##') and s.endswith('##'):
        return s[2:][:-2].strip()

def add_to_topic(s,mid):
    th = dbj.hsh2(s)
    tp = '%s/topic-%s' % (conf.DATA, th)
    print os.path.exists(tp)
    if not os.path.exists(tp):
        print s
        open(tp, 'a').write(s + '\n')
    open(tp, 'a').write(mid + '\n')
