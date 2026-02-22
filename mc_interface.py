from mcrcon import MCRcon
import pyttsx3
import random

def speak(text, voice):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def summon(mob, voice, username, password, port, host):
    with MCRcon(host, "sekret", port=port) as mcr:
        rand = random.randint(1, 10)
        for i in range(rand):
            resp = mcr.command(f"/summon {mob} ~ ~ ~")
            print(resp)
        resp = mcr.command(f"/tp @e[type={mob}, limit={rand}, sort=nearest] {username}")
        print(resp)
        if voice == "Male":
            voi = 0
            voice_call(mob, rand, voi)
        elif voice == "Female":
            voi = 1
            voice_call(mob, rand, voi)
        else:
            voice_call(mob, rand, None)


def voice_call(mob, rand: int, v):
    if not v:
        return
    elif rand == 1:
        speak(f"Spawning a {mob}", v)
    else:
        speak(f"Spawning {rand} {mob}s", v)


