#!/bin/bash

#cd src

name="$1"

# Optionally harden the container by closing common unused ports
if [ "$HARDEN_PORTS" = "true" ]; then
    echo "[HARDEN] Closing unused service ports"
    iptables -A INPUT -p tcp --dport 23 -j DROP  # Telnet
    iptables -A INPUT -p tcp --dport 11211 -j DROP  # Memcached
    iptables -A INPUT -p tcp --dport 80 -j DROP   # HTTP
fi
if [ -z "$1" ]
then
      echo "start command need module_name to initiate!"
      exit 1
fi

if [[ $1 = "FactorySimulation.py" ]]
then

	#IP=$(hostname -I)
	#IP_STR=${IP// /,}
  	sudo memcached -d -u nobody memcached -l 127.0.0.1:11211,192.168.1.31
	sudo service memcached start	   

fi

if [ $1 = "PLC1.py" ] || [ $1 = "PLC2.py" ] || [ $1 = "HMI1.py" ] || [ $1 = "HMI2.py" ] || [ $1 = "HMI3.py" ] || [ $1 = "FactorySimulation.py" ] || [ $1 = "Attacker.py" ] || [ $1 = "AttackerMachine.py" ] || [ $1 = "AttackerRemote.py" ]
then 
	python3 $1
else
	echo "the is no command with name: $1"
fi
