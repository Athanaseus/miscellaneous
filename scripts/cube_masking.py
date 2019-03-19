from astropy.io import fits
import argparse
from functools import partial
from astropy.io import fits as fitsio


def cube_masking(cube_name, threshold, out_mask=None):
    "Create a mask from a cube image"
    hdr = fits.open(cube_name)
    data_cube = hdr[0].data
    data[data>threshold] = 1.0
    data[data<threshold] = 0.0

    header = hdr[0].header
    if out_mask is None:
        out_mask = '{}-mask.fits'.format(cube_name.split('.fits')[0])
    fits.writeto(out_mask, data, header, clobber=True)


def get_argparser():
    "Get argument parser"
    parser = argparse.ArgumentParser(
                 description="This method is specifically for casa header editing")
    argument = partial(parser.add_argument)
    argument('-i', '--image',  dest='image', help='Name of the CASA image fits file')
    argument('-o', '--out-mask',  dest='out', help='Name of the CASA output image fits file')
    argument('-t', '--threshold',  dest='thresh', help='Threshold value in units of Jy/beam')
    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()
    cube_masking(args.image, args.thresh, args.out)


if __name__ == '__main__':
    main()
