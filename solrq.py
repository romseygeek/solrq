#!/usr/bin/env python

"""Usage: solrq [options] <query>

Connection options:
    -h <host>, --host <host>              hostname of solr server [default: localhost]
    -p <port>, --port <port>              port of solr server [default: 8983]
    -t <path>, --path <path>              path to solr server [default: solr/]
    --url <url>                           complete url to solr server

Debugging options:
    -v, --verbose                         verbose output
"""

import requests
import sys
from docopt import docopt

VERSION = "0.0.1"

def build_http_query(options, query):
    url = options['--url'] or "http://%(--host)s:%(--port)s/%(--path)s" % options
    url += "/select"
    params = { 'q' : query, 'wt' : 'json' }
    return url, params

def format_results(options, solrresponse):
    return solrresponse.json

options = docopt(__doc__, version=VERSION)
query = options['<query>']
url, params = build_http_query(options, query)
response = requests.get(url, params=params)
if options['--verbose']:
    print response.url
print format_results(options, response)
