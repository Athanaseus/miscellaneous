import stimela

INPUT = "input"
OUTPUT = "output"
MSDIR = "msdir"
PREFIX = "calibration"

recipe = stimela.Recipe("Stimela simulation example", ms_dir=MSDIR)


MS_meq = 'meerkat_SourceRecovery_meqtrees.ms'
MS_cub = 'meerkat_SourceRecovery_cubical.ms'
PREFIX_meq = MS_meq[:-3]
PREFIX_cub = MS_cub[:-3]
LSM = 'skymodel.txt'
FREQ0 = '1.42GHz'
PHASE_CENTER = "J2000,0deg,-30deg"

TEL_NAME = 'meerkat'    # Telescope name
SYN_TIME = 2            # Sythesis time in hours
INT_TIME = 60           # Integration time
SMEARING = False        # Source time and bandwidth smearing
SEFD = 551              # Spectral Flux Energy Density
delta_freq = 2          # Channel width in MHz
IN_CHAN = 16            # Number of input channels
OUT_CHAN = 4            # Number of output channels
delta_freq = 2          # Channel width in MHz
POINT_SOURCES = 100     # Number of point source (i.e if 0% only extended sources)
NPIX = 4096             # Number of pixels
CELL_SIZE = 1.0         # Pixel size
NITERS = 20000          # Number of cleaning iterations
LOOP_GAIN = 0.1         # Cleaning loop gain
IM_WEIGHT = 'uniform'   # Imaging weighting
BRIGGS_robust = -2      # Robust parameter
ISL_THRESH = 10.0       # Island detection threshold sigma
PIX_THRESH = 20.0       # Pixel detection threshold in sigma
CATALOG_TYPE = 'gaul'   # Sourcery output catalog type

# Create simulated Measurement Set (MS)
recipe.add("cab/simms", "make_simulated_meq_ms", {
    "msname"    :   MS_meq,
    "telescope" :   TEL_NAME,
    "synthesis" :   SYN_TIME,  # in hours
    "dtime"     :   INT_TIME,  # in seconds
    "freq0"     :   FREQ0,
    "dfreq"     :   "{}MHz".format(delta_freq),
    "nchan"     :   IN_CHAN,
    },
    input=INPUT,
    output=OUTPUT,
    label="Making simulated MS = %s" % PREFIX_meq)


recipe.add("cab/simms", "make_simulated_cub_ms", {
    "msname"    :   MS_cub,
    "telescope" :   TEL_NAME,
    "synthesis" :   SYN_TIME,  # in hours
    "dtime"     :   INT_TIME,  # in seconds
    "freq0"     :   FREQ0,
    "dfreq"     :   "{}MHz".format(delta_freq),
    "nchan"     :   IN_CHAN,
    },
    input=INPUT,
    output=OUTPUT,
    label="Making simulated MS = %s" % PREFIX_cub)

# 2: Add noise and calibration (propagation) effects to MS
recipe.add("cab/simulator", "simulate_meq_noise", {
    "msname"    :   MS_meq,
    "skymodel"  :   LSM,
    "addnoise"  :   True,
    "sefd"      :   SEFD,
    "Gjones"    :   True,
    "gain-max-period" : 4,
    "gain-min-period" : 1,
    "phase-max-period": 4,
    "phase-min-period": 1,
    "column"    :   "DATA",
    },
    input=INPUT,
    output=OUTPUT,
    label="Add noise and propagation effects to %s" % PREFIX_meq)

recipe.add("cab/simulator", "simulate_cub_noise", {
    "msname"    :   MS_cub,
    "skymodel"  :   LSM,
    "addnoise"  :   True,
    "sefd"      :   SEFD,
    "Gjones"    :   True,
    "column"    :   "DATA",
    },
    input=INPUT,
    output=OUTPUT,
    label="Add noise and propagation effects to %s" % PREFIX_cub)


# 3: Image corrupted data

