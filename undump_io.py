#!/usr/bin/env python

# This is free and unencumbered software released into the public domain.
#
# See LICENSE for more information.
#

import os
import re
import sys
import argparse

DATA_re = re.compile(".*\(data-HEAP\): (.*)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='undump_io: extract requests from dump_io generated logfiles')
    parser.add_argument('--filter', help='Filter to apply.')
    parser.add_argument('--filter-file', help='Filename to store filtered output in')
    parser.add_argument('--no-list', action='store_true', help='Dont display a list of all requests')
    parser.add_argument('--output', help='File to write ALL requests into')
    parser.add_argument('file', help="Logfile to parse")

    args = parser.parse_args()
    reqs = {}

    if not os.path.exists(args.file):
        print("Requested logfile {} does not exist!".format(args.file))
        sys.exit(0)

    with open(args.file, 'r') as fh:
        for line in fh.readlines():
            parts = line.split("] ")
            if len(parts) != 5 or '(103)' not in parts[3]:
                continue

            dt = parts[0][1:]
            ignore, pid = parts[2].split('pid ')
            ignore, ip = parts[3].split('client ')

            uniq = "{}|{}".format(pid, ip)

            data = DATA_re.match(parts[4])
            if data is None:
                continue
            dump = data.group(1).strip()

            reqs.setdefault(uniq, {'date': dt, 'request':[]})['request'].append(dump)

    print("Total of {} requests rebuilt.".format(len(reqs)))

    if not args.no_list or args.output is not None:
        out = sys.stdout if args.output is None else open(args.output, 'w')
        for r in sorted(reqs, key=lambda x: reqs[x]['date']):
            req = reqs[r]
            pid, ip = r.split('|')
            out.write("{}: [{}]: {}\n".format(req['date'], pid, ip))
            for data in req['request']:
                out.write("    {}\n".format(data))
        if args.output is not None:
            out.close()

    if args.filter is not None:
        print("\nFiltering requests for '{}'".format(args.filter))
        hdl = sys.stdout if args.filter_file is None else open(args.filter_file, 'w')
        matches = 0
        for r in sorted(reqs, key=lambda x: reqs[x]['date']):
            req = reqs[r]
            pid, ip = r.split('|')
            r_data = "{}: [{}]: {}\n".format(req['date'], pid, ip)
            for data in req['request']:
                r_data += "    {}\n".format(data)
            if args.filter in r_data:
                hdl.write(r_data)
                matches += 1

        if args.filter_file is not None:
            hdl.close()
        print("\nTotal of {} matches for filter {}".format(matches, args.filter))
