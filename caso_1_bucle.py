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

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    cantidad_sucursales = 12
    info( '* Adding controller\n' )
    info( '* Add switches\n')
   
    #aca creo switch lan para red sucursales
    for i in range(cantidad_sucursales):
        i = i + 1
        globals()['slan%s' %i] = net.addSwitch('slan%s' %i, cls=OVSKernelSwitch, failMode='standalone')
        
    #aca creo los witches wan para las sucursales
    for i in range(cantidad_sucursales):
        i = i + 1
        globals()['swan%s' %i] = net.addSwitch('swan%s' %i, cls=OVSKernelSwitch, failMode='standalone')
    
    rcentral = net.addHost('rcentral', cls=Node, ip='')
    rcentral.cmd('sysctl -w net.ipv4.ip_forward=1')

    #Creo los routers
    for i in range(cantidad_sucursales):
        i = i + 1
        globals()['rsuc%s' %i] = net.addHost('rsuc%s' %i, cls=Node, ip='')
        #ruteo los routers
        globals()['rsuc%s' %i].cmd('sysctl -w net.ipv4.ip_forward=1')


    info( '* Add hosts\n' )
    #aca creo 1 solo host por cada sucursal (sirve para probar)
    for i in range(cantidad_sucursales):
        i = i + 1
        globals()['h1suc%s' %i] = net.addHost('h1suc%s' %i, cls=Host, ip='10.0.%s.2/24' %i, defaultRoute=None)
    
    for i in range(cantidad_sucursales):
        i = i + 1
        globals()['h2suc%s' %i] = net.addHost('h2suc%s' %i, cls=Host, ip='10.0.%s.254/24' %i, defaultRoute=None)
    print("esto es: ", globals()['h2suc2'])


    info( '* Add links\n')
    #Agregamos el link, ponemos nombre a la interfaz y le agregamos una IP.
    #Debe ir primero el router con la interfaz, luego el switch.
    #hay que poner nombres cortos en las interfaces sino te tira error.
   
    print("hola")
    for i in range(cantidad_sucursales):
        n = i + 1
        rcdireccion = 6 + i*8
        rsucdireccion = 1 + i*8
        hdireccion = 1
        net.addLink(rcentral,globals()['swan%s' %n], intfName1='rcentral.eth%s' %n, params1={'ip': '192.168.100.%s/29' %rcdireccion})
        net.addLink(globals()['rsuc%s'%n],globals()['swan%s' %n], intfName1='r1.eth%s' %n, params1={'ip': '192.168.100.%s/29' %rsucdireccion})
        net.addLink(globals()['rsuc%s'%n],globals()['slan%s' %n], intfName1='r%s.eth' %n, params1={'ip': '10.0.%s.1/24' %n})
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
        globals()['h1suc%s'%n].cmd('ip route add 10.0.0.0/21 via 10.0.%s.1'%n)
        rcentral.cmd('ip ro add 10.0.%s.0/24 via 192.168.100.%s'%(n,rsucdireccion))
        globals()['rsuc%s'%n].cmd('ip ro add 10.0.0/21 via 192.168.100.%s'%rcdireccion)

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel( 'info' )
    myNetwork()
