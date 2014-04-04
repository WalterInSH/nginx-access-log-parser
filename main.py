__author__ = "Richard O'Dwyer"
__email__ = "richard@richard.do"
__license__ = "None"

import re


def process_log(log):
    requests = get_requests(log)
    files = get_files(requests)
    totals = file_occur(files)
    return totals


def get_requests(f):
    log_line = f.read()
    pat = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s'  #IP address
           '\[(.+)\]\s'  #datetime
           '"GET\s(.+)\s\w+/.+"\s\d+\s'  #requested file
           '\d+\s"(.+)"\s'  #referrer
           '"(.+)"'  #user agent
    )
    requests = find(pat, log_line, None)
    return requests


def find(pat, text, match_item):
    match = re.findall(pat, text)
    if match:
        return match
    else:
        return False


def get_files(requests):
    #get requested files with req
    requested_files = []
    for req in requests:
        #req[2] for req file match, change to
        #data you want to count totals
        requested_files.append(req[2])
    return requested_files


def file_occur(files):
    #file occurrences in requested files
    d = {}
    for file in files:
        file = file.split('?')[0]
        d[file] = d.get(file, 0) + 1
    return d


if __name__ == '__main__':
    pv_suffix = None
    url_ignore = (".jpg", ".png", ".json", ".css", ".js")
    #nginx access log, standard format
    log_file = open('access.log', 'r')

    #return dict of files and total requests
    records = process_log(log_file).items()
    for url, value in records:
        #skip ignored files
        if url.endswith(url_ignore):
            continue
        print(url + " - " + str(value))


