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

    cantidad_sucursales = 6
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

    info( '* Add links\n')
    #Agregamos el link, ponemos nombre a la interfaz y le agregamos una IP.
    #Debe ir primero el router con la interfaz, luego el switch.
    #hay que poner nombres cortos en las interfaces sino te tira error.
    net.addLink(rcentral,swan1, intfName1='rcentral1-eth0', params1={'ip':'192.168.100.6/29'})
    net.addLink(rsuc1,swan1, intfName1='rsuc1-eth1', params1={'ip':'192.168.100.1/29'})
    net.addLink(rsuc1,slan1, intfName1='rsuc1-eth0', params1={'ip':'10.0.1.1/24'})
    net.addLink(globals()['h1suc1'],globals()['slan1'])
    net.addLink(globals()['h2suc1'],globals()['slan1'])

    #rcentral con swan
    for i in range(cantidad_sucursales):
        i = i + 1
        rcdireccion = 6 + 6
        net.addLink(rcentral,global()['swan%s' %i], intfName1='rcentral.eth%s' %i, params1={'ip': '192.168.100.%s/29' %rcdireccion})
   
    #rsuc con wan
    for i in range(cantidad_sucursales):
        i = i + 1
        rcdireccion = 6 + 6
        net.addLink(global()['rsuc%s' %i],global()['swan%s' %i], intfName1='rsuc-eth%s' %i, params1={'ip': '192.168.100.%s/29' %rcdireccion})
    #rsuc con slan
    for i in range(cantidad_sucursales):
        i = i + 1
        rcdireccion = 6 + 6
        net.addLink(global()['rsuc%s' %i],global()['slan%s' %i], intfName1='rsuc-eth%s' %i, params1={'ip': '10.0.%s.1/24' %rcdireccion})

    #slan con hosts
    for i in range(cantidad_sucursales):
        i = i + 1
        rcdireccion = 6 + 6
        net.addLink(global()['h1suc%s' %i],global()['slan%s' %i])



    net.addLink(rcentral,swan2, intfName1='rcentral2-eth0', params1={'ip':'192.168.100.14/29'})
    net.addLink(rsuc2,swan2, intfName1='rsuc2-eth1', params1={'ip':'192.168.100.9/29'})
    net.addLink(rsuc2,slan2, intfName1='rsuc2-eth0', params1={'ip':'10.0.2.1/24'})
    net.addLink(globals()['h1suc2'],globals()['slan2'])
    net.addLink(globals()['h2suc2'],globals()['slan2'])
    

    info( '* Starting network\n')
    net.build()
    info( '* Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '* Starting switches\n')
    net.get('slan1').start([])
    net.get('swan1').start([])
    net.get('slan2').start([])
    net.get('swan2').start([])

    info( '* Post configure switches and hosts\n')

    #Agregar tabla de ruteo
    """
    h1suc1.cmd('ip route add 0.0.0.0/0 via 10.0.1.1')
    rsuc1.cmd('ip ro add 0.0.0.0/0 via 192.168.100.6')
    rcentral.cmd('ip ro add 0.0.0.0/0 via 192.168.100.1')
    """
    h1suc1.cmd('ip route add 0.0.0.0/0 via 10.0.1.1')
    h1suc2.cmd('ip route add 0.0.0.0/0 via 10.0.2.1')

    rcentral.cmd('ip ro add 10.0.1.0/24 via 192.168.100.1')
    rcentral.cmd('ip ro add 10.0.2.0/24 via 192.168.100.9')

    """
    esto esta mal porque yo quiero llegar a los hosts entonces debo poner ro add red de los hosts, no red de los routers...
    si dejo esto asi, y hago ping de host1suc1 a host1suc2 me va a decir que no se puede conectar, pero la direccion la conoce.
    rsuc1.cmd('ip ro add 192.168.100.8/29 via 192.168.100.6')
    rsuc2.cmd('ip ro add 192.168.100.0/29 via 192.168.100.14')
    """
    rsuc1.cmd('ip ro add 10.0.2.0/24 via 192.168.100.6')
    rsuc2.cmd('ip ro add 10.0.1.0/24 via 192.168.100.14')

    CLI(net)
    net.stop()

if _name_ == '_main_':
    setLogLevel( 'info' )
    myNetwork()