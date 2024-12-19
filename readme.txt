# How To Push new changes to Docker-Hub:
docker build -t splasher2000/find-the-client:0.03 .

docker push splasher2000/find-the-client:0.03



# install git
sudo apt-get update
sudo apt-get install git

# to clone
git clone https://github.com/SChristophS/find_the_client.git

# run setup
chmod +x setup.sh
./setup.sh

# to run
nohup python3 app.py > output.log 2>&1 &

>: Dies ist eine Umleitung der Standardausgabe (stdout). 
Alles, was das Skript normalerweise auf der Konsole ausgibt, wird stattdessen in die angegebene Datei geschrieben.

output.log: Das ist die Datei, in die die Standardausgabe (stdout) umgeleitet wird. 
In diesem Fall werden die Konsolenausgaben des Skripts in die Datei output.log geschrieben.

2>&1: Dies ist eine Umleitung der Standardfehlerausgabe (stderr). 
Die 2 steht für "Standardfehlerausgabe" und 1 für "Standardausgabe". 
Die Syntax 2>&1 bedeutet, dass die Standardfehlerausgabe an den gleichen Ort wie die Standardausgabe umgeleitet wird. 
In diesem Fall werden also sowohl die normalen Ausgaben als auch die Fehlerausgaben in die Datei output.log geschrieben.

&: Das kaufmännische Und (&) am Ende des Befehls bedeutet, dass das Skript im Hintergrund ausgeführt wird.
Das ermöglicht es Ihnen, die Kontrolle über die Konsole zurückzuerhalten und weitere Befehle auszuführen, während das Skript weiterhin im Hintergrund läuft.

# to find Process-ID (PID)
ps aux | grep app.py

# to kill
kill <PID>

# make script executable
chmod +x /home/christoph/apps/dynDNS/nsupdate.sh

# add crontab
crontab -e

# add new line
0 * * * * /home/christoph/apps/dynDNS/nsupdate.sh