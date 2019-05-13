import stimela

INPUT = 'input'
OUTPUT = 'output'
MSDIR = 'msdir'

HI_CUBE = 'wlm_60.fits'
OUT_MASK = 'wlm_60.mask'

recipe = stimela.Recipe('Sofia Mask and Mom0 map', ms_dir=MSDIR)

step = 'sofia_sources'
recipe.add('cab/sofia', step,
           {
            "import.inFile"         : HI_CUBE+':output',
            "steps.doFlag"          : False,
            "steps.doScaleNoise"    : True,
            "steps.doSCfind"        : True,
            "steps.doMerge"         : True,
            "steps.doReliability"   : False,
            "steps.doParameterise"  : False,
            "steps.doWriteMask"     : True,
            "steps.doMom0"          : True,
            "steps.doMom1"          : False,
            "steps.doWriteCat"      : False,
            "flag.regions"          : [],
            "scaleNoise.statistic"  : 'mad',
            "SCfind.threshold"      : 5,
            "SCfind.rmsMode"        : 'mad',
            "merge.radiusX"         : 2,
            "merge.radiusY"         : 2,
            "merge.radiusZ"         : 2,
            "merge.minSizeX"        : 2,
            "merge.minSizeY"        : 2,
            "merge.minSizeZ"        : 2,
            "merge.minVoxels"       : 1,
            "merge.maxVoxels"       : -1,
            "writeCat.basename"     : OUT_MASK,
           },
            input=INPUT,
            output=OUTPUT,
            label='{0:s}:: Make SoFiA mask and images'.format(step))

recipe.run()
