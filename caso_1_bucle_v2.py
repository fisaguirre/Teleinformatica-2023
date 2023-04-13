#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import math

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    #cantidad_sucursales = 12
    cantidad_sucursales = input("Agregue la cantidad de sucursales: ")
    mascara_red_host = 24
    mascara_router = 29

    mascara_sub_red_host = 32 - (math.log(cantidad_sucursales,2) + 8)
    mascara_sub_red_host = int(mascara_sub_red_host)
    # Se imprime la mascara de subred resultante
    #print("La mascara de subred adecuada es /{}".format(mascara_sub_red_host))

    info( '* Adding controller\n' )
    info( '* Add switches\n')
   
    """1-Creo switch lan
    2-creo switch wan
    3-creo routers y los ruteo
    """
    for i in range(cantidad_sucursales):
        i = i + 1
        globals()['slan%s' %i] = net.addSwitch('slan%s' %i, cls=OVSKernelSwitch, failMode='standalone')
        globals()['swan%s' %i] = net.addSwitch('swan%s' %i, cls=OVSKernelSwitch, failMode='standalone')
        globals()['rsuc%s' %i] = net.addHost('rsuc%s' %i, cls=Node, ip='')
        globals()['rsuc%s' %i].cmd('sysctl -w net.ipv4.ip_forward=1')
  
    rcentral = net.addHost('rcentral', cls=Node, ip='')
    rcentral.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '* Add hosts\n' )
    for i in range(cantidad_sucursales):
        i = i + 1
        globals()['h1suc%s' %i] = net.addHost('h1suc%s' %i, cls=Host, ip='10.0.%s.2/%s' %(i,mascara_red_host), defaultRoute=None)
    print("esto es: ", globals()['h1suc2'])

    info( '* Add links\n')
    #Agregamos el link, ponemos nombre a la interfaz y le agregamos una IP.
    #Debe ir primero el router con la interfaz, luego el switch.
    #hay que poner nombres cortos en las interfaces sino te tira error.
    for i in range(cantidad_sucursales):
        n = i + 1
        rcdireccion = 6 + i*8
        rsucdireccion = 1 + i*8
        hdireccion = 1
        net.addLink(rcentral,globals()['swan%s' %n], intfName1='rcentral.eth%s' %n, params1={'ip': '192.168.100.%s/%s' %(rcdireccion,mascara_router)})
        net.addLink(globals()['rsuc%s'%n],globals()['swan%s' %n], intfName1='r1.eth%s' %n, params1={'ip': '192.168.100.%s/%s' %(rsucdireccion,mascara_router)})
        net.addLink(globals()['rsuc%s'%n],globals()['slan%s' %n], intfName1='r%s.eth' %n, params1={'ip': '10.0.%s.1/%s' %(n, mascara_red_host)})
        net.addLink(globals()['h1suc%s'%n],globals()['slan%s' %n])

    info( '* Starting network\n')
    net.build()
    info( '* Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '* Starting switches\n')
    for i in range(cantidad_sucursales):
        i = i + 1
        net.get('slan%s'%i).start([])
        net.get('swan%s'%i).start([])
       
    info( '* Post configure switches and hosts\n')
    #Agregar tabla de ruteo
    for i in range(cantidad_sucursales):
        n = i + 1
        rcdireccion = 6 + i*8
        rsucdireccion = 1 + i*8
        net['h1suc%s'%n].cmd('ip route add 10.0.0.0/%s via 10.0.%s.1'%(mascara_sub_red_host,n))
        net['rcentral'].cmd('ip ro add 10.0.%s.0/%s via 192.168.100.%s'%(n,mascara_red_host,rsucdireccion))
        net['rsuc%s'%n].cmd('ip ro add 10.0.0/%s via 192.168.100.%s'%(mascara_sub_red_host,rcdireccion))

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel( 'info' )
    myNetwork()
