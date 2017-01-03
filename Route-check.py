from jnpr.junos import Device
from jnpr.junos.op.routes import RouteTable

'''
 List with host names and correspondent IP's to display to user
 and select which one to connect to. This code assumes Device#1 and 2
 are logical-systems for learning purposes.
'''
host_names = [ 'Device#1','Device#2','Device#3','Device#4' ]
host_ips = [ '1.1.1.1','2.2.2.2','3.3.3.3','4.4.4.4' ]

def seleccion_host():
        print 'Select host: '
        counter_temp = 1
        for host in host_names:
                print counter_temp, ') ', host
                counter_temp = counter_temp + 1

        while True:
                seleccion = input('Write #: ')
                if seleccion < 1 or seleccion > 4:
                        continue
                else:
                        break
        return seleccion

''' Handle Device functions '''
def crear_Device(hostp,userp,passwordp):
        return Device(host=hostp,user=userp,password=passwordp)

def abrir_Device(devp):
        devp.open()
        return

def cerrar_Device(devp):
        devp.close()
        return

def crear_RouteTable(devp):
        return RouteTable(devp)

''' Obtain routes from object RouteTable '''
def obtener_rutas_RouteTable(rt,prefijo,seleccion):
        if seleccion == 1 or seleccion == 2:
                rt.get( destination=prefijo,
                   table='inet.0',
                   logical_system='LSYS-NAME'+str(seleccion) )
        else:
                rt.get( destination=prefijo, table = 'inet.0' )
        return

def cli_showroute_Device(devp,prefijo,seleccion):
        comando = 'show route table inet.0 ' + prefijo
        if seleccion == 1 or seleccion == 2:
                comando = comando + ' logical-system LSYS-NAME' + str(seleccion)
        return devp.cli(comando)

''' Returns a tuple with interface description '''
def cli_int_description_Device(devp,interface):
        desc_int_logica = devp.cli('show interfaces descriptions ' + interface)
        int_fis = interface.split('.')[0]
        desc_int_fisica = devp.cli('show interfaces descriptions ' + int_fis)
        return desc_int_logica, desc_int_fisica

seleccion = seleccion_host()
dev = crear_Device(host_ips[seleccion-1], 'username', 'password')
print 'opening device...'
abrir_Device(dev)
print 'device open!'
print 'creating RouteTable object...'
table = crear_RouteTable(dev)
print 'RouteTable object created!'

# Ingress IP address 
ingreso_ip = raw_input('Ingress IP prefix: ')
print 'obtaining route information...'
obtener_rutas_RouteTable(table,ingreso_ip,seleccion)
print 'route information obtained'
print cli_showroute_Device(dev,ingreso_ip,seleccion)
print 'Interface Description:'
desc_int_log, desc_int_fis = cli_int_description_Device(dev,table[0]['via'])
print desc_int_log
print desc_int_fis
print 'closing device...'
cerrar_Device(dev)
print 'device closed'
