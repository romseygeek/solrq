#!/usr/bin/env python

"""Usage: solrq [options] <query>

Connection options:
    -h <host>, --host <host>              hostname of solr server [default: localhost]
    -p <port>, --port <port>              port of solr server [default: 8983]
    -t <path>, --path <path>              path to solr server [default: solr/]
    --url <url>                           complete url to solr server

Search options:
    --filter <filter>                     filter query
    --phrase <phrase>                     phrase filter (for dismax query handlers)
    --boost <boost>                       boost query

Output options:
    -c, --count                           print the number of matching docs
    -f <fields>, --fields <fields>        comma-delimited list of fields to display [default: *,score]

Debugging options:
    -v, --verbose                         verbose output
    -x, --explain                         explain scores
"""

import requests
import sys
import pprint
from docopt import docopt

VERSION = "0.0.1"

def build_http_query(options, query):
    url = options['--url'] or "http://%(--host)s:%(--port)s/%(--path)s" % options
    url += "/select"
    params = { 'q' : query, 'wt' : 'json' }
    fl = options['--fields']
    if 'id' not in fl.split(','): 
        fl += ",id"
    params['fl'] = fl
    if options['--filter']:
        params['fq'] = options['--filter']
    if options['--phrase']:
        params['pf'] = options['--phrase']
    if options['--boost']:
        params['bq'] = options['--boost']
    if options['--explain']:
        params['debugQuery'] = "on"
    return url, params

def format_results(options, solrresponse):
    json = solrresponse.json
    if options['--count']:
        return json['response']['numFound']
    return [ format_result(options, doc, json) for doc in json['response']['docs'] ]

def format_result(options, doc, json):
    result = doc
    if options['--explain']:
        result['explain'] = json['debug']['explain'][doc['id']]
    if 'id' not in options['--fields']:
        del result['id']
    return result

def print_result(doc):
    for field in doc:
        print "%s: %s" % (field, doc[field])

options = docopt(__doc__, version=VERSION)
query = options['<query>']
url, params = build_http_query(options, query)
response = requests.get(url, params=params)
if options['--verbose']:
    print response.url
for doc in format_results(options, response):
    print_result(doc)
