# ============================================================
# CHATBOT - GESTIÓN DE VACACIONES
# TPI - Organización Empresarial
# Autores: Maira Aguirre Gusmán y Patricio Elizaincin
#
# Este chatbot implementa una Máquina de Estados Finitos (FSM)
# alineada al diagrama BPMN del proceso de solicitud de
# vacaciones. Cada bloque elif representa un nodo del diagrama.
# ============================================================

# datetime: convierte el string de fecha a un objeto fecha
# timedelta: calcula la fecha de fin sumando los días solicitados
from datetime import datetime, timedelta

# -------------------------------------------------------------
# BASE DE DATOS SIMULADA
# Diccionario que simula una base de datos de empleados.
# Cada empleado tiene nombre, área, saldo de días y
# un historial de solicitudes para detectar superposiciones.
# -------------------------------------------------------------
empleados = {
    "1001": {
        "nombre": "Juan Perez",
        "area": "Sistemas",
        "dias": 15,
        "solicitudes": []
    },
    "1002": {
        "nombre": "Maria Lopez",
        "area": "Administración",
        "dias": 10,
        "solicitudes": []
    },
    "1003": {
        "nombre": "Carlos Gomez",
        "area": "Recursos Humanos",
        "dias": 5,
        "solicitudes": [
            {
                "fecha_inicio": "01/01/2027",
                "dias": 3,
                "estado": "APROBADA"
            }
        ]
    }
}

# Variable de estado — controla el flujo de la FSM
# Cada valor representa un nodo del diagrama BPMN
estado = "inicio"

print(" CHATBOT DE GESTIÓN DE VACACIONES ")
print(" Escriba 'salir' para cancelar en cualquier momento.")

# -----------------------------------------
# BUCLE PRINCIPAL — MÁQUINA DE ESTADOS
# Cada iteración procesa un estado y define
# la transición al siguiente según el BPMN
# -----------------------------------------
while True:

    # ----------------------------------------
    # ESTADO: inicio
    # Nodo de inicio del diagrama BPMN.
    # El empleado ingresa su número de legajo.
    # ----------------------------------------
    if estado == "inicio":

        legajo = input("\nIngrese su número de legajo: ")

        if legajo.lower() == "salir":
            estado = "fin_cancelado"
            continue

        # Compuerta: Legajo existe?
        # Sí -> muestra datos y pasa al menú
        # No -> informa error y vuelve a pedir legajo
        if legajo not in empleados:
            print("Error: Legajo no encontrado.")
            continue

        empleado = empleados[legajo]
        print(f"\nBienvenido {empleado['nombre']}")
        print(f"Área  : {empleado['area']}")
        estado = "menu"

    # --------------------------------------
    # ESTADO: menu
    # Permite al empleado elegir una acción.
    # --------------------------------------
    elif estado == "menu":

        print("\n--- MENÚ ---")
        print("1. Consultar saldo de días")
        print("2. Solicitar vacaciones")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            estado = "consulta"
        elif opcion == "2":
            estado = "solicitud"
        elif opcion == "3":
            estado = "fin_cancelado"
        else:
            print("Opción inválida.")

    # --------------------------------------
    # ESTADO: consulta
    # Muestra el saldo de días disponibles.
    # --------------------------------------
    elif estado == "consulta":

        print(f"\nUsted posee {empleado['dias']} días disponibles.")
        estado = "menu"

    # --------------------------------------------
    # ESTADO: solicitud
    # Tarea de usuario — lane Empleado.
    # El empleado ingresa fecha de inicio y días.
    # --------------------------------------------
    elif estado == "solicitud":

        if empleado["dias"] == 0:
            print("\nNo posee días disponibles.")
            estado = "menu"
            continue

        fecha_str = input("\nIngrese fecha de inicio (DD/MM/AAAA): ").strip()
        if fecha_str.lower() == "salir":
            estado = "fin_cancelado"
            continue

        # Compuerta: Formato de fecha válido?
        # Sí -> continúa con la siguiente compuerta
        # No -> informa error y vuelve a pedir fecha
        try:
            fecha_dt = datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            print("Error: formato de fecha inválido. Use DD/MM/AAAA.")
            continue

        try:
            dias_pedidos = int(input("¿Cuántos días desea solicitar? "))
            if dias_pedidos <= 0:
                print("Debe ingresar un número mayor a 0.")
                continue
        except ValueError:
            print("Error: Debe ingresar un número.")
            continue

        # Compuerta: Saldo suficiente?
        # Sí -> continúa con la siguiente compuerta
        # No -> informa saldo insuficiente y vuelve
        if dias_pedidos > empleado["dias"]:
            print(f"\nSaldo insuficiente.")
            print(f"  Disponible : {empleado['dias']} días")
            print(f"  Solicitado : {dias_pedidos} días")
            continue

        # Compuerta: Fechas disponibles?
        # Sí -> registra la solicitud como PENDIENTE
        # No -> informa superposición y vuelve a pedir fechas
        # Se verifica que el período no se superponga con
        # solicitudes activas del mismo empleado
        fecha_fin = fecha_dt + timedelta(days=dias_pedidos - 1)
        hay_superposicion = False

        for sol in empleado["solicitudes"]:
            if sol["estado"] in ["PENDIENTE", "APROBADA"]:
                sol_ini = datetime.strptime(sol["fecha_inicio"], "%d/%m/%Y")
                sol_fin = sol_ini + timedelta(days=sol["dias"] - 1)
                if not (fecha_fin < sol_ini or fecha_dt > sol_fin):
                    hay_superposicion = True
                    break

        if hay_superposicion:
            print("\nError: las fechas se superponen con una solicitud activa.")
            print("Elija un período diferente.")
            continue

        # Las tres compuertas pasaron -> registrar como PENDIENTE
        empleado["solicitudes"].append({
            "fecha_inicio": fecha_str,
            "dias": dias_pedidos,
            "estado": "PENDIENTE"
        })

        # Mostrar resumen antes de la confirmación
        print("\n--- RESUMEN DE SOLICITUD ---")
        print(f"Empleado     : {empleado['nombre']}")
        print(f"Área         : {empleado['area']}")
        print(f"Fecha inicio : {fecha_str}")
        print(f"Días         : {dias_pedidos}")
        print(f"Saldo actual : {empleado['dias']} días")

        estado = "confirmando"

    # ---------------------------------------
    # ESTADO: confirmando
    # Tarea de usuario — lane Empleado.
    # Compuerta: Empleado confirma?
    # Sí -> actualiza a APROBADA y descuenta días
    # No -> actualiza a CANCELADA y vuelve al menú
    # ---------------------------------------
    elif estado == "confirmando":

        confirmacion = input("\n¿Confirma la solicitud? (s/n): ").strip().lower()

        # Empleado confirma? -> Sí - Registro Aprobado
        if confirmacion == "s":
            empleado["solicitudes"][-1]["estado"] = "APROBADA"
            empleado["dias"] -= dias_pedidos
            print("\nRegistro aprobado.")
            print(f"Días restantes: {empleado['dias']}")
            estado = "menu"

        # Empleado confirma? -> No - Cancelar solicitud
        elif confirmacion == "n":
            empleado["solicitudes"][-1]["estado"] = "CANCELADA"
            print("\nSolicitud cancelada.")
            estado = "menu"

        # Camino infeliz: entrada inválida
        else:
            print("Opción inválida. Ingrese 's' o 'n'.")

    # -----------------------------------------
    # ESTADO: fin_cancelado
    # Evento de fin del diagrama BPMN.
    # -----------------------------------------
    elif estado == "fin_cancelado":
        print("\nGracias por utilizar el Chatbot.")
        break