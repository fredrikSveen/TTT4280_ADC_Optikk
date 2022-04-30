import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

plt.rcParams.update({'font.size': 23})

#transmittans
# pulsklokke = [75,75,76,73,74,73]

#reflektans
pulsklokke = [74,70,75,75,75]

r_pulser = []
g_pulser = []
b_pulser = []

for i in range(1,6):
    data1 = []
    #Bruk for transmittans målinger
#     if i == 5:
#         i=6
#     filename = "sample"+str(i)+".txt"

    #bruk for reflektans målinger
    filename = "reflektans/reflektans_"+str(i)+".txt"

    with open(filename) as file:
        lines = file.readlines()
        
    for i in lines:
        data1.append(i.split(" "))

    data = signal.detrend(data1, axis=0)

    sample_period = 1/40  # change unit to micro seconds

    # Generate time axis
    num_of_samples = data.shape[0]  # returns shape of matrix
    t = np.linspace(start=0, stop=num_of_samples*sample_period, num=num_of_samples)

    # Generate frequency axis and take FFT
    freq = np.fft.fftfreq(n=num_of_samples, d=sample_period)
    spectrum = np.fft.fft(data, axis=0)
        
    red = [float(p[0]) for p in data]
    green = [float(p[1]) for p in data]
    blue = [float(p[2]) for p in data]
    t = np.linspace(0, 10, len(red))
    
    plt.subplot(3, 1, 1)
    plt.title("Rød kanal fra video.")
    plt.xlabel("Tid [s]")
    plt.ylabel("Styrke")
    plt.plot(t,red, color="r")
    
    plt.subplot(3, 1, 2)
    plt.title("Grønn kanal fra video.")
    plt.xlabel("Tid [s]")
    plt.ylabel("Styrke")
    plt.plot(t, green, color="g")
    
    plt.subplot(3, 1, 3)
    plt.title("Blå kanal fra video.")
    plt.xlabel("Tid [s]")
    plt.ylabel("Styrke")
    plt.plot(t, blue, color="b")
    
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    
    plt.show()
    
    
    red_spec = [np.complex(c[0]) for c in spectrum]
    green_spec = [np.complex(c[1]) for c in spectrum]
    blue_spec = [np.complex(c[2]) for c in spectrum]
    for i in range (0,6):
        red_spec[i] = 0
        red_spec[-i] = 0
        green_spec[i] = 0
        green_spec[-i] = 0
        blue_spec[i] = 0
        blue_spec[-i] = 0


    puls_r = abs(freq[np.argmax(np.absolute(red_spec))]*60)
    puls_g = abs(freq[np.argmax(np.absolute(green_spec))]*60)
    puls_b = abs(freq[np.argmax(np.absolute(blue_spec))]*60)
    r_pulser.append(puls_r)
    g_pulser.append(puls_g)
    b_pulser.append(puls_b)    

#     print("Målt puls (rød kanal):", round(puls_r,1))
#     print("Målt puls (grønn kanal):", round(puls_g,1))
#     print("Målt puls (blå kanal):", round(puls_b,1))
# 
#     plt.title("Power spectrum of signal")
#     plt.xlabel("Frequency [Hz]")
#     plt.ylabel("Power [dB]")
#     plt.plot(freq, 20*np.log10(np.abs(spectrum))) # get the power spectrum
#     #plt.plot(freq, 20*np.log10(red)) # get the power spectrum
#     #plt.plot(cut_freq, 20*np.log10(cut_spec)) # get the power spectrum
#     plt.show()

    plt.title("Frekvensspektrum")
    plt.xlabel("Pulsfrekvens [bpm]")
    plt.ylabel("Energi [dB]")
    plt.plot(freq[:len(green_spec)//2]*60, 20*np.log10(np.abs(red_spec[:len(green_spec)//2])), 'r', label='Rød kanal') # get the power spectrum
    plt.plot(freq[:len(green_spec)//2]*60, 20*np.log10(np.abs(green_spec[:len(green_spec)//2])), 'g', label='Grønn kanal') # get the power spectrum
    plt.plot(freq[:len(green_spec)//2]*60, 20*np.log10(np.abs(blue_spec[:len(green_spec)//2])), 'b', label='Blå kanal') # get the power spectrum
    plt.legend()
    plt.grid()
    #plt.plot(freq, 20*np.log10(red)) # get the power spectrum
    #plt.plot(cut_freq, 20*np.log10(cut_spec)) # get the power spectrum
    plt.show()
#         

#     plt.title("Puls")
#     plt.xlabel("tid [s]")
#     plt.ylabel("Pulsstyrke")
#     plt.plot(t,red)
# 
#     plt.show()
    
print(r_pulser)
print(g_pulser)
print(b_pulser)
avg_r = sum(r_pulser)/len(r_pulser)
avg_g = sum(g_pulser)/len(r_pulser)
avg_b = sum(b_pulser)/len(r_pulser)

maaler_average = sum(pulsklokke)/len(pulsklokke)
std_r = np.std(r_pulser)
std_g = np.std(g_pulser)
std_b = np.std(b_pulser)

print("Gjennomsnitt av rød, grønn, blå:", avg_r, avg_g,avg_b)
print("Standardavvik for rød, grønn og blå:", std_r, std_g, std_b)
