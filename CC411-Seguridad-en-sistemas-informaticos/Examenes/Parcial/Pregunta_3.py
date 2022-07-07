#Vamos a importar lo necesario
from sys import flags
import os
from scapy.all import *
from scapy.layers.inet import *
#Vamos a definir tanto la IP como el numero de saltos
ip = IP(dst = 'www.youtube.com',ttl = (1,10))
port = RandNum(1024,65535)
syn = ip / TCP(sport = port, dport = 80, flags = 'S', seq = 42)
synack,error = sr(syn)
#Realizamos el rastreo de la ruta
print("Rastrear ruta paquete SYN")
#Imprimimos el resultado
synack.summary(lambda s, r: r.sprintf("%IP.src%\t{ICMP:%ICMP.type%}\t{TCP:%TCP.flags%}"))