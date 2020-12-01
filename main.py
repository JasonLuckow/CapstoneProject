from matplotlib import pyplot as plt
import thinkdsp
from playsound import playsound
import numpy as np
from playsound import playsound

lettersDict = { "1000001": "A",   "1100001": "a",
                "1000010": "B",   "1100010": "b",
                "1000011": "C",   "1100011": "c",
                "1000100": "D",   "1100100": "d",
                "1000101": "E",   "1100101": "e",
                "1000110": "F",   "1100110": "f",
                "1000111": "G",   "1100111": "g",
                "1001000": "H",   "1101000": "h",
                "1001001": "I",   "1101001": "i",
                "1001010": "J",   "1101010": "j",
                "1001011": "K",   "1101011": "k",
                "1001100": "L",   "1101100": "l",
                "1001101": "M",   "1101101": "m",
                "1001110": "N",   "1101110": "n",
                "1001111": "O",   "1101111": "o",
                "1010000": "P",   "1110000": "p",
                "1010001": "Q",   "1110001": "q",
                "1010010": "R",   "1110010": "r",
                "1010011": "S",   "1110011": "s",
                "1010100": "T",   "1110100": "t",
                "1010101": "U",   "1110101": "u",
                "1010110": "V",   "1110110": "v",
                "1010111": "W",   "1110111": "w",
                "1011000": "X",   "1111000": "x",
                "1011001": "Y",   "1111001": "y",
                "1011010": "Z",   "1111010": "z",
                
                "0101110": ".",
                "0101100": ",",
                "0100000": " "}

freqsList = [400,600,800,1000,1200,1400,1600]

class CapstoneProject():
    def __init__(self, wavFile): 
        self.waveFile = wavFile
        self.wave_from_file = thinkdsp.read_wave(wavFile)
        self.spectrum = self.wave_from_file.make_spectrum()
        self.spectrogram = self.wave_from_file.make_spectrogram(seg_length=512)
        self.newTimes = []
        self.ans = ""
        for num in self.spectrogram.times():
            if int(num) not in self.newTimes:
                self.newTimes.append(int(num))

    def decodeWavFile(self):
        for times in self.newTimes:
            wave = self.wave_from_file.segment(start=times, duration=.4)

            spectrum = wave.make_spectrum()
            spectrum.high_pass(cutoff=300,factor=0)

            peaks = spectrum.peaks()
            newPeaks = []

            for peak in peaks:
                amp = peak[0]
                freq = peak[1]
                freqInt = int(freq)
                if amp > 100 and (freqInt % 200 == 0) and freq not in newPeaks:
                    newPeaks.append(int(peak[1]))

            newPeaks.sort()

            binList = ""
            for freq in freqsList:
                if int(freq) in newPeaks:
                    binList += "1"
                else:
                    binList += "0"

            if binList in lettersDict:
                self.ans += lettersDict.get(binList)
    
    @staticmethod
    def encodeWavFile(message):
        """
            returns: .wav file destination to the ecoded message
        """
        binNum = ""
        encodedWave = thinkdsp.SinSignal(freq=0, amp=0, offset=0).make_wave()
        offCount = 0
        for letter in message:
            for key, value in lettersDict.items():
                if letter == value:
                    binNum = key
                    
            count = 0

            for num in binNum:
                if num == str(1):
                    signal = thinkdsp.SinSignal(freq=freqsList[count], amp=1000, offset=0)
                    encodedWave += signal.make_wave(start=offCount, duration=.92)
                else:
                    signal = thinkdsp.SinSignal(freq=freqsList[count], amp=0, offset=offCount)
                    encodedWave += signal.make_wave(start=offCount, duration=0.92)
                count += 1

            offCount += 1

        encodedWave.play("encodedWave.wav")
        return "encodedWave.wav"

    @staticmethod
    def playWav(waveFile):
        playsound(waveFile)

    def answer(self):
        """
            returns: answer to the encoded .wav file, decodeWavFile must be ran first.
        """
        # print("\n\n\t" + self.ans + "\n\n")
        return self.ans

    def plotSpectrum(self):
        self.spectrum.high_pass(cutoff=300,factor=0)
        self.spectrum.plot()
        plt.title('Spectrum')
        # plt.xlim(right=self.newTimes[-1])
        plt.show()

    def plotSpectrogram(self):
        self.spectrogram.plot(high=1700)
        plt.title('Spectrogram')
        plt.ylim(bottom=350)
        plt.xlim(right=self.newTimes[-1]+1)
        plt.show()


# encodedMessage = CapstoneProject.encodeWavFile("I miss the old Kanye") ## uncomment this line to decode this .wav file
encodedMessage = "ece3304_capstone_message01.wav" ## uncomment this line to decode this .wav file
# CapstoneProject.playWav(encodedMessage) 
newProblem = CapstoneProject(encodedMessage)
newProblem.decodeWavFile()
decodedMessage = newProblem.answer()
print("\n\n\tEncoded message wav file: " + encodedMessage + "\n" + "\tEncoded message: " + decodedMessage + "\n")
newProblem.plotSpectrum()
newProblem.plotSpectrogram()


