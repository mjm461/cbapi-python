__author__ = 'bwolfson'

import sys
import optparse

# in the github repo, cbapi is not in the example directory
sys.path.append('../src/cbapi')

import cbapi

def build_cli_parser():
    parser = optparse.OptionParser(usage="%prog [options]", description="Get the a report's info from a configured feed")

    # for each supported output type, add an option
    #
    parser.add_option("-c", "--cburl", action="store", default=None, dest="server_url",
                      help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_option("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_option("-n", "--no-ssl-verify", action="store_false", default=True, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    parser.add_option("-i", "--id", action="store", default=None, dest="id",
                      help="Feed id")
    parser.add_option("-r", "--report_id", action = "store", default = None, dest = "reportid",
                      help = "Report id")
    return parser

def main(argv):
    parser = build_cli_parser()
    opts, args = parser.parse_args(argv)
    if not opts.server_url or not opts.token or not opts.id or not opts.reportid:
      print "Missing required param; run with --help for usage"
      sys.exit(-1)

    # build a cbapi object
    #
    cb = cbapi.CbApi(opts.server_url, token=opts.token, ssl_verify=opts.ssl_verify)

    curr_feeds = cb.feed_enum()
    feed_does_exist = False

    for feed in curr_feeds:
        if int(feed['id']) == int(opts.id):
            feed_does_exist = True

    if not feed_does_exist:
        print "No feed with id %s found" % opts.id
        sys.exit(-1)

    curr_reports = cb.feed_report_enum(opts.id)
    report_does_exist = False
    for report in curr_reports:
        if opts.reportid == report['id']:
            report_does_exist = True
    if not report_does_exist:
        print "No report with id %s found" % opts.reportid
        sys.exit(-1)

    # get the feed's report stats
    stats = cb.feed_report_stats(opts.id, opts.reportid)

    for key in stats.keys():
        print "%-22s : %s" % (key, stats[key])

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))