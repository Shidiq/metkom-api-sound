# FIR Audio Filter API with Kaiser Window

This repository contains a Flask-based API for filtering WAV audio files using a Finite Impulse Response (FIR) filter with a Kaiser window. The API allows users to upload an audio file, apply a customizable FIR filter, and retrieve the filtered audio along with visualizations of the original vs. filtered signal, amplitude response, and impulse response.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
	- [`/filter` (POST)](#filter-post)
	- [`/plot_signal` (GET)](#plot_signal-get)
	- [`/plot_amplitude_response` (GET)](#plot_amplitude_response-get)
	- [`/plot_impulse_response` (GET)](#plot_impulse_response-get)
  - [Examples](#examples)
	- [Using `curl`](#using-curl)
	- [Using a Python Script](#using-a-python-script)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Notes](#notes)

---

## Features

- **Audio Filtering**: Apply a customizable FIR filter with a Kaiser window to a WAV audio file.
- **Visualization**: Generate plots for:
  - Original vs. Filtered Audio Signal
  - Amplitude Response of the FIR Filter
  - Impulse Response of the FIR Filter
- **API Access**: Interact with the application via RESTful API endpoints.
- **Customization**: Adjust filter parameters like cutoff frequency, transition width, and stopband attenuation.
- **Plot Formats**: Plots are generated in SVG format with high DPI settings for quality.
- **Simple Global Data Handling**: Uses global variables to store data between requests (suitable for simple use cases).

---

## Getting Started

### Prerequisites

- **Python 3.6+**
- **Python Packages**:
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `flask`

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: If `requirements.txt` is not provided, you can install the packages manually:

   ```bash
   pip install numpy scipy matplotlib flask
   ```

---

## Usage

### Running the Application

1. **Ensure Matplotlib Backend is Set**:

   The application sets the Matplotlib backend to `Agg` to allow plotting without a display environment. This is already handled in the script.

2. **Run the Flask Application**:

   ```bash
   python app.py
   ```

   **Note**: Replace `app.py` with the actual script name if different.

3. **Verify the Server is Running**:

   You should see output similar to:

   ```
    * Serving Flask app "app" (lazy loading)
    * Environment: production
      WARNING: Do not use the development server in a production environment.
      Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

### API Endpoints

#### `/filter` (POST)

- **Description**: Uploads a WAV file and applies the FIR filter.
- **URL**: `http://localhost:5000/filter`
- **Method**: `POST`
- **Form Data Parameters**:
  - `file`: The WAV file to be filtered.
  - `cutoff`: (Optional) Cutoff frequency in Hz (default: `1000.0`).
  - `width`: (Optional) Transition width in Hz (default: `50.0`).
  - `ripple_db`: (Optional) Stopband attenuation in dB (default: `60.0`).
- **Response**:
  - Returns the filtered WAV file as an attachment.

#### `/plot_signal` (GET)

- **Description**: Retrieves the plot of the original vs. filtered audio signal.
- **URL**: `http://localhost:5000/plot_signal`
- **Method**: `GET`
- **Response**:
  - Returns the plot image in SVG format.

#### `/plot_amplitude_response` (GET)

- **Description**: Retrieves the amplitude response plot of the FIR filter.
- **URL**: `http://localhost:5000/plot_amplitude_response`
- **Method**: `GET`
- **Response**:
  - Returns the plot image in SVG format.

#### `/plot_impulse_response` (GET)

- **Description**: Retrieves the impulse response plot of the FIR filter.
- **URL**: `http://localhost:5000/plot_impulse_response`
- **Method**: `GET`
- **Response**:
  - Returns the plot image in SVG format.

**Note**: The plotting endpoints require that a POST request has been made to `/filter` beforehand, as the data is stored in global variables.

### Examples

#### Using `curl`

**1. Upload and Filter an Audio File**

```bash
curl -X POST \
     -F "file=@data/speech.wav" \
     -F "cutoff=1000" \
     -F "width=50" \
     -F "ripple_db=60" \
     http://localhost:5000/filter \
     --output filtered.wav
```

- **Explanation**:
  - `-X POST`: Specifies the POST method.
  - `-F`: Sends form data.
  - `file=@data/speech.wav`: Uploads `speech.wav` from the `data` directory.
  - `--output filtered.wav`: Saves the filtered audio as `filtered.wav`.

**2. Retrieve the Original vs. Filtered Signal Plot**

```bash
curl http://localhost:5000/plot_signal --output plot_signal.svg
```

**3. Retrieve the Amplitude Response Plot**

```bash
curl http://localhost:5000/plot_amplitude_response --output plot_amplitude_response.svg
```

**4. Retrieve the Impulse Response Plot**

```bash
curl http://localhost:5000/plot_impulse_response --output plot_impulse_response.svg
```

#### Using a Python Script

```python
import requests

# URL of the Flask app
base_url = 'http://localhost:5000'

# Path to your WAV file
file_path = 'data/speech.wav'

# Filter parameters
params = {
    'cutoff': '1000',
    'width': '50',
    'ripple_db': '60'
}

# Upload and filter the audio file
with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(f'{base_url}/filter', files=files, data=params)

# Save the filtered audio
with open('filtered.wav', 'wb') as f:
    f.write(response.content)

# Retrieve and save the plots
endpoints = {
    'plot_signal': 'plot_signal.svg',
    'plot_amplitude_response': 'plot_amplitude_response.svg',
    'plot_impulse_response': 'plot_impulse_response.svg'
}

for endpoint, filename in endpoints.items():
    plot_response = requests.get(f"{base_url}/{endpoint}")
    if plot_response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(plot_response.content)
        print(f"Saved {filename}")
    else:
        print(f"Failed to retrieve {endpoint}")
```

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---

## License

This project is licensed under the GPL-3.0 license - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - For the web framework.
- [NumPy](https://numpy.org/) - For numerical computations.
- [SciPy](https://www.scipy.org/) - For signal processing functions.
- [Matplotlib](https://matplotlib.org/) - For plotting and visualization.

---

## Notes

### Global Variables and Data Persistence

This application uses global variables to store data between requests. While this approach is acceptable for simple, single-user applications or testing purposes, it is **not recommended for production environments** due to the following reasons:

- **Thread Safety**: Global variables can lead to race conditions and inconsistent data in multi-threaded applications.
- **Concurrency Issues**: In a web application serving multiple users, data might get mixed up between users.
- **Scalability**: Global variables are not suitable for applications that require scaling across multiple processes or servers.

**Recommendation**: For production use, consider implementing a more robust data storage solution, such as server-side sessions, a caching mechanism, or a database to store user-specific data between requests.

### Matplotlib Backend

The application sets the Matplotlib backend to `Agg` to allow rendering plots without a display environment. This is necessary for server environments where a GUI is not available.

### Plot Formats

- **Format**: Plots are saved in SVG format for scalability and quality.
- **DPI Setting**: The DPI is set to 300 for high-resolution images.
- **Font Settings**: `plt.rcParams["svg.fonttype"] = "none"` is used to ensure text remains as text in the SVG.

### Dependencies

- **Python Packages**: The application uses `numpy`, `scipy`, `matplotlib`, and `flask`.
- **No External Caching**: Unlike versions that use Redis or other caching mechanisms, this application relies on global variables.

---

**Disclaimer**: This application is intended for educational purposes and may require adjustments for production use. Ensure that you handle user input validation, error handling, and security considerations appropriately in a real-world application.

---

**Contact Information**: If you have any questions or need assistance, feel free to open an issue or contact the repository maintainer.

---

**Note**: Ensure that you have the appropriate permissions and licenses to use and distribute any third-party code or resources included in this project.