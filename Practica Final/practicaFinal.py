import csv
import os
from datetime import datetime, date

# /**
#  * Diccionario en memoria con los clientes indexados por id.
#  */
clientes = {}
# /**
#  * Diccionario en memoria con los eventos indexados por id.
#  */
eventos = {}
# /**
#  * Lista con todas las ventas cargadas desde el CSV.
#  */
ventas = []

# /** Ruta al CSV de clientes. */
CLIENTES_FILE = "Practica Final/data/clientes.csv"
# /** Ruta al CSV de eventos. */
EVENTOS_FILE = "Practica Final/data/eventos.csv"
# /** Ruta al CSV de ventas. */
VENTAS_FILE = "Practica Final/data/ventas.csv"
# /** Ruta de salida para el informe resumido. */
INFORME_FILE = "Practica Final/data/informe_resumen.csv"

class Cliente:
    """/**
    * Representa un cliente que viene del CSV.
    * @param id_cliente identificador entero del cliente.
    * @param nombre nombre completo.
    * @param email correo electronico validado basico.
    * @param fecha_alta fecha en la que se dio de alta.
    */"""
    def __init__(self, id_cliente, nombre, email, fecha_alta):
        self.id = id_cliente
        self.nombre = nombre
        self.email = email
        self.fecha_alta = fecha_alta

    def antiguedad_dias(self):
        """/**
        * Calcula cuantos dias han pasado desde la fecha de alta.
        * @return numero de dias como entero.
        */"""
        return (date.today() - self.fecha_alta).days

    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.email}) alta {self.fecha_alta}"


class Evento:
    """/**
    * Modelo simple para un evento con categoria y precio.
    * @param id_evento identificador entero.
    * @param nombre titulo del evento.
    * @param categoria familia del evento.
    * @param fecha fecha del evento como date.
    * @param precio precio unitario en euros.
    */"""
    def __init__(self, id_evento, nombre, categoria, fecha, precio):
        self.id = id_evento
        self.nombre = nombre
        self.categoria = categoria
        self.fecha = fecha
        self.precio = precio

    def dias_hasta_evento(self):
        """/**
        * Calcula cuantos dias faltan para la fecha del evento.
        * @return dias restantes (puede ser negativo si ya paso).
        */"""
        return (self.fecha - date.today()).days

    def __str__(self):
        return f"{self.id} - {self.nombre} [{self.categoria}] {self.fecha} precio {self.precio} (faltan {self.dias_hasta_evento()} dias)"


class Venta:
    """/**
    * Representa una venta asociada a cliente y evento.
    * @param id_venta identificador entero de la venta.
    * @param cliente_id id del cliente que compra.
    * @param evento_id id del evento comprado.
    * @param cantidad numero de entradas.
    * @param total importe total de la venta.
    * @param fecha fecha de la venta.
    */"""
    def __init__(self, id_venta, cliente_id, evento_id, cantidad, total, fecha):
        self.id = id_venta
        self.cliente_id = cliente_id
        self.evento_id = evento_id
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha

    def __str__(self):
        return f"Venta {self.id} cliente {self.cliente_id} evento {self.evento_id} total {self.total} fecha {self.fecha}"


def parse_fecha(texto):
    """/**
    * Convierte una cadena en formato YYYY-MM-DD a objeto date.
    * @param texto cadena con la fecha a parsear.
    * @return fecha como objeto date.
    */"""
    return datetime.strptime(texto.strip(), "%Y-%m-%d").date()


def validar_email(texto):
    """/**
    * Valida un email de forma muy basica.
    * @param texto correo a revisar.
    * @return True si parece valido, False si no.
    */"""
    if "@" not in texto or texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    if not usuario or "." not in dominio:
        return False
    if dominio.startswith(".") or dominio.endswith("."):
        return False
    return True


