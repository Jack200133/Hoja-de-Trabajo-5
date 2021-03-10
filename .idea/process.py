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
    run = True
    while run:
        yield RAM.get(Ram_need)
        print(' %s esta listo para empezar, con un tienpo de %s, ram = %s' % (
            name, env.now,  Ram_need))
        while cant_inst > 0:

            with CPU.request() as req:

                yield req
                yield env.timeout(3)
                cant_inst = cant_inst - 3
                if(cant_inst < 0):
                    cant_inst = 0
                print(' %s Hace 3 procesos, con un tienpo de %s y queda con %s penientes' %
                      (name, env.now, cant_inst))
            feo = random.randint(1, 3)
            if(feo == 1):
                with wait_time.request() as req:
                    yield req
                    yield env.timeout(1)
                    print(' %s entra a espera, con un tienpo de %s' % (
                        name, env.now))
        RAM.put(Ram_need)
        print(' %s FINALIZADO, finaliza con un tienpo de %s' %
              (name, env.now))
        run = False


env = simpy.Environment()  # crea el ambiente de simulacion
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=3)
wait = simpy.Resource(env, capacity=25)

random.seed(10)

for i in range(50):
    Cantint = random.randint(1, 10)

    Ram_need = (random.expovariate(1/10) % 10+1)

    env.process(process(env, 'Proceso %d' %
                        i, round(Ram_need), Cantint, CPU, wait, RAM))

env.run()
