import csv
import os

COLUMNAS = ["nombre", "poblacion", "superficie", "continente"]

#Las siguientes funciones trabajan sobre el archivo CSV

def crear_archivo(ruta):
    try:
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
            escritor.writeheader()
        return True
    except Exception:
        print("No se puede crear el archivo por lo que no se guardara")
        return False

def guardar_paises(ruta, paises):
    try:
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
            escritor.writeheader()
            for pais in paises:
                escritor.writerow(pais)
        return True
    except Exception:
        print("Error al guardar en el archivo CSV.")
        return False

def cargar_paises(ruta):
    paises = []
    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for  fila in lector:
                if not all(col in fila and fila[col] is not None for col in COLUMNAS):
                    continue
                nombre = fila["nombre"].strip()
                poblacion = convertir_positivo(fila["poblacion"])
                superficie = convertir_positivo(fila["superficie"])
                continente = fila["continente"].strip()

                if nombre != "" and continente != "" and poblacion is not None and superficie is not None:
                    if buscar_posicion(paises, nombre) == -1:
                        paises.append({
                            "nombre": nombre,
                            "poblacion": poblacion,
                            "superficie": superficie, 
                            "continente": continente
                        })
    except FileNotFoundError:
        print("El archivo no existe, se creaara uno nuevo")
        crear_archivo(ruta)
    except Exception:
        print("Error al leer el archivo, por favor verifique el formato")
    return paises

#Funciones que trabajan para validar entradas

def buscar_posicion(paises, nombre):
    nombre_buscado = nombre.strip().lower()
    for i in range(len(paises)):
        if paises[i]["nombre"].lower() == nombre_buscado:
            return i
    return -1

def pedir_entero(mensaje, minimo):
    while True:
        try:
            numero = int(input(mensaje))
            if numero < minimo:
                print(f"Error: El numero no debe ser menor a {minimo}")
                continue
            return numero
        except ValueError:
            print("Error: Ingrese un numero valido")

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("Error: El campo no debe estar vacio")
            continue
        if not texto.replace(" ", "").isalpha():
            print("Error: El campo solo debe contener letras")
            continue
        return texto

def convertir_positivo(texto):
    try:
        numero = int(str(texto).strip())
        if numero <= 0:
            return None
        return numero
    except Exception:
        return None

#Funciones basicas para visualizar, modificar

def mostrar_paises(lista, titulo="Listado de Paises"):
    if len(lista) == 0:
        print("No se cargaron los paises todavia")
        return
    print(f"\n===={titulo}====")
    for pais in lista:
        print(
            f"{pais['nombre']} | Continente: {pais['continente']} | "
            f"Poblacion: {pais['poblacion']} | Superficie: {pais['superficie']} km2"
        )

def agregar_paises(paises, ruta):
    print("\nAgregar Pais")
    nombre = pedir_texto("Ingrese el nombre del Pais: ")
    if buscar_posicion(paises, nombre) != -1:
        print(f"Error: El pais {nombre} ya esta cargado")
        return paises
    poblacion = pedir_entero(f"Ingrese la poblacion de {nombre}: ", 1)
    superficie = pedir_entero(f"Ingrese la superficie: ", 1)
    continente = pedir_texto(f"Ingrese el continente de {nombre}: ")

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })
    guardar_paises(ruta, paises)
    print(f"Se agrego el pais {nombre} correctamente")
    return paises

def actualizar_pais(paises, ruta):
    print("\nActualizar Datos de Pais")
    nombre = pedir_texto("Nombre del pais a actualizar: ")
    pos = buscar_posicion(paises, nombre)
    if pos == -1:
        print(f"Error: El pais ingresado no esta en el registro")
        return paises

    pais_actu = paises[pos]
    print(
        f"Datos actuales de {pais_actu['nombre']} | "
        f"Poblacion: {pais_actu['poblacion']} | Superficie: {pais_actu['superficie']} km2"
    )
    nueva_poblacion = pedir_entero("Nueva poblacion: ", 1)
    nueva_superficie = pedir_entero("Nueva superficie: ", 1)

    paises[pos]["poblacion"] = nueva_poblacion
    paises[pos]["superficie"] = nueva_superficie

    guardar_paises(ruta, paises)
    print(f"El pais {nombre} se actualizo correctamente")
    return paises

def buscar_pais(paises):
    print("\nBuscar Pais")
    termino = pedir_texto("Ingrese el nombre del pais: ").lower().strip()
    encontrado = []
    for pais in paises:
        if termino in pais["nombre"].lower():
            encontrado.append(pais)
    mostrar_paises(encontrado, f"\nResultados de busqueda para'{termino.title()}'")

#Funciones auxiliares para usar el sorted() u ordenamieto en otras funciones

def obtener_nombre(pais):
    return pais["nombre"].lower()

def obtener_poblacion(pais):
    return pais["poblacion"]

def obtener_superficie(pais):
    return pais["superficie"]

#Funciones de ordenamiento, filtro y estadisticas

