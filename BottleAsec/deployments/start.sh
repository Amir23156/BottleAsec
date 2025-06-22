

printStep(){
    echo ""
    echo ""
    echo "[" $1 "STARTED]"
    sleep 1 
}

printStep 'DOCKER_COMPOSE UP'
sudo docker-compose up -d

printStep 'DOCKER_COMPOSE UP'
sudo docker-compose ps

# Capture traffic on both networks to monitor lateral movement
sudo tcpdump -w ics_traffic.pcap -i br_icsnet &
sudo tcpdump -w office_traffic.pcap -i br_office


