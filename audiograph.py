import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import threading

arduino = serial.Serial('COM3', baudrate=115200 , timeout=0.1) #rtscts=True)
def to_arduino(x):
    arduino.write(bytes(x, 'utf-8'))
    # time.sleep(0.05)
    data = arduino.readline().decode('utf-8')
    print(data)
    # if x in data:
    return data
    # else:
    #     to_arduino(x)

# Set the audio parameters
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Create a figure and axis for plotting
fig, ax = plt.subplots()

# Create a time axis for the x-axis
x = np.arange(0, 2 * CHUNK, 2)

# Create an empty line object for the plot
line, = ax.plot(x, np.random.rand(CHUNK), '-')

# Set the y-axis limits
# ax.set_ylim(-32768, 32767)
ax.set_ylim(-5000, 5000)

def update_plot(stream):
    while True:
        data = stream.read(CHUNK)

        # Convert the data to a numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Update the line object with the new audio data
        line.set_ydata(audio_data)
        
        # Redraw the plot
        fig.canvas.draw()

        # Flush any pending GUI events
        plt.pause(0.01)
def update_arduino(stream):
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        intensity = np.max(audio_data)

        # Apply the FFT to the audio data
        fft_data = np.fft.fft(audio_data)
    
        # Calculate the frequencies corresponding to the FFT bins
        frequencies = np.fft.fftfreq(len(fft_data), 1/RATE)

        # Find the index of the maximum magnitude in the FFT data
        max_index = np.argmax(np.abs(fft_data))

        # Get the frequency corresponding to the maximum magnitude
        max_frequency = int(abs(frequencies[max_index]))

        color = max_frequency/100
        # if max_frequency > 1500:
        #     color = 1
        # elif max_frequency > 500:
        #     color = 2
        # else:
        #     color = 3

        # print(max_frequency, color)
        to_arduino(str(color))
        to_arduino(str(intensity))# + "|" + str(max_frequency))
        # Print the calculated frequency
        # print("Frequency:", max_frequency)
        # print("REVERSE" + str(max_frequency)[::-1])
        time.sleep(0.05)

        # print(stream.get_time()


thread = threading.Thread(target=update_arduino, args=(stream,))
thread.start()

update_plot(stream)
# while True:
#     # Read audio data from the stream
#     data = stream.read(CHUNK)

#     # Convert the data to a numpy array
#     audio_data = np.frombuffer(data, dtype=np.int16)

#     # pusdeo_freq = np.zeros(audio_data==0)
#     psudeo_intn = np.max(audio_data)
#     # print(psudeo_intn)
#     to_arduino(str(psudeo_intn))
#     # # Update the line object with the new audio data
#     line.set_ydata(audio_data)
    
#     # # Redraw the plot
#     fig.canvas.draw()
    

#     # # Flush any pending GUI events
#     plt.pause(0.01)
# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
