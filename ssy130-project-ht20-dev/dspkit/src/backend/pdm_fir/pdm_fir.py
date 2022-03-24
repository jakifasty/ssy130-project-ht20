import sys
import scipy.signal as signal

PDM_FTL_TAPS       = 16
PDM_FTL_SAMPLE_F   = 1024
PDM_FTL_CUT_OFF    = 8
PDM_FTL_SCALE_BITS = 30

taps1 = signal.firwin(PDM_FTL_TAPS*16, PDM_FTL_CUT_OFF, nyq=PDM_FTL_SAMPLE_F/2)
taps  = (taps1 * (2**PDM_FTL_SCALE_BITS)).astype(int)

def print_head():
	print '/* Generated by pdm_fir.py */'
	print '#define PDM_FTL_SCALE_BITS %d' % PDM_FTL_SCALE_BITS

def print_taps():
	print 'static int const tap_coeff[PDM_FTL_TAPS*16] = {'
	print ','.join(['%i' % t for t in taps])
	print '};'

def byte_coef(i, b):
	bit, off, tot = 1<<7, i*8, 0
	while bit:
		if bit & b:
			tot += taps[off];
		else:
			tot -= taps[off];
		bit >>= 1
		off += 1
	return tot

def print_byte_coefs():
	print 'static int const byte_coeff[PDM_FTL_TAPS*2][256] = {'
	for i in range(PDM_FTL_TAPS*2):
		print ' { // [%i]' % i
		print ','.join(['%i' % byte_coef(i, b) for b in range(256)])
		print ' },'
	print '};'

if __name__ == '__main__':
	if 'plot' in sys.argv:
		import numpy as np
		from matplotlib.pylab import *
		title('Digital filter frequency response')
		w, h = signal.freqz(taps1)
		plot(w*PDM_FTL_SAMPLE_F/(2*np.pi), np.abs(h), 'b')
		ylabel('Amplitude')
		yscale('log')
		xlabel('Frequency (kHz)')
		xlim(0, PDM_FTL_SAMPLE_F/2)
		show()
	else:
		print_head()
		# print_taps()
		print_byte_coefs()

