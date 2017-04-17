from signal_processing.window_type import WindowType
from signal_processing.signal_smoother import SignalSmoother
import soundfile as sf


class SignalConnector:
    def connectFromSignals(self, signals, smoother_window_type=WindowType.hamming, window_length=40):
        signal = [item for sublist in signals for item in sublist]
        return SignalSmoother(signal).smooth(smoother_window_type, window_length)

    def connectFromFiles(self, files, smoother_window_type=WindowType.hamming, window_length=40):
        signals = []
        for file in files:
            data, _ = sf.read(file)
            signals.append(data)
        return self.connectFromSignals(signals, smoother_window_type, window_length)
