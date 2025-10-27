hora_salida_mas_temprana = 24
trabajador_salida_mas_temprana = ""
contador_entradas = 0

trabajadores = input("Ingrese el número de trabajadores: ")
print(trabajadores)
num_trabajadores = int(trabajadores)
 
hora_ref = input("Ingrese la hora de referencia (0-23): ")

while not hora_ref.isdigit() or not (0 <= int(hora_ref) <= 23):
    print("Hora incorrecta, ingrese un valor entre 0 y 23")
    hora_ref = input("Ingrese la hora de referencia (0-23): ")

hora_referencia = int(hora_ref)

while num_trabajadores > 0 :
    
    nombre = input("Ingrese el nombre del trabajador: ")

    hora_entrada = input("Ingrese la hora de entrada del trabajador (0-23): ")  
    while not hora_ref.isdigit() or not (0 <= int(hora_ref) <= 23):
        print("Hora incorrecta, ingrese un valor entre 0 y 23")
        hora_entrada = input("Ingrese la hora de entrada del trabajador (0-23): ")

    hora_entrada_int = int(hora_entrada)

    hora_salida = input("Ingrese la hora de salida del trabajador (0-23): ")
    while not hora_ref.isdigit() or not (0 <= int(hora_ref) <= 23):
        print("Hora incorrecta, ingrese un valor entre 0 y 23")
        hora_salida = input("Ingrese la hora de salida del trabajador (0-23): ")
    
    hora_salida_int = int(hora_salida)
    
    if hora_salida_int <= hora_entrada_int:
        print("Error: La hora de salida debe ser mayor que la hora de entrada para el trabajador", nombre,". Se omite este registro sin contabilizarlo.")
        continue

    if hora_entrada_int <= hora_referencia:
        contador_entradas += 1
    
    if hora_salida_int < hora_salida_mas_temprana:
        hora_salida_mas_temprana = hora_salida_int
        trabajador_salida_mas_temprana = nombre
    
    num_trabajadores -= 1
else:
    if trabajador_salida_mas_temprana:
        print(f"El trabajador con la salida más temprana es {trabajador_salida_mas_temprana} a las {hora_salida_mas_temprana} horas")
    else:
        print("No se registraron trabajadores con horarios válidos")
        
    print(f"Número de trabajadores que entraron antes o a la hora de referencia: {contador_entradas}")