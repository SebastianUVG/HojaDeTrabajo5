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

    