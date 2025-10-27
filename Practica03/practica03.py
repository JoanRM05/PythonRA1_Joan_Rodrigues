import csv
from typing import List, Set, Dict

class RegistroHorario:
    def __init__(self, empleado: str, dia: str, entrada: int, salida: int):
        self.empleado = empleado
        self.dia = dia
        self.entrada = entrada
        self.salida = salida

    def duracion(self) -> int:
        """Devuelve la cantidad de horas trabajadas en este registro"""
        return self.salida - self.entrada


class Empleado:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.registros: List[RegistroHorario] = []

    def agregar_registro(self, registro: RegistroHorario):
        """Añade un registro horario al empleado"""
        self.registros.append(registro)

    def horas_totales(self) -> int:
        """Calcula las horas totales trabajadas"""
        return sum(registro.duracion() for registro in self.registros)

    def dias_trabajados(self) -> int:
        """Devuelve el número de días distintos trabajados"""
        return len({registro.dia for registro in self.registros})

    def fila_csv(self) -> List:
        """Devuelve una fila para el CSV de resumen"""
        return [self.nombre, self.dias_trabajados(), self.horas_totales()]


class GestorHorarios:
    def __init__(self):
        self.empleados: Dict[str, Empleado] = {}

    def leer_csv(self, archivo: str):
        """Lee el archivo CSV y agrupa los registros por empleado"""
        try:
            with open(archivo, newline='', encoding='utf-8') as f:
                lector = csv.reader(f, delimiter=';', quotechar='"')
                for fila in lector:
                    nombre, dia, h_entrada, h_salida = fila
                    entrada = int(h_entrada)
                    salida = int(h_salida)
                    registro = RegistroHorario(nombre, dia, entrada, salida)
                    if nombre not in self.empleados:
                        self.empleados[nombre] = Empleado(nombre)
                    self.empleados[nombre].agregar_registro(registro)
        except FileNotFoundError:
            print(f"Error: El archivo {archivo} no se encontró")
            self.empleados = {}

    def escribir_resumen(self, archivo_salida: str):
        """Escribe el resumen en un archivo CSV"""
        with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            escritor.writerow(['Empleado', 'Dias_trabajados', 'Horas_totales'])
            for empleado in self.empleados.values():
                escritor.writerow(empleado.fila_csv())


def leer_registros(archivo: str) -> List[RegistroHorario]:
    registros = []
    try:
        with open(archivo, newline='', encoding='utf-8') as f:
            lector = csv.reader(f, delimiter=';', quotechar='"')
            for fila in lector:
                
                nombre, dia, h_entrada, h_salida = fila
                entrada = int(h_entrada)
                salida = int(h_salida)
                registro = RegistroHorario(nombre, dia, entrada, salida)
                registros.append(registro)

    except FileNotFoundError:
        print(f"Error: El archivo {archivo} no se encontró")
    return registros

def empleados_madrugadores(registros: List[RegistroHorario], hora_referencia: int) -> Set[str]:
    madrugadores = {r.empleado for r in registros if r.entrada <= hora_referencia}
    with open('Practica03/resource/madrugadores.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['Empleado'])
        for empleado in madrugadores:
            escritor.writerow([empleado])
    return madrugadores

def empleados_por_dia(registros: List[RegistroHorario]) -> Dict[str, Set[str]]:
    empleados_por_dia = {}
    for registro in registros:
        if registro.dia not in empleados_por_dia:
            empleados_por_dia[registro.dia] = set()
        empleados_por_dia[registro.dia].add(registro.empleado)
    return empleados_por_dia

def empleados_lunes_y_viernes(empleados_por_dia: Dict[str, Set[str]]):
    lunes = empleados_por_dia.get('Lunes', set())
    viernes = empleados_por_dia.get('Viernes', set())
    interseccion = lunes & viernes
    with open('Practica03/resource/en_dos_dias.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['Empleado'])
        for empleado in interseccion:
            escritor.writerow([empleado])
    return interseccion

def empleados_sabado_no_domingo(empleados_por_dia: Dict[str, Set[str]]):
    sabado = empleados_por_dia.get('Sábado', set())
    domingo = empleados_por_dia.get('Domingo', set())
    diferencia = sabado - domingo
    with open('Practica03/resource/exclusivos_sabado_no_domingo.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['Empleado'])
        for empleado in diferencia:
            escritor.writerow([empleado])
    return diferencia

def resumen_semanal(registros: List[RegistroHorario]):
    resumen = {}
    for registro in registros:
        if registro.empleado not in resumen:
            resumen[registro.empleado] = {'dias': set(), 'horas': 0}
        resumen[registro.empleado]['dias'].add(registro.dia)
        resumen[registro.empleado]['horas'] += registro.duracion()
    
    with open('Practica03/resource/resumen_semanal.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['Empleado', 'Dias_trabajados', 'Horas_totales'])
        for empleado, datos in resumen.items():
            escritor.writerow([empleado, len(datos['dias']), datos['horas']])

def empleados_turno_largo(registros: List[RegistroHorario]) -> Set[str]:
    turnos_por_empleado = {}
    for registro in registros:
        if registro.empleado not in turnos_por_empleado:
            turnos_por_empleado[registro.empleado] = []
        turnos_por_empleado[registro.empleado].append(registro.duracion())
    
    empleados_largos = {emp for emp, turnos in turnos_por_empleado.items() if all(t >= 6 for t in turnos)}
    with open('Practica03/resource/turnos_largos.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['Empleado'])
        for empleado in empleados_largos:
            escritor.writerow([empleado])
    return empleados_largos

def main():
    
    registros = leer_registros('Practica03/resource/horarios.csv')
    if not registros:
        return
    
    hora_referencia = 8

    madrugadores = empleados_madrugadores(registros, hora_referencia)
    print(f"Empleados que empiezan antes de las {hora_referencia}: {madrugadores}")

    emp_por_dia = empleados_por_dia(registros)
    for dia, empleados in emp_por_dia.items():
        print(f"{dia}: {empleados}")

    interseccion = empleados_lunes_y_viernes(emp_por_dia)
    print(f"Empleados que trabajaron Lunes y Viernes: {interseccion}")

    exclusivos = empleados_sabado_no_domingo(emp_por_dia)
    print(f"Empleados que trabajaron Sábado pero no Domingo: {exclusivos}")
    print("Operación utilizada: Diferencia (sábado - domingo)")

    resumen_semanal(registros)
    print("Se ha generado el fichero resumen_horarios.csv")

    turnos_largos = empleados_turno_largo(registros)
    print(f"Empleados con todos sus turnos >= 6 horas: {turnos_largos}")

    gestor = GestorHorarios()
    gestor.leer_csv('Practica03/resource/horarios.csv')
    gestor.escribir_resumen('Practica03/resource/resumen_clases.csv')
    print("Se ha generado el fichero resumen_clases.csv")

if __name__ == "__main__":
    main()