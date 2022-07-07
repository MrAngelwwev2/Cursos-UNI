#Vamos a realizar las siguientes importaciones
import os
import sys
os.sys.path.append('/usr/lib/python3/dist-packages')
from scapy.all import *
from scapy.layers.inet import *

def is_root():
    return os.getuid() == 0
    
def run_scan(zombie, target, port):
    print('[*] Scan %s port %d using %s as zombie' % (target, port, zombie))
    #Obtenemos la identificación de IP del zombi con un SYN/ACK
    p1 = sr1(IP(dst=zombie)/TCP(sport=12345,dport=(123),flags="SA"),verbose=0)
    initial_id = p1.id
    print('[+] Id de IP inicial del zombie', initial_id)
    #SYN para apuntar con la IP falsificada del zombie
    p2 = send(IP(dst=target,src=zombie)/TCP(sport=12345,dport=(port),flags="S"),verbose=0)
    #SYN/ACK al zombie para ver si escuchó del objetivo
    p3 = sr1(IP(dst=zombie)/TCP(sport=12345,dport=(123),flags="SA"),verbose=0)
    final_id = p3.id
    print('[+] Id de IP final del zombie', final_id)
    if final_id - initial_id < 2:
        print('[+] Puerto %d : cerrado' % port)
    else:
        print ('[+] Puerto %d : abierto' % port)

if __name__ == '__main__':
    print
    if not is_root():
        print('[!] Debe de correr como administrador. Saliendo')
        sys.exit(1)
    if len(sys.argv) < 4 or sys.argv[1] == '-h':
        print('Usage: idle_scan.py zombieIP targetIP targetPort')
        sys.exit(1)
    run_scan(sys.argv[1], sys.argv[2], int(sys.argv[3]))