recipe.add('cab/wsclean', 'image_wsclean_meq', dict({
    "msname"                :   MS_meq,
    "prefix"                :   PREFIX_meq,
    "column"                :   "DATA",
    "niter"                 :   20000,
    "auto-threshold"        :   0.5,
    "auto-mask"             :   3,
    "channelsout"           :   OUT_CHAN,
    "npix"                  :   NPIX,
    "cellsize"              :   "%sasec" % CELL_SIZE,
    "weight"                :   IM_WEIGHT,
    "joinchannels"          :   True if OUT_CHAN > 1 else False,
    }.items() + ({
     "weight": '%s %s' % (IM_WEIGHT, BRIGGS_robust)}.items()
                        if IM_WEIGHT == 'briggs' else {}.items())),
    input=INPUT,
    output=OUTPUT,
    label='image_wsclean_meq:: %s image data' % PREFIX_meq)


recipe.add('cab/wsclean', 'image_wsclean_cub', dict({
    "msname"                :   MS_cub,
    "prefix"                :   PREFIX_cub,
    "column"                :   "DATA",
    "niter"                 :   20000,
    "auto-threshold"        :   0.5,
    "auto-mask"             :   3,
    "channelsout"           :   OUT_CHAN,
    "npix"                  :   NPIX,
    "cellsize"              :   "%sasec" % CELL_SIZE,
    "weight"                :   IM_WEIGHT,
    "joinchannels"          :   True if OUT_CHAN > 1 else False,
    }.items() + ({
     "weight": '%s %s' % (IM_WEIGHT, BRIGGS_robust)}.items()
                        if IM_WEIGHT == 'briggs' else {}.items())),
    input=INPUT,
    output=OUTPUT,
    label='image_wsclean_cub:: %s image data' % PREFIX_cub)

# 4: Make image and residual cubes

