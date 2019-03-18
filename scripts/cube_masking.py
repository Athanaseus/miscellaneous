from astropy.io import fits

hdr = fits.open("your-image-name.fits")
data = hdr[0].data
data[data>"countour_level_from_kvis"] = 1.0
data[data<"countour_level_from_kvis"] = 0.0
header = hdr[0].header

fits.writeto('mask-image.fits', data, header, clobber=True)
