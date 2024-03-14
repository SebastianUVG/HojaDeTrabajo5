#Sebastian Garcia Bustamante 22291
#Hoja de trabajo #5
#Estructura de datos
#Basado en algunoes ejemplos proporcionados por el profesor.
#Python 3.9.9 64bits

#importar  librerias
import simpy
import random

class Proceso:
    def __init__(self, env, ram, cpu, wait, velocidad, MRam, NPro, Ninst):
        self.env = env
        self.ram = ram
        self.cpu = cpu
        self.wait = wait
        self.velocidad = velocidad
        self.MRam = MRam
        self.NPro = NPro
        self.Ninst = Ninst
        self.Ttotal = 0.0
        self.tiempo = []

        self.env.process(self.ejecutar_procesos())

    def ejecutar_procesos(self):
        for i in range(self.NPro):
            tiempo_proceso = random.expovariate(1.0 / self.Ninst)
            NIns = random.randint(1, 10)
            CRam = random.randint(1, 10)
            self.env.process(self.proceso(f'Proceso {i}', CRam, NIns, tiempo_proceso))

        yield self.env.timeout(0)  # Para que el proceso no termine inmediatamente y permita ejecutar la simulación

    def proceso(self, nom, cantRam, NIns, tiempo_proceso):
        yield self.env.timeout(tiempo_proceso)
        print(f'{nom}. Solicita {cantRam} de RAM (New)')
        tiempo_inicial = self.env.now

        yield self.ram.get(cantRam)
        print(f'{nom}. Solicitud aceptada por {cantRam} de RAM (Admited)')

        tiempo_final = 0

        while tiempo_final < NIns:
            with self.cpu.request() as req:
                yield req
                if (NIns - tiempo_final) >= self.velocidad:
                    efec = self.velocidad
                else:
                    efec = (NIns - tiempo_final)

                print(f'{nom}. CPU ejecutara {efec} instrucciones. (Ready)')
                yield self.env.timeout(efec / self.velocidad)

                tiempo_final += efec
                print(f'{nom}. CPU ({tiempo_final}/{NIns}) completado. (Running)')

            decision = random.randint(1, 2)

            if decision == 1 and tiempo_final < NIns:
                with self.wait.request() as req2:
                    yield req2
                    yield self.env.timeout(1)
                    print(f'{nom}. Realizadas operaciones de entrada/salida. (Waiting)')

        yield self.ram.put(cantRam)
        print(f'{nom}. Retorna {cantRam} de RAM. (Terminated)')
        self.Ttotal += (self.env.now - tiempo_inicial)
        self.tiempo.append(self.env.now - tiempo_inicial)

# Definición de variables
velocidad = 6.0
Mram = 100
Procesos = 50
Ninst = 5  # Define el número de intervalos para la generación de tiempos de llegada
random.seed(5555)
# Ambientes de simulación
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=2)
ram = simpy.Container(env, init=Mram, capacity=Mram)
espera = simpy.Resource(env, capacity=2)

# Creación de la instancia de la clase Proceso
proceso_instancia = Proceso(env, ram, cpu, espera, velocidad, Mram, Procesos, Ninst)

# Se corre la simulación
env.run()

# Se calcula el tiempo promedio
promedio = (proceso_instancia.Ttotal / Procesos)
print("El tiempo promedio de los procesos es:", promedio, "segundos")

# Se calcula la desviación estándar
suma = sum((i - promedio)**2 for i in proceso_instancia.tiempo)
desviacion = (suma / (Procesos - 1))**0.5
print("La desviación estándar de los tiempos es:", desviacion, "segundos")