recipe.add('cab/fitstool', 'meq_image_cubes', {
     "image"        : [PREFIX_meq+'-{0:04d}-image.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_meq+'-cube.image.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='meq_image_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_meq))

recipe.add('cab/fitstool', 'meq_residual_cubes', {
     "image"        : [PREFIX_meq+'-{0:04d}-residual.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_meq+'-cube.residual.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='meq_residuals_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_meq))


recipe.add('cab/fitstool', 'cub_image_cubes', {
     "image"        : [PREFIX_cub+'-{0:04d}-image.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_cub+'-cube.image.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='cub_images_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_cub))

recipe.add('cab/fitstool', 'cub_residual_cubes', {
     "image"        : [PREFIX_cub+'-{0:04d}-residual.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_cub+'-cube.residual.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='cub_residuals_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_meq))


# 5: Source Finding

meq_image = 'meerkat_SourceRecovery_meqtrees-cube.image.fits'
recipe.add('cab/pybdsm', 'source_finder_meq', {
    "filename"              :   '%s:output' % meq_image,
    "outfile"               :   MS_meq[:-3],
    "thresh_pix"            :   PIX_THRESH,
    "thresh_isl"            :   ISL_THRESH,
    "group_by_isl"          :   True,
    "spectralindex_do"      :   True if OUT_CHAN > 1 else False,
    "multi_chan_beam"       :   True if OUT_CHAN > 1 else False,
    "clobber"               :   True,
    "catalog_type"          :   CATALOG_TYPE,
    "adaptive_rms_box"      :   True,
    "blank_limit"           :   1e-9,
    },
    input=INPUT,
    output=OUTPUT,
    label='src_finder_%s:: Source finder' % meq_image)

cub_image = 'meerkat_SourceRecovery_cubical-cube.image.fits'
recipe.add('cab/pybdsm', 'source_finder_cub', {
    "filename"              :   '%s:output' % cub_image,
    "outfile"               :   MS_cub[:-3],
    "thresh_pix"            :   PIX_THRESH,
    "thresh_isl"            :   ISL_THRESH,
    "group_by_isl"          :   True,
    "spectralindex_do"      :   True if OUT_CHAN > 1 else False,
    "multi_chan_beam"       :   True if OUT_CHAN > 1 else False,
    "clobber"               :   True,
    "catalog_type"          :   CATALOG_TYPE,
    "adaptive_rms_box"      :   True,
    "blank_limit"           :   1e-9,
    },
    input=INPUT,
    output=OUTPUT,
    label='src_finder_%s:: Source finder' % cub_image)


# 6: Calibration

# MeqTrees

recipe.add('cab/calibrator', 'meq_cal', {
    "skymodel"             : '{0:s}.lsm.html:output'.format(MS_meq[:-3]),
    "model-column"         : "MODEL_DATA",
    "msname"               : MS_meq,
    "threads"              : 4,
    "column"               : "DATA",
    "output-data"          : "CORR_DATA",
    "output-column"        : "CORRECTED_DATA",
    "prefix"               : PREFIX_meq,
    "label"                : "cal{0:d}".format(1),
    "read-flags-from-ms"   : True,
    "read-flagsets"        : "-stefcal",
    "write-flagset"        : "stefcal",
    "write-flagset-policy" : "replace",
    "Gjones"               : True,
    "Gjones-solution-intervals" : [30, 0],
    "Gjones-matrix-type"   : "GainDiag",
    "Gjones-ampl-clipping"      : True,
    "Gjones-ampl-clipping-low"  : 0.5,
    "Gjones-ampl-clipping-high" : 1.5,
    "make-plots"           : True,
    "tile-size"            : 4,
   },
    input=INPUT,
    output=OUTPUT,
    label="meq_cal:: Calibrate ms={0:s}".format(MS_meq))

# Cubucal

recipe.add('cab/cubical', 'cub_cal', {
    "data-ms"          : MS_cub,
    "data-column"      : 'DATA',
    "out-model-column" : 'MODEL_DATA',
    "sol-term-iters"   : '200',
    "data-time-chunk"  : 32,
    "dist-ncpu"        : 2,
    "sol-jones"        : 'G',
    "model-list"       : '{0:s}.lsm.html:output'.format(MS_cub[:-3]),
    "out-name"         : PREFIX_cub,
    "out-mode"         : 'sr',
    "out-plots"        : True,
    "weight-column"    : 'WEIGHT',
    "montblanc-dtype"  : 'float',
    "g-solvable"       : True,
    "g-type"           : 'complex-2x2',
    "g-time-int"       : 8,
    "g-freq-int"       : 8,
    "g-clip-low"       : 0.5,
    "g-clip-high"      : 1.5,
    "g-max-prior-error": 1000,
    "g-max-post-error" : 1000
    },
    input=INPUT,
    output=OUTPUT,
    shared_memory='2Gb',
    label="cub_cal:: Calibrate ms={0:s}".format(MS_cub))

# 7 Image Corrected DATA

recipe.add('cab/wsclean', 'image_wsclean_meq_cal', dict({
    "msname"                :   MS_meq,
    "prefix"                :   PREFIX_meq+'-cal',
    "column"                :   "CORRECTED_DATA",
    "niter"                 :   20000,
    "auto-threshold"        :   0.5,
    "auto-mask"             :   3,
    "channelsout"           :   OUT_CHAN,
    "npix"                  :   NPIX,
    "cellsize"              :   "%sasec" % CELL_SIZE,
    "weight"                :   IM_WEIGHT,
    "joinchannels"          :   True if OUT_CHAN > 1 else False,
    }.items() + ({
     "weight": '%s %s' % (IM_WEIGHT, BRIGGS_robust)}.items()
                        if IM_WEIGHT == 'briggs' else {}.items())),
    input=INPUT,
    output=OUTPUT,
    label='image_wsclean_meq_cal:: %s image data' % PREFIX_meq)


recipe.add('cab/wsclean', 'image_wsclean_cub', dict({
    "msname"                :   MS_cub,
    "prefix"                :   PREFIX_cub+'-cal',
    "column"                :   "CORRECTED_DATA",
    "niter"                 :   20000,
    "auto-threshold"        :   0.5,
    "auto-mask"             :   3,
    "channelsout"           :   OUT_CHAN,
    "npix"                  :   NPIX,
    "cellsize"              :   "%sasec" % CELL_SIZE,
    "weight"                :   IM_WEIGHT,
    "joinchannels"          :   True if OUT_CHAN > 1 else False,
    }.items() + ({
     "weight": '%s %s' % (IM_WEIGHT, BRIGGS_robust)}.items()
                        if IM_WEIGHT == 'briggs' else {}.items())),
    input=INPUT,
    output=OUTPUT,
    label='image_wsclean_cub:: %s image data' % PREFIX_cub)

# 4: Make image and residual cubes

recipe.add('cab/fitstool', 'meq_cal_image_cubes', {
     "image"        : [PREFIX_meq+'-cal-{0:04d}-image.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_meq+'-cal-cube.image.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='meq_cal_image_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_meq))

recipe.add('cab/fitstool', 'meq_cal_residual_cubes', {
     "image"        : [PREFIX_meq+'-cal-{0:04d}-residual.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_meq+'-cal-cube.residual.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='meq_cal_residuals_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_meq))


recipe.add('cab/fitstool', 'cub_cal_image_cubes', {
     "image"        : [PREFIX_cub+'-cal-{0:04d}-image.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_cub+'-cal-cube.image.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='cub_cal_images_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_cub))

recipe.add('cab/fitstool', 'cub_cal_residual_cubes', {
     "image"        : [PREFIX_cub+'-cal-{0:04d}-residual.fits:output'.format(d) for d in xrange(OUT_CHAN)],
     "output"       : PREFIX_cub+'-cal-cube.residual.fits',
     "stack"        : True,
     "delete-files" : True,
     "fits-axis"    : 'FREQ',
    },
    input=INPUT,
    output=OUTPUT,
    label='cub_cal_residuals_cubes:: Make {0:s} cube from wsclean'.format(PREFIX_cub))


# 5: Source Finding

meq_image = 'meerkat_SourceRecovery_meqtrees-cube.image.fits'
recipe.add('cab/pybdsm', 'source_finder_meq_cal', {
    "filename"              :   '%s:output' % meq_image,
    "outfile"               :   MS_meq[:-3]+'-cal',
    "thresh_pix"            :   PIX_THRESH,
    "thresh_isl"            :   ISL_THRESH,
    "group_by_isl"          :   True,
    "spectralindex_do"      :   True if OUT_CHAN > 1 else False,
    "multi_chan_beam"       :   True if OUT_CHAN > 1 else False,
    "clobber"               :   True,
    "catalog_type"          :   CATALOG_TYPE,
    "adaptive_rms_box"      :   True,
    "blank_limit"           :   1e-9,
    },
    input=INPUT,
    output=OUTPUT,
    label='src_finder_cal_%s:: Source finder' % meq_image)

cub_image = 'meerkat_SourceRecovery_cubical-cube.image.fits'
recipe.add('cab/pybdsm', 'source_finder_cub_cal', {
    "filename"              :   '%s:output' % cub_image,
    "outfile"               :   MS_cub[:-3]+'-cal',
    "thresh_pix"            :   PIX_THRESH,
    "thresh_isl"            :   ISL_THRESH,
    "group_by_isl"          :   True,
    "spectralindex_do"      :   True if OUT_CHAN > 1 else False,
    "multi_chan_beam"       :   True if OUT_CHAN > 1 else False,
    "clobber"               :   True,
    "catalog_type"          :   CATALOG_TYPE,
    "adaptive_rms_box"      :   True,
    "blank_limit"           :   1e-9,
    },
    input=INPUT,
    output=OUTPUT,
    label='src_finder_cal_%s:: Source finder' % cub_image)



#recipe.run(steps=[14]) cubical
recipe.run()
steps = [
         "make_simulated_meq_ms",
         "make_simulated_cub_ms",
         "simulate_meq_noise",
         "simulate_cub_noise",
         "image_wsclean_meq",
         "image_wsclean_cub",
         "src_finder_%s" % meq_image,
         "src_finder_%s" % cub_image,
        ]
