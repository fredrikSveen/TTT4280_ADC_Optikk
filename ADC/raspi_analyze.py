import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

plt.rcParams.update({'font.size': 20})
tall = 1


def raspi_import(path, channels=5):
    """
    Import data produced using adc_sampler.c.
    Returns sample period and ndarray with one column per channel.
    Sampled data for each channel, in dimensions NUM_SAMPLES x NUM_CHANNELS.
    """

    with open(path, 'r') as fid:
        sample_period = np.fromfile(fid, count=1, dtype=float)[0]
        data = np.fromfile(fid, dtype=np.uint16)
        data = data.reshape((-1, channels))
    return sample_period, data


# Import data from bin file
sample_period, data = raspi_import('sampling_output.bin')

#data = signal.detrend(data, axis=0)  # removes DC component for each channel
print(sample_period)
sample_period *= 1e-6  # change unit to micro seconds

# Generate time axis
num_of_samples = data.shape[0]  # returns shape of matrix
t = np.linspace(start=0, stop=num_of_samples*sample_period, num=num_of_samples)

data2 = signal.detrend(data, axis=0)  # removes DC component for each channel

# Generate frequency axis and take FFT
freq = np.fft.fftfreq(n=num_of_samples, d=sample_period)
spectrum = np.fft.fft(data2, axis=0)  # takes FFT of all channels


# Plot the results in two subplots
# NOTICE: This lazily plots the entire matrixes. All the channels will be put into the same plots.
# If you want a single channel, use data[:,n] to get channel n
plt.subplot(2, 1, 1)
plt.title("Samplet signal i tidsdomene")
plt.xlabel("Tid [s]")
plt.ylabel("Volt [V]")

# Loop to be able to name all the graphs.
for i in range(0,5):
    graf = []
    for j in range(0, len(data)):
        graf.append(data[j][i]*5/4096)
    plt.plot(t[1:9375], graf[1:9375], label="ADC"+str(i+1))
    
plt.legend()

plt.subplot(2, 1, 2)
plt.title("Frekvensspektrum")
plt.xlabel("Frekvens [Hz]")
plt.ylabel("Energi [dB]")
plt.plot(freq, 20*np.log10(np.abs(spectrum))) # get the power spectrum

plt.show()