def filtrar_paises(paises):
    if len(paises) == 0:
        print("Todavia no se han ingresado paises al registro")
        return
    print("\n==== FILTRAR PAISES ====")
    print("1. Por continente")
    print("2. Por poblacion")
    print("3. Por superficie")
    opcion = input("Elija una opcion del 1 al 3: ").strip()

    filtro = []
    match opcion:
        case "1":
            continente = pedir_texto("Ingrese el continente: ").lower()
            for pais in paises:
                if pais["continente"].lower() == continente:
                    filtro.append(pais)
            mostrar_paises(filtro, f"Paises del continente: {continente.upper()}")
        case "2":
            minimo = pedir_entero("Poblacion minima: ", 0)
            maximo = pedir_entero("Poblacion maxima: ", minimo)
            for pais in paises:
                if minimo <= pais["poblacion"] <= maximo:
                    filtro.append(pais)
            mostrar_paises(filtro, f"Paises con poblacion entre {minimo} y {maximo}:")
        case "3":
            minimo = pedir_entero("Superficie minima: ", 0)
            maximo = pedir_entero("Superficie maxima: ", minimo)
            for pais in paises:
                if minimo <= pais["superficie"] <= maximo:
                    filtro.append(pais)
            mostrar_paises(filtro, f"Paises con superficei entre {minimo} y {maximo}:")
        case _:
            print("Por favor, ingrese una opcion valida")

def ordenar_paises(paises):
    if len(paises) == 0:
        print("Error: Todavia no se han cargado los paises")
        return
    print("\n==== ORDENAR PAISES ====")
    print("1. Por nombre")
    print("2. Por poblacion")
    print("3. Por superficie")
    opcion = input("Ingrese una opcion del 1 al 3").strip()
    
    if opcion not in ("1", "2", "3"):
        print("Por favor ingrese una opcion de valida")
        return
    sentido = input("Indique ascendente(a) o descendente(d): ").strip().lower()
    if sentido == "a":
        descendente = False
        sentido_etiqueta = "ASCENDENTE"
    elif sentido == "d":
        descendente = True
        sentido_etiqueta = "DESCENDENTE"
    else:
        print("Sentido invalido. Por favor indique con 'a' o 'd'.")
        return
    match opcion:
        case "1":
            ordenados = sorted(paises, key=obtener_nombre, reverse=descendente)
            mostrar_paises(ordenados, f"PAISES ORDENADOS POR NOMBRE ({sentido_etiqueta})")
        case "2":
            ordenados = sorted(paises, key=obtener_poblacion, reverse=descendente)
            mostrar_paises(ordenados, f"PAISES ORDENADOS POR POBLACION ({sentido_etiqueta})")
        case "3":
            ordenados = sorted(paises, key=obtener_superficie, reverse=descendente)
            mostrar_paises(ordenados, f"PAISES ORDENADOS POR SUPERFICIE ({sentido_etiqueta})")

def mostrar_estadisticas(paises):
    if len(paises) == 0:
        print("Error: Todavia no se han cargado los paises")
        return
    print("\n==== ESTADISTICAS GENERALES ====")
    mayor_pob = paises[0]
    menor_pob = paises[0]
    suma_poblacion = 0
    suma_superficie = 0
    por_continente = {}

    for pais in paises:
        if pais["poblacion"] > mayor_pob["poblacion"]:
            mayor_pob = pais
        if pais["poblacion"] < menor_pob["poblacion"]:
            menor_pob = pais

        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        cont = pais["continente"]
        if cont in por_continente:
            por_continente[cont] += 1
        else:
            por_continente[cont] = 1

    total = len(paises)
    prom_poblacion = suma_poblacion / total
    prom_superficie = suma_superficie / total

    print(f"Pais con mayor poblacion: {mayor_pob['nombre']} ({mayor_pob['poblacion']}) habitantes")
    print(f"Pais con menor poblacion: {menor_pob['nombre']} ({menor_pob['poblacion']}) habitantes")
    print(f"Promedioo de poblacion total: {prom_poblacion:.2f} habitantes")
    print(f"Promedio de superficie: {prom_superficie:.2f} km2")
    print(f"\nCantidad de paises por continente:")
    for cont, cantidad in por_continente.items():
        print(f" - {cont}: {cantidad}")

#Funciones sobre el menu de interaccion

def mostrar_menu():
    print("\n===== GESTION DE DATOS DE PAISES =====")
    print("1. Listar todos los paises")
    print("2. Agregar un pais")
    print("3. Actualizar poblacion y superficie de un pais")
    print("4. Buscar pais por nombre")
    print("5. Filtrar paises")
    print("6. Ordenar paises")
    print("7. Mostrar estadisticas")
    print("8. Salir")

def main():
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta_script, "paises.csv")
    paises = cargar_paises(ruta)

    while True:
        mostrar_menu()
        opcion = input("Elegi una opcion del 1 al 8: ").strip()

        match opcion:
            case "1":
                mostrar_paises(paises)
            case "2":
                paises = agregar_paises(paises, ruta)
            case "3":
                paises = actualizar_pais(paises, ruta)
            case "4":
                buscar_pais(paises)
            case "5":
                filtrar_paises(paises)
            case "6":
                ordenar_paises(paises)
            case "7":
                mostrar_estadisticas(paises)
            case "8":
                guardar_paises(ruta, paises)
                print("Se guardaron los datos correctamente. Hasta luego!")
                break
            case _:
                print("Opcion invalida. Intente nuevamente")
if __name__ == "__main__":
    main()
''''
Se importo "import os" a ultimo momento debido a problemas con el csv ya que este se crea en la raiz de VSCode y no deberia, se aclara en el informe ante cualquier duda
y el mismo es para que al ejecutarlo desde otro equipo arrancara bien sin necesidad de buscar el archivo por todos lados como le paso al estudiante :c

'''