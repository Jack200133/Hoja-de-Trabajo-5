import simpy
import random

#el proceso se tiene que crear esperando espacio de memoria disponible
#luego de asignarle la memoria espera a que el procesador lo atienda
# y tiene una anctidad de instruciones para realizar
# EL CPU atiende el proceso por tiempo limitado para hacer 3 instrucciones

# name: identificador del proceso
# Ram_need: cantidad de ram necesitado
# cant_inst: cantidad de instrucciones

def process(env,name,Ram_need,cant_inst,CPU,wait_time):




    with CPU.request() as req:
        yield req
        if (cant_inst > 3):
            temp = 3
            print('%s realizando proceso en CPU con %s procesos' % (name,temp))
            yield env.timeout(1)
            cant_inst = cant_inst - temp
            print('%s tinene %s intruccioes pendientes' % (name,cant_inst))
        if (cant_inst <= 3):
            print('%s realizando proceso en CPU con %s procesos' % (name,cant_inst))
            yield env.timeout(1)
            print('%s termino sus intrucciones en %s' % (name,env.now))

env = simpy.Environment() #crea el ambiente de simulacion
RAM = simpy.Container(env, init=100,capacity=100)
CPU = simpy.Resource(env,capacity=3)

random.seed(10)

for i in range(10):
    Cantint = random.randint(1,10)
    env.process(process(env,'Proceso %d' % i, random.expovariate(1.0/10),Cantint,CPU,0))