import json

print("Programa gestión de pacientes.")

class PacienteYaRegistradoError(Exception):
    pass

class IDNoValidoError(Exception):
    pass

pacientes = []  # Lista de pacientes
pac_registrados = set()  # Conjunto para pacientes registrados
diag_previos = set()  # Conjunto de diagnósticos previos
id_paciente = 1  # ID inicial


# Función para guardar los pacientes (en el archivo JSON) opcion 5
def guardar_pacientes(pacientes):
    try:
        with open('pacientes.json', 'w') as f:
            json.dump(pacientes, f, indent=4)
        print("Datos guardados correctamente.")
    except FileNotFoundError as e:
        print(f"No se encontró el archivo: {e}")
    except json.JSONDecodeError as e:
        print(f"El formato del archivo es incorrecto: {e}")

# Función Recursiva para guardar dianósticos   
def agregar_diagnostico(diagnosticos):
    diagnostico = input("Ingrese el diagnóstico del paciente o 'salir' para volver al menu principal: ").lower()
    if diagnostico == 'salir':
        return diagnosticos # Devuelve la lista de diagnósticos
    if not diagnostico:
        print("El diagnóstico no puede estar vacío.")
        return agregar_diagnostico(diagnosticos)  # Llamada recursiva si el diagnóstico está vacío.
    diagnosticos.append(diagnostico)
    return agregar_diagnostico(diagnosticos)  # Llamada recursiva para seguir agregando diagnósticos.



# Función para agregar un paciente / opcion 1
def agregar_paciente(pacientes, pac_registrados, id_paciente):
    nombre = input("Ingrese el nombre del paciente: ").lower()
    try:
        if any(caracter.isdigit() for caracter in nombre):
            raise ValueError("El nombre no puede contener números.")
    except ValueError as e:
        print(f"Error: {e}")
        return agregar_paciente(pacientes, pac_registrados, id_paciente)
    
    if nombre in pac_registrados:
        raise PacienteYaRegistradoError(f"El paciente {nombre} ya está registrado.")

    try:
        edad = int(input("Ingrese la edad del paciente: "))
    except ValueError:
        print("La edad introducida no es un número")
        return agregar_paciente(pacientes, pac_registrados, id_paciente)

    sexo = input("Ingrese el sexo del paciente (M/F): ").upper()
    
    paciente = {  # Crear un diccionario con los datos del paciente
        'ID': id_paciente,
        'Nombre': nombre,
        'Edad': edad,
        'Sexo': sexo,
        'diagnosticos': []  # lista de diagnósticos vacía
    }

    # Conjunto para agregar diagnóstico
    #while True:
    #    diagnostico = input("Ingrese el diagnóstico del paciente o 'salir' para volver al menu principal: ").lower()
    #    if diagnostico == 'salir':
    #        break  # Sale del while
    #    if not diagnostico:
    #        print("El diagnóstico no puede estar vacío.")
    #           continue
    #    paciente['diagnosticos'].append(diagnostico)  # Agregar el diagnóstico al conjunto


    # Llamar a la funcion recursiva para agregar diagnosticos
    paciente['diagnosticos'] = agregar_diagnostico(paciente['diagnosticos'])

    pacientes.append(paciente)  # Agregar paciente a la lista
    pac_registrados.add(nombre)  # Agregar el nombre al conjunto

    opcion = input("Presione 5 para guardar al paciente.")

    if opcion == '5':
            guardar_pacientes(pacientes)
            return pacientes
    print(f"Paciente {nombre} (ID: {id_paciente}) agregado correctamente.")
    return id_paciente + 1  # Incrementar el ID para el siguiente paciente



# Función para mostrar la lista de pacientes / opcion 2 / 1 imprimimos si no esta, 2 recorremos los elementos y si esta imprimimos el diccionario
def mostrar_pacientes(pacientes):
    if not pacientes:
        print("No hay pacientes registrados.")
        return

    print("\nLista de pacientes registrados:")
    for paciente in pacientes:  #for_in_ recorre elemento por elemento
        print(f"Paciente ID: {paciente['ID']}") #busca en el diccionario
        print(f"Nombre: {paciente['Nombre']}")
        print(f"Edad: {paciente['Edad']}")
        print(f"Sexo: {paciente['Sexo']}")
        print(f"Diagnósticos previos: {paciente['diagnosticos']}")



