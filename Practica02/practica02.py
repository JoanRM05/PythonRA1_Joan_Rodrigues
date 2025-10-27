import json

horarios = {}

def load_horarios():
    try:
        with open('Practica02/resource/horarios.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        horarios = {}
        for nombre, tiempos in data.items():
            horarios[nombre] = (tiempos[0], tiempos[1])
        
        return horarios
    
    except FileNotFoundError:
        print("Error: El archivo 'horarios.json' no se encuentra en la ruta especificada.")
        return {}
    except json.JSONDecodeError:
        print("Error: El archivo 'horarios.json' tiene un formato JSON inválido.")
        return {}

def menu():
    """
    Menú principal repetitivo (bucle while) para elegir acciones:
      1) Mostrar registros
      2) Contar entradas
      3) Salir
    """
    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Salir")
        opcion = input("Elige una opción (1-3): ").strip()
 
        if opcion == '1':
            mostrar_registros()
        elif opcion == '2':
            contar_entradas()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")
 
 
def mostrar_registros():
    print("\nRegistros de horarios: \n")
    
    for indice, (nombre, (entrada, salida)) in enumerate(horarios.items()):
        print(f"{indice}: {nombre} = Entrada - {entrada}, Salida - {salida}")
    print("\n")


def validar_hora(hora_str):
    try:
        hora_str = hora_str.strip().replace(" ", "")
        hora, mins = hora_str.split(":", 1)
        hora_int = int(hora)
        mins_int = int(mins)

        if 0 <= hora_int <= 23 and 0 <= mins_int <= 59:
            return True, hora_int, mins_int
        else:
            return False, None, None
    except ValueError:
        return False, None, None


def contar_entradas():
    
    contador = 0
    while True:

        hora_ref = input("Ingrese la hora de referencia de entrada (00:00 - 23:00): ")

        validar, hora_ref_int, mins_ref_int = validar_hora(hora_ref)
        
        """ debugpy.breakpoint() """
        
        if validar:
            break
        else:
            print("Formato incorrecto, ingrese la hora en formato HH:MM (Ej: 09:30)")
            continue


    for nombre, (entrada, salida) in horarios.items():
        
        validar, hora_entrada_int, mins_entrada_int = validar_hora(entrada)

        if not validar:
            print(f"Formato incorrecto en la hora de entrada de {nombre}, se esperaba HH:MM")
            continue

        if hora_entrada_int < hora_ref_int:
            contador += 1
        elif hora_entrada_int == hora_ref_int and mins_entrada_int <= mins_ref_int:
            contador += 1

    print(f"\nNúmero de empleados que han entrado a las {hora_ref_int}:{mins_ref_int} o antes: {contador}\n")

    
if __name__ == '__main__':
    horarios = load_horarios()
    menu()

