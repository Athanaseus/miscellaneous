import stimela


INPUT = 'input'
OUTPUT = 'output'
MSDIR = 'msdir'

IMAGE = ''
PIX_THRESH = 10
ISL_THRESH = 5


stimela.register_globals()

recipe = stimela.Recipe('Source Finder', ms_dir=MSDIR)

recipe.add('cab/pybdsm', 'source_finder',
        {
            "filename"        :   "%s:output" % IMAGE,
            "outfile"         :   "pybdsm_%s" % IMAGE[:-5],
            "thresh_pix"      :    PIX_THRESH,
            "thresh_isl"      :    ISL_THRESH,
            "clobber"         :    True,
            "adaptive_rms_box":    True,
            "catalog_type"    :    "gaul",
        },
            input=INPUT,
            output=OUTPUT,
            label='src_finder:: Sourcery')

recipe.run()
