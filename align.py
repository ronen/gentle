import argparse
import logging
import multiprocessing
import os
import sys

import gentle

parser = argparse.ArgumentParser(
        description='Align a transcript to audio by generating a new language model.  Outputs JSON')
parser.add_argument(
        '--nthreads', default=multiprocessing.cpu_count(), type=int,
        help='number of alignment threads')
parser.add_argument(
        '--arate', default=8000, type=int,
        help='audio sampling rate')
parser.add_argument(
        '-o', '--output', metavar='output', type=str, 
        help='output filename')
parser.add_argument(
        '--conservative', dest='conservative', action='store_true',
        help='conservative alignment')
parser.set_defaults(conservative=False)
parser.add_argument(
        '--disfluency', dest='disfluency', action='store_true',
        help='include disfluencies (uh, um) in alignment')
parser.set_defaults(disfluency=False)
parser.add_argument(
        '--log', default="INFO",
        help='the log level (DEBUG, INFO, WARNING, ERROR, or CRITICAL)')
parser.add_argument(
        'audiofile', type=str,
        help='audio file')
parser.add_argument(
        'txtfile', type=str,
        help='transcript text file')
args = parser.parse_args()

log_level = args.log.upper()
logging.getLogger().setLevel(log_level)

disfluencies = set(['uh', 'um'])

def on_progress(p):
    for k,v in p.items():
        logging.debug("%s: %s" % (k, v))


with open(args.txtfile) as fh:
    transcript = fh.read()

gentle.config.arate=args.arate

logging.info("converting audio to %d sampled wav" % args.arate)

with gentle.resampled(args.audiofile) as wavfile:
    logging.info("starting alignment")
    aligner = gentle.ForcedAligner(transcript, nthreads=args.nthreads, disfluency=args.disfluency, conservative=args.conservative, disfluencies=disfluencies)
    result = aligner.transcribe(wavfile, progress_cb=on_progress, logging=logging)

fh = open(args.output, 'w') if args.output else sys.stdout
fh.write(result.to_json(indent=2))
if args.output:
    logging.info("output written to %s" % (args.output))
