# Laboratorios de Redes y Sistemas Distribuidos

## Descripción del Laboratorio 1: Desarrollo de una API
El laboratorio consiste en diseñar una API con Flask para gestionar una base de datos de películas. Se organiza en cuatro etapas:
* Configuración del Entorno: Crear un entorno virtual con venv e instalar librerías necesarias.
* Desarrollo de la API: Implementar funcionalidades para gestionar películas (búsqueda, actualización, eliminación, listados y sugerencias).
* Integración Externa: Conectar la API con una API de feriados para recomendar películas según el género y próximos feriados.
* Evaluación: Probar funcionalidades con scripts y herramientas como Postman, enfocándose en eficiencia, escalabilidad y seguridad.

El laboratorio fomenta habilidades en diseño de APIs y programación con Python.
Vea con más detalles: [Aquí](Laboratorio%201:%20Desarrollo%20de%20una%20API/2024%20Lab1_enunciado.pdf)

## Descripción del Laboratorio 2: Aplicación Servidor
Este laboratorio se centra en la implementación de un servidor de archivos utilizando sockets en Python, empleando un protocolo casero llamado HFTP (Home-made File Transfer Protocol). Se organiza en las siguientes etapas:
* Implementación del Servidor:
Diseñar un servidor que utilice HFTP para gestionar solicitudes como listado, metadatos, fragmentos de archivos y cierre de conexión.
Garantizar robustez frente a comandos malformados o intencionadamente incorrectos.
* Manejo de Conexiones:
Configurar el servidor para manejar múltiples clientes utilizando hilos o poll.
Probar comandos con herramientas como Telnet y clientes proporcionados.
* Evaluación y Extensión:
Probar casos exitosos y no exitosos con scripts y realizar pruebas entre diferentes máquinas en red.
Implementar soporte para múltiples clientes simultáneos y documentar los resultados.

Este laboratorio refuerza conceptos de programación cliente/servidor, diseño de protocolos personalizados y manejo eficiente de conexiones en red.

## Descripción del Laboratorio 3: Transporte
Este laboratorio utiliza Omnet++ para analizar y diseñar modelos de red, enfocándose en el control de congestión y flujo. Se organiza en dos tareas principales:

* Análisis del Modelo de Red:
Simular un modelo de red basado en colas para estudiar el impacto de tasas de transferencia y tamaños de buffer.
Configurar casos de estudio con distintos parámetros y realizar mediciones como demoras, pérdidas de paquetes y utilización de buffers.
Producir gráficos de carga ofrecida vs. carga útil y analizar cuellos de botella en el sistema.

* Diseño de Soluciones:
Implementar un sistema de control de flujo y congestión para evitar pérdidas por saturación de buffers.
Diseñar un canal de retorno entre el receptor y el transmisor para regular la tasa de transmisión mediante feedback.
Realizar simulaciones y comparar los resultados con y sin control de congestión.

El laboratorio promueve habilidades en simulación de redes, análisis de tráfico y diseño de algoritmos eficientes para redes congestionadas.

## Descripción del laboratorio 4: Red

Este laboratorio se centra en el análisis y diseño de estrategias de enrutamiento en redes simuladas con Omnet++. Los objetivos principales son:

* Comprender y modelar redes: Se provee un modelo de red en anillo con 8 nodos conectados mediante enlaces full-duplex.

* Análisis del enrutamiento: La capa de red básica proporcionada enruta paquetes utilizando una única interfaz fija. Se deben medir métricas como la demora, cantidad de saltos y utilización de recursos.
* Experimentos:
Caso 1: Analizar el rendimiento con tráfico generado por dos nodos hacia un destino común.
Caso 2: Explorar el comportamiento cuando todos los nodos generan tráfico hacia un único nodo, determinando un valor de estabilidad de la red según el intervalo de llegada.
* Diseño de una nueva estrategia de enrutamiento: Se solicita implementar un algoritmo más eficiente, comparar los resultados con los casos anteriores y proponer mejoras adicionales.
* Tarea opcional (estrella): Diseñar una estrategia de enrutamiento adaptable a cualquier topología, incluyendo nodos con múltiples interfaces o interfaces inactivas.

El laboratorio busca desarrollar habilidades en el diseño de protocolos de red y evaluación de rendimiento mediante simulación.
