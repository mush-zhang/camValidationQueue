"""
This module uses Streamlink to find a livestream src URL on a webpage.

*****************************
Command Line Usage: python fetchstreamsrc.py [WEBPAGE]
Arguments:
    In the main function, user can set duration, framePerSecond, and output filename.
** WARNING ** This is currently a WIP script and IS NOT ROBUST.

******************************
    ** THE CAM2 PROJECT **
******************************
Authors: Caleb Tung,
Created: 6/17/2017
Updated by: Jia En Chua,
Updated on: 7/18/2018

"""

from __future__ import print_function # Force the use of Python3.x print()

import re
import sys
import streamlink
from pprint import pprint as pp
from subprocess import call


def __select_stream(page_streams):
    """
    HELPER selects the desired stream src given a Stream dictionary

    param: page_streams the Stream dictionary
    return: the selected URL, or None on fail
    """

    # TODO: Figure out how to handle multiple different streams (not just one stream
    #       with multiple resolutions
    src_url = None

    if len(page_streams) >= 1:
        if '720p' in page_streams: # Default choose the stream with best resolution
            # pp(page_streams)
            src_url = page_streams['720p'].url
        else: # No 'best' resolution was determined
            unused_key, stream_val = page_streams.popitem() # Just get the first one
            src_url = stream_val.url

    return src_url


def get_stream_src_from_url(page_url):
    """
    Fetches the source URL of a livestream on a given webpage

    param: page_url the URL of the webpage with a livestream on it
    return: the URL of the livestream source, or None on fail
    """

    src_url = None # The source URL to return

    try:
        page_streams = streamlink.streams(page_url) # Get a dictionary of all streams

        # TODO: Find a way to collect the frame width and height, along with FPS, if
        #       possible.  Might need to use FFmpeg?

        src_url = __select_stream(page_streams)

    except streamlink.exceptions.PluginError as perr:
        # If no suitable URL can be confirmed, Streamlink may suggest a potential one
        # e.g. //bla.com/stream.m3u8 which is perfectly legit once 'http:' is prepended
        # Extract it from the error message with regex
        src_url_match = re.search(r"Invalid URL '(.*?)'", str(perr), re.M|re.I)
        if src_url_match != None:
            src_url = 'http:' + str(src_url_match.group(1))

            # TODO: Implement check to see if http:// needs to be prepended

    return src_url


def getImages_from_stream(page_url, duration, framesPerSec, outputfile):
    hls_url = get_stream_src_from_url(page_url)
    call(["ffmpeg", "-i", hls_url, "-vf", "fps=" + framesPerSec, "-t", duration, "-y", "Outputs/" + outputfile + "%d.jpg"])



if __name__ == '__main__':
    EXPECTED_NUM_ARGS = 1 + 1

    hls_url = None
    fps = "2"
    duration = "5"
    outputfile = "result"
    if len(sys.argv) < EXPECTED_NUM_ARGS:
        print('Expected ' + str(+ EXPECTED_NUM_ARGS-1) + ' cmd line args.')
    else:
        hls_url = get_stream_src_from_url(sys.argv[1])

    if hls_url:
        getImages_from_stream(hls_url, duration, fps, outputfile)
