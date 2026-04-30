# Copyright (C) 2026 Cryptix
# SPDX-License-Identifier: GPL-3.0-or-later 

import os
import time
import random
import urllib.request
import speech_recognition as sr
from pydub import AudioSegment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def choose_browser():
    # Prompt user for browser choice
    while True:
        print("\nWhich browser would you like to use?")
        print("1: Firefox")
        print("2: Chrome")
        choice = input("Enter 1 or 2: ").strip()
        
        if choice == '1':
            # Configure Firefox with US-English
            print("[Info] Setting up Firefox (Language: en-US)...")
            options = webdriver.FirefoxOptions()
            options.set_preference("intl.accept_languages", "en-US")
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
        
        elif choice == '2':
            # Configure Chrome with US-English
            print("[Info] Setting up Chrome (Language: en-US)...")
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            options.add_argument("--lang=en-US")
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)
        else:
            print("[Warning] Invalid input. Please enter '1' or '2'.")

def process_audio(src_url, mp3_path, wav_path):
    # Download audio payload
    print("[Info] Downloading audio payload...")
    urllib.request.urlretrieve(src_url, mp3_path)
    
    # Convert MP3 to WAV for speech recognition
    print("[Info] Converting MP3 to WAV format...")
    AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
    
    # Transcribe audio using Google Speech Recognition
    print("[Info] Transcribing audio...")
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        
    try:
        # Enforce en-US for international compatibility
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        raise Exception("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        raise Exception(f"Google Speech Recognition service error: {e}")

def human_delay():
    # Simulate natural user behavior
    time.sleep(random.uniform(1.2, 2.8))

def main():
    # Setup temporary file paths
    data_path = os.getcwd()
    mp3_file = os.path.join(data_path, "audio.mp3")
    wav_file = os.path.join(data_path, "audio.wav")
    
    browser = choose_browser()
    wait = WebDriverWait(browser, 15) 
    
    try:
        print("[Info] Accessing reCAPTCHA demo page...")
        browser.get("https://www.google.com/recaptcha/api2/demo")
        
        # Switch to checkbox iframe and click
        print("[Info] Locating reCAPTCHA checkbox...")
        checkbox_frame = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'anchor')]")))
        browser.switch_to.frame(checkbox_frame)
        human_delay()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))).click()
        
        # Switch to challenge popup iframe
        browser.switch_to.default_content()
        print("[Info] Waiting for challenge popup...")
        challenge_frame = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'bframe')]")))
        browser.switch_to.frame(challenge_frame)
        
        # Trigger the audio challenge
        human_delay()
        wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))).click()
        
        # Refresh iframe focus for the audio controls
        browser.switch_to.default_content()
        challenge_frame = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'bframe')]")))
        browser.switch_to.frame(challenge_frame)
        
        # Play audio snippet
        print("[Info] Playing audio challenge...")
        human_delay()
        play_btn_xpath = "//div[contains(@class, 'rc-audiochallenge-play-button')]/button | //button[@id='audio-instructions']"
        wait.until(EC.element_to_be_clickable((By.XPATH, play_btn_xpath))).click()
        
        # Extract source URL and transcribe
        audio_element = wait.until(EC.presence_of_element_located((By.ID, "audio-source")))
        src = audio_element.get_attribute("src")
        recognized_text = process_audio(src, mp3_file, wav_file)
        
        print(f"\n[Success] Recognized Text: {recognized_text}\n")
        
        # Input transcribed text and verify
        input_field = wait.until(EC.element_to_be_clickable((By.ID, "audio-response")))
        input_field.send_keys(recognized_text.lower())
        human_delay()
        wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))).click()
        
        # Submit the final form on the main page
        print("[Info] Submitting final form...")
        browser.switch_to.default_content() 
        human_delay()
        
        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-demo-submit")))
        submit_btn.click()
        
        print("[Success] Form submitted successfully!")

    except (TimeoutException, NoSuchElementException):
        print("[Error] Automation failed: Could not locate web elements in time.")
    except WebDriverException as e:
        print(f"[Error] WebDriver encountered an issue: {e}")
    except Exception as e:
        print(f"[Error] Unexpected exception: {e}")
        
    finally:
        # Cleanup temporary audio files
        print("[Info] Cleaning up temporary files...")
        for f in [mp3_file, wav_file]:
            if os.path.exists(f): os.remove(f)
        print("[Info] Process finished.")

if __name__ == "__main__":
    main()