import stimela

INPUT = "input"
OUTPUT = "output"
MSDIR = "msdir"
PREFIX = "ragavi"


recipe = stimela.Recipe("Stimela simulation example", ms_dir=MSDIR)

table = "meerkathi-wlm-1gc1.B0"

recipe.add("cab/ragavi", "gain_plotter",
           {
                "table"   :   "{:s}:output".format(table),
                "field"   :   0,
                "gaintype":   'B',
                "htmlname":   "test-B"
           },
           input=INPUT,
           output=OUTPUT,
           label="ragavi::ragavi")

recipe.run()
