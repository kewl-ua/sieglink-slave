SLAVE_TUNNELED_IP = 10.0.0.2
MASTER_TUNNELED_IP = 10.0.0.3

SLAVE_IPV6_ADDRESS = fd33:a466:9b52:8:7ff6:b042:1831:587d
MASTER_IPV6_ADDRESS = fd33:a466:9b52:8:3a26:7add:2ed2:3207

listen:
	socat -u UDP-RECV:5000,reuseaddr EXEC:"python3 main.py"

listen_ipv6:
	socat UDP6-RECV:5000,reuseaddr - | python3 main.py

listen_tunneled:
	socat -u UDP-RECV:5000,reuseaddr EXEC:"python3 main.py"

slave_service_prepare:
	sudo cp sieglink_slave.service /etc/systemd/system/sieglink_slave.service
	
slave_service:
	sudo systemctl daemon-reload
	sudo systemctl enable sieglink_slave
	sudo systemctl start sieglink_slave
	sudo systemctl status sieglink_slave

pigpio_prepare:
	sudo cp pigpiod.service /etc/systemd/system/pigpiod.service
	sudo cat /etc/systemd/system/pigpiod.service

pigpio:
	sudo systemctl daemon-reload
	sudo systemctl enable pigpiod
	sudo systemctl start pigpiod
	sudo systemtl status pigpiod

