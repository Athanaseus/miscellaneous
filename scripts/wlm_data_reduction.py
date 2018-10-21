# WLM Data Redution using CASA

# Open CASA from terminal. NB: All tasks will be run in one-liner mode. 
$ casa

####################
#     Summary      #
####################

# Observation info
listobs('wlm.ms')

# plot antenna positions
plotants('wlm.ms')

# plot observation uv-coverage
plotuv('wlm.ms')

# plot amplitude vs time of the entire observation for all fields
plotms(vis='wlm.ms',xaxis='time',yaxis='amplitude')

####################
#   Visualization  #
####################

# Plot amplitude against baselines for calibrators (fields 0 & 2 & 3)
plotms(vis='wlm.ms', xaxis='baseline', yaxis='amplitude', field = '0')
plotms(vis='wlm.ms', xaxis='baseline', yaxis='amplitude', field = '3')
plotms(vis='wlm.ms', xaxis='baseline', yaxis='amplitude', field = '2')

# Plot amplitude against frequency for calibrators (fields 0 & 2 & 3)
plotms(vis='wlm.ms', xaxis='frequency', yaxis='amplitude', field = '0')
plotms(vis='wlm.ms', xaxis='frequency', yaxis='amplitude', field = '3')
plotms(vis='wlm.ms', xaxis='frequency', yaxis='amplitude', field = '2')

 #---------------
 #  Flagging    \
 #---------------
 
# Start with manual flagging
# Visualize of correlations of the callibrator and iterate for each baseline 
plotms(vis='wlm.ms', xaxis='channel', yaxis='amplitude', iteraxis='baseline', field = '0', correlation='XX')
plotms(vis='wlm.ms', xaxis='channel', yaxis='amplitude', iteraxis='baseline', field = '0', correlation='YY')
plotms(vis='wlm.ms', xaxis='channel', yaxis='amplitude', iteraxis='baseline', field = '3', correlation='XX')
plotms(vis='wlm.ms', xaxis='channel', yaxis='amplitude', iteraxis='baseline', field = '3', correlation='YY')

# Here you can further explore automatic flagging [Tfcrop, aoflagger, etc]

# chop of bandpass roll-off
flagdata(vis='wlm.ms', spw=[0:0~150, 0:3946~4095])

# unflagging frequency of interset
flagdata(vis='wlm.ms', mode='unflag', spw='0:1419.8~1421.6MHz', field='1')

# Calibrator scans [1, 7, 15, 23, 31]



#########################
#      Calibration      #
#########################


# Ensure no calibration is performed on the data previously
clearcal('wlm.ms')

# Set junsky to the obs data using the flux calibrator standard model J1938-6341
setjy(vis='wlm.ms', field='J1938-6341', fluxdensity=-1, standard='Perley-Butler 2010')

# Delay calibration
gaincal(vis='wlm.ms', caltable='Ktable', field='0,1,2,3', gaintype='K', solint='64s', refant='m000', combine='scan', minblperant=1, solnorm=False, minsnr=5, calmode='ap')

# Plot the delay solutions
plotcal(caltable='Ksoln', xaxis='time', yaxis='delay', iteration='antenna', subplot=421) 

# Bandpass calibration
bandpass(vis='wlm.ms', caltable='btable', field='0', refant='m000', combine='scan', solint='32s', bandtype='B', minsnr=5, gaintable = ['Ksoln'], interp = ['linear', 'nearest'])

# Gain calibration
gaincal(vis='wlm.ms', field='0', caltable='gain', refant='m000', calmode='p', gaintable='Ksoln1',interp='linear',gaintype='G', gaintable=['ktable', 'btable'])

######## Sandeep

prefix = 'wlm'

# Set up some useful variables (these will also be set later on)
msfile = prefix + '.ms'
ktable = prefix + '.delaycal'
btable = prefix + '.bcal'
gtable = prefix + '.gcal'
ftable = prefix + '.fluxscale'
splitms = prefix + '.src.split.ms'
imname = prefix + '.cleanimg'


# This is MeerKAT and PKS1934-638 is sufficiently unresolved
# that we dont need a model image.  For higher frequencies
# you would want to use one.
#modimage = ''
# Setjy knows about this source so we dont need anything more
setjy(vis=msfile, field='J1938-6341', fluxdensity=-1, standard='Perley-Butler 2010')

# Delay calibration
gaincal(vis='wlm.ms', caltable=ktable, field='0,1,2,3', gaintype='K', solint='inf', refant='m000', combine='scan', minblperant=1, solnorm=False, minsnr=5, calmode='ap')
# Plot the delay solutions
plotcal(caltable=ktable, xaxis='time', yaxis='delay', iteration='antenna', subplot=821)

# Bandpass calibration
# We can first do the bandpass on the single 5min scan on PKS1938-6341
# At 1.21GHz phase stablility should be sufficient to do this without
# a first (rough) gain calibration.  This will give us the relative
# antenna gain as a function of frequency.
bandpass(vis=msfile, caltable=btable, field='0', refant='m000', combine='scan', solint='inf', bandtype='B', minsnr=5, gaintable = [ktable], interp = ['linear', 'nearest'])

# Gain calibration
# Armed with the bandpass and delay, we now solve for the
# time-dependent antenna gains
gaincal(vis=msfile, field='0,2', caltable=gtable, refant='m000', gaintable='Ksoln1', interp='nearest', gaintype='G', calmode='ap', solint='inf', gaintable = [ktable, btable])

# Bootstrap flux scale
# we will be using PKS1934-638 (the source we did setjy on) as
# our flux standard reference - note its extended name as in
# the FIELD table summary above
# we want to transfer the flux to our other gain cal source PKS2326-477
fluxscale(vis=msfile, fluxtable=ftable, reference='J1938-6341')
default('fluxscale')

vis = msfile

# set the name for the output rescaled caltable
ftable = prefix + '.fluxscale'
fluxtable = ftable

# point to our first gain cal table
caltable = gtable

# we will be using PKS1934-638 (the source we did setjy on) as
# our flux standard reference - note its extended name as in
# the FIELD table summary above 
reference = 'PKS1934-638'

# we want to transfer the flux to our other gain cal source PKS2326-477
transfer = 'PKS2326-477'

saveinputs('fluxscale',prefix+'.fluxscale.saved')

inp()

fluxscale()

