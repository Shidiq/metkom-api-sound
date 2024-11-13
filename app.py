import io

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, request, send_file
from scipy.io import wavfile
from scipy.signal import filtfilt, firwin, freqz, kaiserord

matplotlib.use("Agg")
plt.rcParams["svg.fonttype"] = "none"

# Global variables to store data between requests
original_data = None
filtered_data = None
taps = None
fs = None
set_dpi = 300


# Function to process the audio file
def process_audio(file, cutoff_hz, width, ripple_db):
    global original_data, filtered_data, taps, fs

    fs, data = wavfile.read(file)
    original_data = data  # Store original data
    nyq_rate = fs / 2.0
    N, beta = kaiserord(ripple_db, width / nyq_rate)
    taps = firwin(N, cutoff_hz / nyq_rate, window=("kaiser", beta))
    filtered_data = filtfilt(taps, 1.0, data)  # Store filtered data

    # Save the filtered data to a BytesIO object
    buf = io.BytesIO()
    wavfile.write(buf, fs, filtered_data.astype(np.int16))
    buf.seek(0)
    return buf


# Plotting functions (modified to return BytesIO)
def plot_signal(original, filtered):
    plt.figure(figsize=(12, 6))
    plt.plot(original, label="Original")
    plt.plot(filtered, label="Filtered")
    plt.title("Original vs. Filtered Audio Signal")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="svg", dpi=set_dpi)
    plt.close()
    buf.seek(0)
    return buf


def plot_amplitude_response(taps, nyq_rate):
    w, h = freqz(taps, worN=8000)
    plt.figure(figsize=(12, 6))
    plt.plot((w / np.pi) * nyq_rate, 20 * np.log10(np.abs(h)))
    plt.title("Amplitude Response of the FIR Filter")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain (dB)")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="svg", dpi=set_dpi)
    plt.close()
    buf.seek(0)
    return buf


def plot_impulse_response(taps):
    plt.figure(figsize=(12, 6))
    plt.stem(taps)
    plt.title("Impulse Response of the FIR Filter")
    plt.xlabel("Tap Number")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="svg", dpi=set_dpi)
    plt.close()
    buf.seek(0)
    return buf


# Flask API
app = Flask(__name__)


@app.route("/filter", methods=["POST"])
def filter_audio():
    global original_data, filtered_data, taps, fs

    file = request.files["file"]
    cutoff = float(request.form.get("cutoff", 1000.0))
    width = float(request.form.get("width", 50.0))
    ripple_db = float(request.form.get("ripple_db", 60.0))

    # Process the audio and store data in globals
    buf = process_audio(file, cutoff, width, ripple_db)

    # Return the filtered audio file
    return send_file(
        buf,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="filtered.wav",
    )


@app.route("/plot_signal", methods=["GET"])
def get_plot_signal():
    if original_data is None or filtered_data is None:
        return "No data available. Please POST to /filter first.", 400
    buf = plot_signal(original_data, filtered_data)
    return send_file(buf, mimetype="image/svg")


@app.route("/plot_amplitude_response", methods=["GET"])
def get_plot_amplitude_response():
    if taps is None or fs is None:
        return "No data available. Please POST to /filter first.", 400
    nyq_rate = fs / 2.0
    buf = plot_amplitude_response(taps, nyq_rate)
    return send_file(buf, mimetype="image/svg")


@app.route("/plot_impulse_response", methods=["GET"])
def get_plot_impulse_response():
    if taps is None:
        return "No data available. Please POST to /filter first.", 400
    buf = plot_impulse_response(taps)
    return send_file(buf, mimetype="image/svg")


if __name__ == "__main__":
    app.run(debug=True)
