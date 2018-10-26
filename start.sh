# This needs to be called by Raspbian autostart

cd /home/pi/ws/buildmonitor

printf "\n Installing dependencies for the build monitor"
pip3 install -r requirements.txt

printf "\n Starting the build monitor"
while ! /sbin/ifconfig wlan0 | grep -q 'inet [0-9]'; do
  printf "\n Waiting for internet connection"
  sleep 3
done

python3 main.py &
