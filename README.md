# Chatbot de Gestión de Vacaciones — Org Empresarial S.A.

## Descripción

Trabajo Práctico Integrador de la materia Organización Empresarial
(Tecnicatura Universitaria en Programación — UTN).

Chatbot de consola desarrollado en Python que automatiza el proceso
de solicitud de vacaciones de una empresa ficticia. Implementa una
Máquina de Estados Finitos (FSM) alineada a un diagrama BPMN 2.0.

---

## Integrantes

| Maira Aguirre Gusmán |
| Patricio Elizaincin |

---

## Herramientas utilizadas

- Python 3
- bpmn.io (modelado del proceso)
- Visual Studio Code
- GitHub

---

## Proceso modelado

El chatbot automatiza el proceso de **solicitud de vacaciones**, siguiendo
el flujo definido en el diagrama BPMN 2.0 con dos lanes:

- **Empleado:** ingresa legajo, fecha y días, y confirma la solicitud
- **Sistema / Bot:** valida los datos, detecta errores y registra el resultado

### Compuertas implementadas

| Compuerta | Sí | No |
|---|---|---|
| ¿Legajo existe? | Muestra datos del empleado | Informa error, permite reintento |
| ¿Reintentar? | Vuelve a pedir legajo |
| ¿Formato de fecha válido? | Continúa con siguiente validación | Informa error de formato |
| ¿Saldo suficiente? | Continúa con siguiente validación | Informa saldo insuficiente |
| ¿Fechas disponibles? | Registra solicitud como PENDIENTE | Informa superposición de fechas |
| ¿Empleado confirma? | Aprueba la solicitud | Cancela la solicitud |

---

## Base de datos simulada

El sistema utiliza un diccionario en Python que simula una base de datos
de empleados. Cada empleado contiene nombre, área, saldo de días
disponibles e historial de solicitudes activas.

### Empleados disponibles para prueba

| Legajo | Nombre | Área | Días disponibles |
|---|---|---|---|
| 1001 | Juan Perez | Sistemas | 15 |
| 1002 | Maria Lopez | Administración | 10 |
| 1003 | Carlos Gomez | Recursos Humanos | 5 |

---

## Casos de prueba

| Caso | Legajo | Acción | Resultado esperado |
|---|---|---|---|
| Flujo completo OK | 1001 | Fecha válida + confirmar | Solicitud aprobada |
| Legajo inválido | 9999 | Ingresar legajo | Error: legajo no encontrado |
| Fecha inválida | 1001 | Fecha 32/13/2024 | Error: formato inválido |
| Saldo insuficiente | 1002 | Pedir 20 días | Error: saldo insuficiente |
| Superposición | 1003 | Fecha 01/01/2027 | Error: fechas ocupadas |
| Cancelar solicitud | 1001 | Fecha válida + n | Solicitud cancelada |
| Salir | cualquiera | Escribir salir | Fin del chatbot |

---

## Diagrama BPMN

El diagrama del proceso se encuentra en la carpeta `/docs` del repositorio.
Modelado con BPMN 2.0 usando bpmn.io, incluye:

- Pool: Gestión de Solicitud de Vacaciones — Org Empresarial S.A.
- Lane Empleado
- Lane Sistema / Bot
- 5 compuertas exclusivas XOR
- 3 eventos de fin (Fin OK, Fin Cancelado, Fin Error)

## Máquina de Estados FSM

El bot sabe en qué paso del proceso se encuentra gracias a la variable
`estado`. Cada valor representa un nodo del diagrama BPMN.

| Estado | Descripción |
|---|---|
| `inicio` | El empleado ingresa su legajo |
| `menu` | El empleado elige consulta o solicitud |
| `consulta` | Muestra saldo de días disponibles |
| `solicitud` | Valida fecha, días, saldo y superposición |
| `confirmando` | El empleado confirma o cancela la solicitud |
| `fin_cancelado` | El proceso termina por cancelación o salida |