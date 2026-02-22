import csv
import difflib
import json
import queue
import sys
import time

import pyfiglet
import questionary
import sounddevice as sd
from vosk import Model, KaldiRecognizer

import mc_interface


q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def ask_model():
    model_lang = questionary.select("Choose your model", choices=["English", "Dutch"]).ask()
    if model_lang == "English":
        model = Model(lang="en-us", )
        return model
    elif model_lang == "Dutch":
        model = Model(lang="nl")
        return model
    else:
        return ask_model()


def main():
    global device, device_info

    f = pyfiglet.Figlet(font="slant")
    print(f.renderText("Voice mob spawning"))
    print("For mc\n")
    print("By:")
    f = pyfiglet.Figlet(font="3d-ascii")
    print(f.renderText("Justablue"))
    mobs = []
    with open("mobs.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            mob_name = row[0].replace("_", " ").lower()
            mobs.append(mob_name)

    user = questionary.text("What is your mc username?",
                            validate=lambda text: True if text else "Please enter a username").ask()
    port = questionary.text(
        "This tool uses mcrcon so what is the port for the mcrcon?",
        validate=lambda num: True if int(num).is_integer() else "Please enter a valid port",
        default="25575"
    ).ask()
    password = questionary.password("What is your mcrcon password?(input is redacted)",
                            validate=lambda text: True if text else "Please enter a password").ask()
    port = int(port)




    try:
        try:
            devices = sd.query_devices()
            print(f"Devices found!")
            device_info = sd.query_devices(kind="input")
            print(f"Default input device found!\n{device_info}")
            device = questionary.confirm(f"Do you want to use your default microphone device?({device_info['name']})",
                                         default=True).ask()
            if device:
                print("Using default microphone device")
            else:
                input_devices = []
                for device in devices:
                    if device["max_input_channels"] > 1:
                        input_devices.append(device)

                # ask user
                device = questionary.select(
                    "Please choose an input device to use",
                    choices=input_devices
                ).ask()  # returns the value (device index)

                device_info = sd.query_devices(device)
                print(f"You selected: {device_info['name']}")
            # soundfile expects an int, sounddevice provides a float:
            samplerate = int(device_info["default_samplerate"])
        except Exception as e:
            print(f"\nError with devices:\n{e}")
            sys.exit(1)
        print(f"\nSamplerate: {samplerate}")

        model = ask_model()
        cutoff = questionary.text(
            "Please choose a word similarity cutoff value for the speech to text",
            default="0.8"
        ).ask()
        cutoff = float(cutoff)
        if not 0 < cutoff < 1:
            raise ValueError("Cutoff must be between 0 and 1")
            sys.exit(1)
        selected_voice = questionary.select("Message choose TTS voice", choices=["Male", "Female", "Off(None)"]).ask()
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device_info["index"], dtype="int16",
                               channels=1, callback=callback):
            print("#" * 80)
            print("Press Ctrl+C to stop the recording")
            print("#" * 80)

            rec = KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    print(rec.Result())
                else:
                    partial_json = rec.PartialResult()
                    partial_dict = json.loads(partial_json)
                    partial_result = partial_dict.get("partial", "")
                    text = partial_dict.get("partial", "")
                    print("Partial:", text)
                    # Fuzzy match against mobs
                    matches = difflib.get_close_matches(text, mobs, n=1, cutoff=cutoff)
                    if matches:
                        mob_name = matches[0].replace(" ", "_").lower()
                        print("Matched Mob:", mob_name)
                        mc_interface.summon(mob_name, selected_voice, username=user, password=password, port=port)
                        time.sleep(1)






    except KeyboardInterrupt:
        print("\nDone")
    except Exception as e:
        print(f"Error:\n{e}")

if __name__ == "__main__":
    main()
