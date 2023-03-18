#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""tab analyzer - process a text file of URLs
for example, exported from https://github.com/alct/export-tabs-urls

"""

import json
import os
import sys
try:
    from urllib.parse import urlparse
except ImportError:
    # Py2
    from urlparse import urlparse


def get_all_lines(readobject):
    for line in readobject:
        line = line.strip()
        yield line

def get_nonblank_lines(readobject):
    for line in readobject:
        line = line.strip()
        if line  != '':
            yield line


def analyzer_tabs(filename):
    protocols = {}
    domains = {}
    with open(filename) as f:  # FIXME encoding
        for line in (get_nonblank_lines(f)):
            #protocol = line.split(':')[0]  # dumb URL processing, use a library! instead
            url_parsed = urlparse(line)
            # then determine domain for protocols that use domains
            protocol = url_parsed.scheme
            protocols[protocol] = protocols.get(protocol, 0) + 1
            domain = url_parsed.netloc   # NOTE includes port, not just domain
            domains[domain] = domains.get(domain, 0) + 1
            #print(url_parsed)
    print(json.dumps(domains, indent=4))
    sorted_domains = dict(sorted(domains.items(), key=lambda item: item[1]))  # FIXME doesn't dump json in sorted order in Python2!
    print(json.dumps(sorted_domains, indent=4))
    print(json.dumps(protocols, indent=4))
    sorted_list = []
    for domain_name in domains:
        sorted_list.append((domains[domain_name], domain_name))
    sorted_list.sort()
    max_top_items = 20
    max_top_items = 30
    for domain_count_tuple in sorted_list[-1 * max_top_items:]:
        print(domain_count_tuple)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version, sys.platform))

    # Dumb argument processing
    try:
        filename = argv[1]
    except IndexError:
        filename = 'tabs.txt'

    analyzer_tabs(filename)

    return 0


if __name__ == "__main__":
    sys.exit(main())
