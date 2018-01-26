import argparse
from astropy.io import fits as fitsio
from functools import partial

def casa_header_edit(fitsfile, outfile):
    """This method is specifically for casa header editing to make it
       compitible with source finder used and other libraries"""
    if os.path.isfile(fitsfile):
        with fitsio.open(fitsfile) as hdu:
            header = hdu[0].header
            del header['ORIGIN']
            header.update(ORIGIN='CASA')
            if not os.path.isfile(outfile):
                hdu.writeto(outfile)

def get_argparser():
    "Get argument parser"
    parser = argparse.ArgumentParser(
                 description="This method is specifically for casa header editing")
    argument = partial(parser.add_argument)
    argument('-i', '--image',  dest='image',
             help='Name of the CASA image fits file')
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    casa_header_edit = args.image
