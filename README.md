# Automated reCAPTCHA Solver

A Python automation script designed to solve Google's reCAPTCHA v2 challenges. It leverages Selenium for web orchestration and utilizes audio transcription to bypass visual verification.

> ## ⚠️ Disclaimer & Legal Notice
> **For Educational Purposes Only.**
> This project is developed for security research and technical demonstration. It is designed to be used exclusively on demo environments (like [Google's reCAPTCHA demo page](https://www.google.com/recaptcha/api2/demo)).
>
> * **Compliance:** Automating interactions with reCAPTCHA may violate the Terms of Service of Google and third-party websites. Use of this script on unauthorized platforms is strictly discouraged.
> * **No Warranty:** This software is provided "as is" without any warranty. The author assumes no liability for any misuse, account suspensions, or legal consequences arising from the use of this code.
> * **Ethical Conduct:** Users are responsible for complying with local laws and the regulations of the websites they visit.


## Features
* **Dynamic Browser Selection:** Choose between Chrome and Firefox at runtime with automatic configuration.
* **Automated Driver Management:** Uses `webdriver-manager` to automatically download and sync the correct WebDriver version.
* **Intelligent Frame Handling:** Seamlessly switches between the main page, the checkbox iframe, and the challenge popup.
* **Audio-Based Bypass:** Triggers the audio challenge and processes the payload for high reliability.
* **Speech-to-Text Integration:** Downloads `.mp3` samples, converts them to `.wav`, and transcribes them using Google Speech Recognition.
* **Human-Like Interaction:** Incorporates randomized delays to mimic natural user behavior and reduce detection.

## Usage
Simply execute the script. On startup, you will be prompted to select your preferred browser (1 for Firefox, 2 for Chrome). The script will then:
1. Initialize the selected WebDriver automatically.
2. Navigate to the reCAPTCHA demo page.
3. Interact with the checkbox and switch to the audio challenge.
4. Download, transcribe, and submit the solution.
5. Perform a final form submission and clean up temporary audio files.

## External Tools
This script requires **FFmpeg** for audio format conversion. You can install it easily using the following commands:

* **Windows:** Run `winget install "FFmpeg (Essentials Build)"`
* **Linux:** Run `sudo apt install ffmpeg`.
* **macOS:** Run `brew install ffmpeg`.
* **Manual download** from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).

## Required Python Packages
Install the necessary dependencies via pip:
* `selenium` - For browser automation.
* `SpeechRecognition` - To interface with the Google Speech-to-Text API.
* `pydub` - For seamless audio format conversion.
* `webdriver-manager` - To eliminate manual WebDriver installation and path issues.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

```
GNU General Public License v3.0
Copyright (c) 2026 Cryptix
```
