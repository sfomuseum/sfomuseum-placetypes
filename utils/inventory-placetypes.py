#!/usr/bin/env python

import os
import sys
import logging
import json

import mapzen.whosonfirst.utils

if __name__ == "__main__":

    import optparse
    opt_parser = optparse.OptionParser()

    # opt_parser.add_option('-R', '--repo', dest='repo', action='store', default=None, help='Path to a valid WOF repo - this takes precedence over options.source, options.csv and options.name-template and assumes that options.repo has both a data and a meta directory')

    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')
    options, args = opt_parser.parse_args()

    if options.verbose:	
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    whoami = os.path.abspath(sys.argv[0])
    utils = os.path.dirname(whoami)
    root = os.path.dirname(utils)

    placetypes = os.path.join(root, "placetypes")

    for repo in args:

        repo = os.path.abspath(repo)
        data = os.path.join(repo, "data")

        crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)

        for feature in crawl:

            props = feature["properties"]
            sfom_placetype = props.get("sfomuseum:placetype", None)

            if not sfom_placetype:
                continue

            fname = "%s.json" % sfom_placetype
            spec = os.path.join(placetypes, fname)

            if os.path.exists(spec):
                continue

            wof_placetype = props.get("wof:placetype", "")
            
            id = mapzen.whosonfirst.utils.generate_id()
            
            pt = {
	        "sfomuseum:id": id,
	        "sfomuseum:name": sfom_placetype,
	        "sfomuseum:role": "common_optional",
	        "sfomuseum:parent": [ ],
                "sfomuseum:concordances": {
                    "wof:placetype": wof_placetype
                }
            }

            fh = open(spec, "w")
            json.dump(pt, fh, indent=2)

            fh.close()
            logging.info("wrote %s (%s)" % (spec, id))
                
        
