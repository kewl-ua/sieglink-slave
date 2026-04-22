listen:
	socat -u UDP-RECV:5000,reuseaddr EXEC:"python3 main.py"
