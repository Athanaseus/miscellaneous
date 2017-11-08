INPUT               =    '.'                      # Directory to output skymodel
PHASE_CENTER        =    "J2000,0deg,-30deg"      # Telescope phase centre
AREA                =    1.0                      # Observed sky area in deg^2
FREQ0               =    '1.42GHz'                # Ref-frequency of observation
LSM                 =    'skymodel.txt'           # Sky model file name
Num_Sources         =    50                       # Total number of sources to write in model
POINT_SOURCES_PER   =    100                      # Percantage of point sources (i.e. all point = 100)
Extended_size_range =    [5, 20]                  # size range for extended sources (arcsec)
NOISE               =    0.00005                  # Noise rms in Jy (None or 0 to sepecify flux range)
SNR_range           =    [5, 100]                 # Signal to Nose ration range
FLUX_range          =    [1, 1]                   # Flux range incase no noise is provided
SPI_range           =    [-0.7, -0.7]             # Spectral index range



import numpy as np


def get_ra_dec_range(area=1.0, phase_centre="J2000,0deg,-30deg"):
    """Get RA and DEC range from area of observations and phase centre"""
    ra = float(phase_centre.split(',')[1].split('deg')[0])
    dec = float(phase_centre.split(',')[2].split('deg')[0])
    d_ra = np.sqrt(area)/2
    d_dec = np.sqrt(area)/2
    ra_range = [ra-d_ra, ra+d_ra]
    dec_range = [dec-d_dec, dec+d_dec]
    return ra_range, dec_range


def get_source_shapes(scale_low_limit=5, scale_high_limit=10, angle_limit=180,
                      num_of_sources=100, point_sources=100):
    """Provides random source shapes to simulate guassian sources"""
    import random
    num_of_point = round(num_of_sources*(point_sources/100.0))
    num_of_extended = num_of_sources - num_of_point
    SHAPEs = []
    maxi = 3  # max. number of tuple indices
    for i in range(num_of_sources):
        current = []
        # add a random number of indices to the tuple
        for j in range(maxi):
            # add another number to the current list
            if j < 2:
                if num_of_extended == num_of_sources:
                    current.append(random.uniform(scale_low_limit, scale_high_limit))
                elif num_of_point == num_of_sources:
                    current.append(0)
                elif i < num_of_point:
                    current.append(0)
                else:
                    current.append(random.uniform(scale_low_limit, scale_high_limit))
            else:
                current.sort()
                current = current[::-1]  # Reverse list so that [maj, min]
                current.append(random.uniform(0, angle_limit))
        # convert current list into a tuple and add to resulting list
        SHAPEs.append(tuple(current))
    random.shuffle(SHAPEs)
    return SHAPEs


def write_skymodel_file(noise_sigma, skymodel, freq=1420000000.0, RAs=[0],
                        DECs=[-30.0], SPIs=[-0.7], SNRs=[100], point_sources=100):
    """Writes the generated sky model parameters in to a file"""
    SHAPEs = get_source_shapes(point_sources=point_sources, num_of_sources=len(SNRs))
    counter = 0
    with open(skymodel, "w") as f:
        f.write("#format: name ra_d dec_d i spi freq0 emaj_s emin_s pa_d\n")
        if len(SNRs) > 1:
            for ra, dec, spi, snr, shape in zip(RAs, DECs, SPIs, SNRs, SHAPEs):
                if shape[0] == 0 and shape[1] == 0:
                    i = snr*noise_sigma
                else:
                    i = snr*noise_sigma
                f.write("J{} {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f}\n".format(
                        counter, ra, dec, i, spi, freq, *shape))
                counter += 1
        else:
            f.write("J0 {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f}\n".format(
                           RAs[0], DECs[0], noise_sigma, SPIs[0], freq, *SHAPEs[0]))
    return skymodel.split('/')[1]


SNRs = sorted(np.random.uniform(*SNR_range, size=Num_Sources))
RAs = np.random.uniform(*get_ra_dec_range(AREA, PHASE_CENTER)[0], size=Num_Sources)
DECs = np.random.uniform(*get_ra_dec_range(AREA, PHASE_CENTER)[-1], size=Num_Sources)
SPIs = sorted(np.random.uniform(*SPI_range, size=Num_Sources))


if __name__ == '__main__':
    write_skymodel_file(NOISE, '%s/%s' %
                        (INPUT, LSM), RAs=RAs,
                        DECs=DECs, SPIs=SPIs, SNRs=SNRs,
                        point_sources=POINT_SOURCES_PER)
