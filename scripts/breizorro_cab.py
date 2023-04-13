import stimela


INPUT = 'input'
OUTPUT = 'output'
MSDIR = 'msdir'

IMAGE = 'I-image.fits'
THRESH = 7.0


stimela.register_globals()

recipe = stimela.Recipe('Make Mask', ms_dir=MSDIR, JOB_TYPE="singularity")

recipe.add('cab/breizorro', 'masking',
        {
            "restored-image"        :   "%s:output" % IMAGE,
            "threshold"             :    THRESH,
        },
            input=INPUT,
            output=OUTPUT,
            label='make_mask:: Breizorro')

recipe.run()
