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

    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8')

    cantidad_sucursales = 6
    info('* Adding controller\n')
    info('* Add switches\n')

    # aca creo switch lan para red sucursales
    slan1 = net.addSwitch('slan1', cls=OVSKernelSwitch, failMode='standalone')
    slan2 = net.addSwitch('slan2', cls=OVSKernelSwitch, failMode='standalone')
    slan3 = net.addSwitch('slan3', cls=OVSKernelSwitch, failMode='standalone')
    slan4 = net.addSwitch('slan4', cls=OVSKernelSwitch, failMode='standalone')
    slan5 = net.addSwitch('slan5', cls=OVSKernelSwitch, failMode='standalone')
    slan6 = net.addSwitch('slan6', cls=OVSKernelSwitch, failMode='standalone')

    swan1 = net.addSwitch('swan1', cls=OVSKernelSwitch, failMode='standalone')
    swan2 = net.addSwitch('swan2', cls=OVSKernelSwitch, failMode='standalone')
    swan3 = net.addSwitch('swan3', cls=OVSKernelSwitch, failMode='standalone')
    swan4 = net.addSwitch('swan4', cls=OVSKernelSwitch, failMode='standalone')
    swan5 = net.addSwitch('swan5', cls=OVSKernelSwitch, failMode='standalone')
    swan6 = net.addSwitch('swan6', cls=OVSKernelSwitch, failMode='standalone')

    rcentral = net.addHost('rcentral', cls=Node, ip='')
    rcentral.cmd('sysctl -w net.ipv4.ip_forward=1')

    rsuc1 = net.addHost('rsuc1', cls=Node, ip='')
    rsuc2 = net.addHost('rsuc2', cls=Node, ip='')
    rsuc3 = net.addHost('rsuc3', cls=Node, ip='')
    rsuc4 = net.addHost('rsuc4', cls=Node, ip='')
    rsuc5 = net.addHost('rsuc5', cls=Node, ip='')
    rsuc6 = net.addHost('rsuc6', cls=Node, ip='')

    rsuc1.cmd('sysctl -w net.ipv4.ip_forward=1')
    rsuc2.cmd('sysctl -w net.ipv4.ip_forward=1')
    rsuc3.cmd('sysctl -w net.ipv4.ip_forward=1')
    rsuc4.cmd('sysctl -w net.ipv4.ip_forward=1')
    rsuc5.cmd('sysctl -w net.ipv4.ip_forward=1')
    rsuc6.cmd('sysctl -w net.ipv4.ip_forward=1')

    h1suc1 = net.addHost('h1suc1', cls=Node,
                         ip='10.0.1.2/24', defualtRoute=None)
    h1suc2 = net.addHost('h1suc2', cls=Node,
                         ip='10.0.2.2/24', defualtRoute=None)
    h1suc3 = net.addHost('h1suc3', cls=Node,
                         ip='10.0.3.2/24', defualtRoute=None)
    h1suc4 = net.addHost('h1suc4', cls=Node,
                         ip='10.0.4.2/24', defualtRoute=None)
    h1suc5 = net.addHost('h1suc5', cls=Node,
                         ip='10.0.5.2/24', defualtRoute=None)
    h1suc6 = net.addHost('h1suc6', cls=Node,
                         ip='10.0.6.2/24', defualtRoute=None)

    info('* Add links\n')
    # Agregamos el link, ponemos nombre a la interfaz y le agregamos una IP.
    # Debe ir primero el router con la interfaz, luego el switch.
    # hay que poner nombres cortos en las interfaces sino te tira error.
    net.addLink(rcentral, swan1, intfName1='rcentral1-eth1',
                params1={'ip': '192.168.100.6/29'})
    net.addLink(rcentral, swan2, intfName1='rcentral1-eth2',
                params1={'ip': '192.168.100.14/29'})
    net.addLink(rcentral, swan3, intfName1='rcentral1-eth3',
                params1={'ip': '192.168.100.22/29'})
    net.addLink(rcentral, swan4, intfName1='rcentral1-eth4',
                params1={'ip': '192.168.100.30/29'})
    net.addLink(rcentral, swan5, intfName1='rcentral1-eth5',
                params1={'ip': '192.168.100.38/29'})
    net.addLink(rcentral, swan6, intfName1='rcentral1-eth6',
                params1={'ip': '192.168.100.46/29'})

    net.addLink(rsuc1, swan1, intfName1='rsuc1-eth0',
                params1={'ip': '192.168.100.1/29'})
    net.addLink(rsuc2, swan2, intfName1='rsuc2-eth0',
                params1={'ip': '192.168.100.9/29'})
    net.addLink(rsuc3, swan3, intfName1='rsuc3-eth0',
                params1={'ip': '192.168.100.17/29'})
    net.addLink(rsuc4, swan4, intfName1='rsuc4-eth0',
                params1={'ip': '192.168.100.25/29'})
    net.addLink(rsuc5, swan5, intfName1='rsuc5-eth0',
                params1={'ip': '192.168.100.33/29'})
    net.addLink(rsuc6, swan6, intfName1='rsuc6-eth0',
                params1={'ip': '192.168.100.41/29'})

    net.addLink(rsuc1, slan1, intfName1='rsuc1-eth1',
                params1={'ip': '10.0.1.1/24'})
    net.addLink(rsuc2, slan2, intfName1='rsuc2-eth1',
                params1={'ip': '10.0.2.1/24'})
    net.addLink(rsuc3, slan3, intfName1='rsuc3-eth1',
                params1={'ip': '10.0.3.1/24'})
    net.addLink(rsuc4, slan4, intfName1='rsuc4-eth1',
                params1={'ip': '10.0.4.1/24'})
    net.addLink(rsuc5, slan5, intfName1='rsuc5-eth1',
                params1={'ip': '10.0.5.1/24'})
    net.addLink(rsuc6, slan6, intfName1='rsuc6-eth1',
                params1={'ip': '10.0.6.1/24'})

    net.addLink(h1suc1, slan1)

    net.addLink(h1suc2, slan2)

    net.addLink(h1suc3, slan3)

    net.addLink(h1suc4, slan4)

    net.addLink(h1suc5, slan5)

    net.addLink(h1suc6, slan6)

    info('* Starting network\n')
    net.build()
    info('* Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('* Starting switches\n')
    net.get('slan1').start([])
    net.get('slan2').start([])
    net.get('slan3').start([])
    net.get('slan4').start([])
    net.get('slan5').start([])
    net.get('slan6').start([])

    net.get('swan1').start([])
    net.get('swan2').start([])
    net.get('swan3').start([])
    net.get('swan4').start([])
    net.get('swan5').start([])
    net.get('swan6').start([])

    info('* Post configure switches and hosts\n')

    # Agregar tabla de ruteo
    # si yo le pongo h1suc1.cmd('ip route add 10.0.2.0/24 via 10.0.1.1') - solo me dejaria hacer ping a la red .2 y no a las demas.
    # si le pongo h1suc1.cmd('ip route add 10.0.0.0/24 via 10.0.1.1'), no me dejarìa a ninguna por la mascara que no encapsula
    # a todas las /24, entoncs debo ponerle /21 para encajar als 6 redes /24
    h1suc1.cmd('ip route add 10.0.0.0/21 via 10.0.1.1')
    h1suc2.cmd('ip route add 10.0.0.0/21 via 10.0.2.1')
    h1suc3.cmd('ip route add 10.0.0.0/21 via 10.0.3.1')
    h1suc4.cmd('ip route add 10.0.0.0/21 via 10.0.4.1')
    h1suc5.cmd('ip route add 10.0.0.0/21 via 10.0.5.1')
    h1suc6.cmd('ip route add 10.0.0.0/21 via 10.0.6.1')

    rcentral.cmd('ip ro add 10.0.1.0/24 via 192.168.100.1')
    rcentral.cmd('ip ro add 10.0.2.0/24 via 192.168.100.9')
    rcentral.cmd('ip ro add 10.0.3.0/24 via 192.168.100.17')
    rcentral.cmd('ip ro add 10.0.4.0/24 via 192.168.100.25')
    rcentral.cmd('ip ro add 10.0.5.0/24 via 192.168.100.33')
    rcentral.cmd('ip ro add 10.0.6.0/24 via 192.168.100.41')

    # aca sucede lo mismo que con los hosts, quiero poder comunicarme con todas las redes /24 por eso ponemos mascara /21
    """
    Esto esta mal porque yo quiero llegar a los hosts entonces debo poner ro add red de los hosts, no red de los routers...
    si dejo esto asi, y hago ping de host1suc1 a host1suc2 me va a decir que no se puede conectar, pero la direccion la conoce.
    rsuc1.cmd('ip ro add 192.168.100.8/29 via 192.168.100.6')
    rsuc2.cmd('ip ro add 192.168.100.0/29 via 192.168.100.14')
    por eso la forma correcta es la siguiente que esta debajo:
    """
    rsuc1.cmd('ip ro add 10.0.2.0/24 via 192.168.100.6')
    rsuc2.cmd('ip ro add 10.0.1.0/24 via 192.168.100.14')
    rsuc1.cmd('ip ro add 10.0.0.0/21 via 192.168.100.6')
    rsuc2.cmd('ip ro add 10.0.0.0/21 via 192.168.100.14')
    rsuc3.cmd('ip ro add 10.0.0.0/21 via 192.168.100.22')
    rsuc4.cmd('ip ro add 10.0.0.0/21 via 192.168.100.30')
    rsuc5.cmd('ip ro add 10.0.0.0/21 via 192.168.100.38')
    rsuc6.cmd('ip ro add 10.0.0.0/21 via 192.168.100.46')

    CLI(net)
    net.stop()


if _name_ == '_main_':
    setLogLevel('info')
    myNetwork()
