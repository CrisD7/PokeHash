# Contenidos del Informe

### **1\. Introducción**

* **Contextualización y Propósito:** Identificación del problema, nicho o vacío al que apunta la aplicación o videojuego propuesto.  
* **Visión General:** Resumen de la aplicación indicando sus principales características, fortalezas y alcance (lo que puede y no puede hacer).  
* **Generación de interés:** Explicación de por qué la solución propuesta es relevante o innovadora.

### **2\. Descripción de la Aplicación e Interacción (Evalúa Rúbrica: Criterio 1 \- 20%)**

* **Mapa de Navegación:** Esquema jerárquico claro de los menús, submenús o estados del juego.  
* **Flujo de Interacción Detallado**: Explicación exhaustiva de la comunicación aplicación-usuario por consola para todas las funcionalidades principales.  
  * *Escenario ideal de uso:* Entradas esperadas por el usuario y respuestas normales del sistema.  
  * *Escenarios críticos y manejo de errores:* Detalle explícito de los mensajes, alertas o validaciones que mostrará el sistema ante datos inválidos, movimientos ilegales o búsquedas sin resultados.

### **3\. Arquitectura de Datos y Estructuras (Evalúa Rúbrica: Criterios 2 y 3\)**

En esta sección se define cómo se representará y almacenará la información en el sistema, yendo desde las unidades más básicas hasta las estructuras de colección.

* **Modelamiento de Entidades:** Definición formal de los `structs` que componen el sistema, detallando sus atributos y tipos de datos (ej. `struct Pelicula`, `struct Usuario`).  
* **Instancias y Selección de TDAs:** Declaración explícita de los Tipos de Datos Abstractos (TDAs) que se utilizarán y **las instancias globales o principales que existirán en el sistema** (ej. "Se utilizará un TDA Mapa instanciado como *Mapa de Películas* para indexar el catálogo usando como clave el id de la película y como valor un dato de tipo Pelicula, y un TDA Lista instanciado como *Lista de Favoritos* por cada usuario"). Se debe justificar por qué estos TDAs modelan bien el problema.  
* **Estructuras de Datos Físicas:** Separación estricta del nivel conceptual. Indicación de la estructura física subyacente en memoria para cada TDA (ej. "El *Mapa de Películas* será una Tabla Hash con encadenamiento"). Argumentación técnica de por qué esa estructura física es la más adcuada.

### **4\. Diseño de la Solución Algorítmica (Evalúa Rúbrica: Criterio 2\)**

Con las entidades y estructuras ya definidas, en esta sección se detalla cómo interactúa el sistema para cumplir con las funcionalidades.

* **Lógica Operacional por Funcionalidad:** Explicación algorítmica paso a paso de las funcionalidades.  
  * *Importante:* Se debe explicar la lógica **haciendo referencia a las instancias declaradas en el punto anterior** (ej. *"Se utiliza la operación `buscar(clave)` sobre el Mapa de Películas"*) y utilizando exclusivamente las operaciones formales de los TDAs, respetando la barrera de abstracción (sin mencionar punteros ni índices).  
* **Algoritmos *Core* o Técnicas Especiales:** Si alguna funcionalidad basa su funcionamiento en un algoritmo avanzado o técnica particular (ej. motor de recomendaciones, algoritmos en grafos como BFS/DFS/Dijkstra, heurísticas de filtrado), se debe dedicar un sub-apartado exclusivo para detallar su lógica. Se debe explicar cómo este algoritmo específico interactúa lógicamente con las instancias de los TDAs para lograr el objetivo.

### **5\. Análisis de Complejidad *(Evalúa Rúbrica: Criterio 4 \- 15%)***

* **Complejidad Temporal y Espacial**: Análisis de los peores casos (Worst-Case) para todas las funciones del sistema.  
* **Justificación de Bajo Nivel**: Argumentación matemática explícita que sustente los costos basándose en el comportamiento interno de la estructura física declarada en el punto anterior (ej. recorrido de punteros, direccionamiento directo, colisiones).

### **6\. Aspecto Desafiante *(Evalúa Rúbrica: Criterio 5 \- Parte del 20%)***

* **Identificación del Reto Técnico**: Exposición de un desafío real de alto nivel computacional y de programación en lenguaje C.  
  * *Ejemplos válidos:* Gestión manual de la memoria dinámica (evitar *memory leaks*), control complejo de punteros al combinar y sincronizar múltiples estructuras simultáneamente, algoritmos combinatorios o IA para juegos.

### **7\. Planificación y Contribución del Equipo *(Evalúa Rúbrica: Criterio 5 \- Parte del 20%)***

* **Distribución de Roles**: Descripción detallada de las responsabilidades operativas y técnicas de cada integrante (Coordinador, Comunicador, Gestor de Calidad, Integrador, etc.).  
* **Planificación**: Periodo de tiempo en que las tareas fueron o serán realizadas (uso de Carta Gantt).  
* **Lista de tareas realizadas por cada integrante del equipo.**

### **8\. Conclusión**

* Análisis crítico del trabajo realizado, destacando fortalezas y debilidades de las decisiones arquitectónicas tomadas.  
* Observaciones relevantes que demuestren un dominio transversal del tema y de las Estructuras de Datos.