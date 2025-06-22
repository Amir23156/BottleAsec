#!/bin/bash

#cd src

name="$1"
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

# Optional office network bridge for HMI3
if [[ "$1" == "HMI3.py" ]]; then
    # Normalize env var to lowercase for comparison
    bridge="${WIFI_BRIDGE_ENABLED,,}"
    if [[ "$bridge" == "false" ]]; then
        echo "WIFI_BRIDGE_ENABLED=false - disabling office network interface"
        # eth1 is the office_network interface added by docker-compose
        ip addr flush dev eth1 2>/dev/null || true
        ip link set eth1 down 2>/dev/null || true
    fi
fi

if [ $1 = "PLC1.py" ] || [ $1 = "PLC2.py" ] || [ $1 = "HMI1.py" ] || [ $1 = "HMI2.py" ] || [ $1 = "HMI3.py" ] || [ $1 = "FactorySimulation.py" ] || [ $1 = "Attacker.py" ] || [ $1 = "AttackerMachine.py" ] || [ $1 = "AttackerRemote.py" ]
then 
	python3 $1
else
	echo "the is no command with name: $1"
fi
