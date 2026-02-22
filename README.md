# Voice Mob spawner
A fun little script to spawn mobs with voice control by using local speech to text

## Installation
### Via releases
Install it via the [releases](https://github.com/Justablue0/VoiceMobSpawning/releases/latest)(It is a portable file)

### Via python
Download the project
```bash
git clone https://github.com/Justablue0/VoiceMobSpawning
```
```bash
cd VoiceMobSpawning
```
install the requirements
```bash
pip install -r requirements.txt
```
and then just run
```bash
python main.py
```


## Setup
In terms of the script, it will guide you through everything.
For it to work you will need a Minecraft server. locally works fine too. download any Minecraft server for example [paper](https://papermc.io/downloads/paper) then in a folder for the server run the jar file it will generate a couple of files. After that go into eula.txt and change the eula to true. Then run the jar file again. After that stop the server(by closing the window or running stop in the window) go to the server.properties file and find the line enable-rcon and change it to 
```properties
enable-rcon=true
```
Then find the line
```properties
rcon.password
```
and set it to something secure. Finally find the line
```properties
rcon.port
```
remember what it is and then run the script/program