# Función para buscar paciente por nombre / opcion 3
def buscar_paciente(pacientes, nombre):
    for paciente in pacientes:
        if paciente['Nombre'].lower() == nombre.lower():
            print(f"Datos del paciente {nombre} (ID: {paciente['ID']}):")
            print(f"Edad: {paciente['Edad']}")
            print(f"Sexo: {paciente['Sexo']}")
            print(f"Diagnósticos previos: {paciente['diagnosticos']}")
            return
    print(f"El paciente {nombre} no está registrado.")
    return



# Función para buscar paciente por ID / opcion 4 
def buscar_paciente_id(pacientes):
    id_paciente = input("Ingrese el ID del paciente: ")

    try:
        id_paciente = int(id_paciente)

    except ValueError:
        print("El ID debe ser un número.")
        return
    
    for paciente in pacientes:
        if paciente['ID'] == id_paciente:
            print(f"Datos del paciente (ID: {paciente['ID']}):")
            print(f"Nombre: {paciente['Nombre']}")
            print(f"Edad: {paciente['Edad']}")
            print(f"Sexo: {paciente['Sexo']}")
            print(f"Diagnósticos previos: {paciente['diagnosticos']}")
            return
        
    print(f"El paciente con ID {id_paciente} no está registrado.")


# Modificar un elemento del archivo / opcion 6
def modificar_paciente():
    nom_modificar = input("Ingrese el nombre del paciente a modificar: ").lower()
    diag_modificar = input("Ingrese el diagnóstico a modificar: ").lower()
    edad_modificar = int(input("Ingrese la edad a modificar: "))
    sexo_modificar = input("Ingrese el sexo a modificar: ").upper()

    try:
        # Abrir el archivo JSON para leer los datos
        with open("pacientes.json", "r") as f:
            lista_pacientes = json.load(f)

        paciente_encontrado = False                
        for paciente in lista_pacientes:
            if paciente['Nombre'].lower() == nom_modificar: 
                paciente['diagnosticos'].append(diag_modificar)
                paciente['Edad'] == edad_modificar
                paciente['Sexo'] == sexo_modificar
                paciente_encontrado = True

        if not paciente_encontrado:
            print("No se encontró un paciente con ese nombre.")
        else:
            with open ("pacientes.json", "w") as f:
                json.dump(lista_pacientes, f, indent=4)

        #with open ("pacientes.json", "w") as f:
        #    f.write(lista_str)

    except FileNotFoundError as e:
        print(f"No se encontró el archivo: {e}")
    except json.JSONDecodeError as e:
        print(f"El formato del archivo es incorrecto: {e}")


# Función principal
def main():
    global id_paciente

    while True:
        print("\nOpciones:")
        print("1. Agregar paciente")
        print("2. Mostrar lista de pacientes")
        print("3. Buscar paciente por nombre")
        print("4. Buscar paciente por ID")
        print("5. Guardar pacientes")
        print("6. Modificar datos de un paciente")
        print("7. Salir")
        opcion = input("Seleccione una opción (1-7): ")

        if opcion == '1':
                id_paciente = agregar_paciente(pacientes, pac_registrados, id_paciente)
        elif opcion == '2':
            mostrar_pacientes(pacientes)
        elif opcion == '3':
            nombre_buscar = input("Ingrese el nombre del paciente a buscar: ")
            buscar_paciente(pacientes, nombre_buscar)
        elif opcion == '4':
            buscar_paciente_id(pacientes)
        elif opcion == '5':
            guardar_pacientes(pacientes)
        elif opcion == "6":
            modificar_paciente()
        elif opcion == '7':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

#if __name__ == "__main__":
main()