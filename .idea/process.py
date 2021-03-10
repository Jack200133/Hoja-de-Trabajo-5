import simpy
import random
import math
# el proceso se tiene que crear esperando espacio de memoria disponible
# luego de asignarle la memoria espera a que el procesador lo atienda
# y tiene una anctidad de instruciones para realizar
# EL CPU atiende el proceso por tiempo limitado para hacer 3 instrucciones

# name: identificador del proceso
# Ram_need: cantidad de ram necesitado
# cant_inst: cantidad de instrucciones


def process(env, name, Ram_need, cant_inst, CPU, wait_time, RAM):
    global totaldia
    totaldia = 0
    llegada = env.now
    run = True
    while run:
        yield RAM.get(Ram_need)
        print(' %s esta listo para empezar, con un tiempo de %s, ram = %s' % (
            name, env.now,  Ram_need))
        while cant_inst > 0:

            with CPU.request() as req:

                yield req
                yield env.timeout(1)
                cant_inst = cant_inst - 3  # cantidad de instrucciones x unidad de tiempo
                if(cant_inst < 0):
                    cant_inst = 0
                print(' %s Hace 3 procesos, con un tiempo de %s y queda con %s penientes' %
                      (name, env.now, cant_inst))
            # random por si se va aespera o vuelve al CPU
            feo = random.randint(1, 3)
            if(feo == 1):
                with wait_time.request() as req:
                    yield req
                    yield env.timeout(1)
                    print(' %s entra a espera, con un tiempo de %s' % (
                        name, env.now))
        RAM.put(Ram_need)  # regresa la ram que uso este proceso
        tiempo = env.now - llegada
        print(' %s FINALIZADO, finaliza con un tiempo de %s' %
              (name, tiempo))
        totaldia = totaldia + tiempo
        run = False


env = simpy.Environment()  # crea el ambiente de simulacion
RAM = simpy.Container(env, init=100, capacity=100)  # capacidad del RAM
CPU = simpy.Resource(env, capacity=1)  # cantidad de CPUS
# cantidad de colas para la espera a CPU
wait = simpy.Resource(env, capacity=3)
cantidadpro = 50  # cantidad de procesos
random.seed(10)  # seed del random

for i in range(cantidadpro):
    Cantint = random.randint(1, 10)  # cantidad de uinstrucciones x proceso

    Ram_need = (random.expovariate(1/10) % 10+1)  # cantidad de ram x proceso

    env.process(process(env, 'Proceso %d' %
                        i, round(Ram_need), Cantint, CPU, wait, RAM))

env.run()
print('Tiempo promedio ', totaldia/cantidadpro)