def cargar_datos():
    """/**
    * Lee los CSV de clientes, eventos y ventas y llena las colecciones globales.
    * @return None
    */"""
    global clientes, eventos, ventas
    clientes = {}
    eventos = {}
    ventas = []

    if os.path.exists(CLIENTES_FILE):
        with open(CLIENTES_FILE, newline='', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                try:
                    cliente = Cliente(
                        int(fila['id']),
                        fila['nombre'].strip(),
                        fila['email'].strip(),
                        parse_fecha(fila['fecha_alta'])
                    )
                    clientes[cliente.id] = cliente
                except Exception as error:
                    print("Error en fila de clientes:", error)
    else:
        print("No se encontró clientes.csv")

    if os.path.exists(EVENTOS_FILE):
        with open(EVENTOS_FILE, newline='', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                try:
                    evento = Evento(
                        int(fila['id']),
                        fila['nombre'].strip(),
                        fila['categoria'].strip(),
                        parse_fecha(fila['fecha']),
                        float(fila['precio'])
                    )
                    eventos[evento.id] = evento
                except Exception as error:
                    print("Error en fila de eventos:", error)
    else:
        print("No se encontró eventos.csv")

    if os.path.exists(VENTAS_FILE):
        with open(VENTAS_FILE, newline='', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                try:
                    venta = Venta(
                        int(fila['id']),
                        int(fila['cliente_id']),
                        int(fila['evento_id']),
                        int(fila['cantidad']),
                        float(fila['total']),
                        parse_fecha(fila['fecha'])
                    )
                    ventas.append(venta)
                except Exception as error:
                    print("Error en fila de ventas:", error)
    else:
        print("No se encontró ventas.csv")

    print("Clientes cargados:", len(clientes))
    print("Eventos cargados:", len(eventos))
    print("Ventas cargadas:", len(ventas))


def listar(tabla):
    """/**
    * Muestra por pantalla el contenido de la tabla solicitada.
    * @param tabla texto: 'clientes', 'eventos' o 'ventas'.
    * @return None
    */"""
    if tabla == 'clientes':
        if not clientes:
            print("No hay clientes para mostrar")
            return
        for cliente in clientes.values():
            print(cliente)
    elif tabla == 'eventos':
        if not eventos:
            print("No hay eventos para mostrar")
            return
        for evento in eventos.values():
            print(evento)
    elif tabla == 'ventas':
        if not ventas:
            print("No hay ventas para mostrar")
            return
        for venta in ventas:
            print(venta)
    else:
        print("Tabla no reconocida")


def pedir_fecha(mensaje):
    """/**
    * Solicita una fecha al usuario hasta que sea valida.
    * @param mensaje texto que se muestra por input.
    * @return objeto date introducido por el usuario.
    */"""
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Introduce una fecha")
            continue
        try:
            return parse_fecha(texto)
        except ValueError:
            print("Formato incorrecto, usa YYYY-MM-DD")


def siguiente_id_clientes():
    """/**
    * Busca el siguiente id disponible para clientes.
    * @return entero con el nuevo id.
    */"""
    max_id = 0
    for clave in clientes.keys():
        if clave > max_id:
            max_id = clave

    if os.path.exists(CLIENTES_FILE):
        try:
            with open(CLIENTES_FILE, newline='', encoding='utf-8') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    try:
                        valor = int(fila.get('id', 0))
                        if valor > max_id:
                            max_id = valor
                    except Exception:
                        continue
        except FileNotFoundError:
            pass
    return max_id + 1


def alta_cliente():
    """/**
    * Da de alta un cliente nuevo pidiendo los datos por consola.
    * @return None
    */"""
    nombre = input("Nombre del cliente: ").strip()
    if not nombre:
        print("El nombre es obligatorio")
        return

    email = input("Email del cliente: ").strip()
    if not validar_email(email):
        print("Email no valido")
        return

    fecha_alta = pedir_fecha("Fecha de alta (YYYY-MM-DD): ")

    nuevo_id = siguiente_id_clientes()
    cliente = Cliente(nuevo_id, nombre, email, fecha_alta)
    clientes[nuevo_id] = cliente

    carpeta = os.path.dirname(CLIENTES_FILE)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)

    archivo_existia = os.path.exists(CLIENTES_FILE)
    with open(CLIENTES_FILE, 'a', newline='', encoding='utf-8') as f:
        campos = ['id', 'nombre', 'email', 'fecha_alta']
        escritor = csv.DictWriter(f, fieldnames=campos)
        if not archivo_existia:
            escritor.writeheader()
        escritor.writerow({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'email': cliente.email,
            'fecha_alta': cliente.fecha_alta.isoformat()
        })

    print("Cliente creado con id", cliente.id)


def filtrar_ventas_por_rango():
    """/**
    * Filtra las ventas por un rango de fechas introducido por el usuario.
    * @return lista de ventas que cumplan el rango.
    */"""
    if not ventas:
        print("No hay ventas en memoria")
        return []

    fecha_inicio = pedir_fecha("Fecha inicio (YYYY-MM-DD): ")
    fecha_fin = pedir_fecha("Fecha fin (YYYY-MM-DD): ")

    if fecha_fin < fecha_inicio:
        print("La fecha fin debe ser mayor o igual que la fecha inicio")
        return []

    filtradas = []
    for venta in ventas:
        if fecha_inicio <= venta.fecha <= fecha_fin:
            filtradas.append(venta)

    if not filtradas:
        print("No se encontraron ventas en ese rango")
    else:
        for venta in filtradas:
            datos_cliente = clientes.get(venta.cliente_id)
            datos_evento = eventos.get(venta.evento_id)
            nombre_cliente = datos_cliente.nombre if datos_cliente else "?"
            nombre_evento = datos_evento.nombre if datos_evento else "?"
            print(f"{venta.fecha} - {nombre_cliente} - {nombre_evento} - {venta.total}")

    return filtradas


def estadisticas():
    """/**
    * Calcula estadisticas generales sobre las ventas y eventos.
    * @return None
    */"""
    if not ventas or not eventos:
        print("Carga datos primero")
        return

    ingresos_totales = 0
    ingresos_evento = {}
    unidades_evento = {}

    for venta in ventas:
        ingresos_totales += venta.total
        ingresos_evento[venta.evento_id] = ingresos_evento.get(venta.evento_id, 0) + venta.total
        unidades_evento[venta.evento_id] = unidades_evento.get(venta.evento_id, 0) + venta.cantidad

    categorias = set()
    precios = []
    dias_proximos = []

    for evento in eventos.values():
        categorias.add(evento.categoria)
        precios.append(evento.precio)
        if evento.fecha >= date.today():
            dias_proximos.append(evento.dias_hasta_evento())

    if precios:
        precio_min = min(precios)
        precio_max = max(precios)
        precio_media = sum(precios) / len(precios)
    else:
        precio_min = precio_max = precio_media = 0

    if dias_proximos:
        dias_proximo_evento = min(dias_proximos)
    else:
        dias_proximo_evento = None

    print("Ingresos totales:", round(ingresos_totales, 2))
    print("Ingresos por evento:")
    for evento_id, total in ingresos_evento.items():
        datos_evento = eventos.get(evento_id)
        nombre_evento = datos_evento.nombre if datos_evento else "?"
        unidades = unidades_evento.get(evento_id, 0)
        print(f"  {nombre_evento}: {round(total, 2)} euros ({unidades} unidades)")

    if categorias:
        print("Categorias registradas:", ", ".join(sorted(categorias)))
    else:
        print("No hay categorias cargadas")

    if dias_proximo_evento is None:
        print("No hay eventos futuros")
    else:
        print("Dias hasta el proximo evento:", dias_proximo_evento)

    print(f"Resumen precios (min, max, media): ({precio_min}, {precio_max}, {round(precio_media, 2)})")


def exportar_informe():
    """/**
    * Genera el informe resumen en CSV con totales por evento.
    * @return None
    */"""
    if not ventas:
        print("No hay ventas para exportar")
        return

    ingresos_evento = {}
    unidades_evento = {}
    for venta in ventas:
        ingresos_evento[venta.evento_id] = ingresos_evento.get(venta.evento_id, 0) + venta.total
        unidades_evento[venta.evento_id] = unidades_evento.get(venta.evento_id, 0) + venta.cantidad

    carpeta = os.path.dirname(INFORME_FILE)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)

    with open(INFORME_FILE, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(['evento_id', 'evento', 'ingresos', 'unidades'])
        for evento_id, total in ingresos_evento.items():
            datos_evento = eventos.get(evento_id)
            nombre_evento = datos_evento.nombre if datos_evento else f"Evento {evento_id}"
            escritor.writerow([evento_id, nombre_evento, round(total, 2), unidades_evento.get(evento_id, 0)])

    print("Informe creado en", INFORME_FILE)


def mostrar_menu():
    """/**
    * Enseña el menu principal y devuelve la opcion elegida.
    * @return cadena con la opcion.
    */"""
    print("\n--- Menu ---")
    print("1. Cargar datos")
    print("2. Listar clientes")
    print("3. Listar eventos")
    print("4. Listar ventas")
    print("5. Alta cliente")
    print("6. Filtrar ventas por fechas")
    print("7. Ver estadisticas")
    print("8. Exportar informe")
    print("9. Salir")
    return input("Elige una opcion: ").strip()


def main():
    """/**
    * Punto de entrada del programa, mantiene el bucle del menu.
    * @return None
    */"""
    opcion = ''
    while opcion != '9':
        opcion = mostrar_menu()
        if opcion == '1':
            cargar_datos()
        elif opcion == '2':
            listar('clientes')
        elif opcion == '3':
            listar('eventos')
        elif opcion == '4':
            listar('ventas')
        elif opcion == '5':
            alta_cliente()
        elif opcion == '6':
            filtrar_ventas_por_rango()
        elif opcion == '7':
            estadisticas()
        elif opcion == '8':
            exportar_informe()
        elif opcion == '9':
            print("Hasta luego")
        else:
            print("Opcion incorrecta")


if __name__ == '__main__':
    main()
