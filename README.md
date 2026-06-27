# PokeHash: Gestor Táctico de Pokémon

**PokeHash** es un gestor táctico e interactivo diseñado para administrar información del universo Pokémon. La aplicación resuelve la necesidad de los jugadores (casuales y competitivos) de planificar y evaluar matemáticamente sus equipos antes de los combates, permitiéndoles consultar rápidamente estadísticas y debilidades elementales.

Lo que comenzó como una aplicación de consola ha evolucionado a una arquitectura dual moderna: **un motor lógico robusto y veloz escrito íntegramente en C, conectado a una elegante Interfaz Gráfica de Usuario (GUI) en Python.**

---

## Cómo Empezar

### Requisitos
- Compilador GCC instalado en el sistema.
- Python 3 instalado en el sistema (con la librería estándar `tkinter`).

### Compilación
El proyecto cuenta con dos ejecutables: la versión clásica de consola y la versión de Interfaz de Programación de Aplicaciones (API) para la GUI.
```bash
# Compilar versión clásica de Consola:
gcc -Wall -Wextra main.c pokehash.c tdas/extra.c tdas/list.c tdas/map.c -o pokehash

# Compilar versión API (Backend para la GUI):
gcc -Wall -Wextra pokehash_api.c pokehash.c tdas/extra.c tdas/list.c tdas/map.c -o pokehash_api
```

### Ejecución
Para iniciar la experiencia gráfica interactiva:
```bash
python3 gui.py
```
*(Si deseas usar la antigua versión por terminal, ejecuta `./pokehash`)*

---

## Estado de las Funcionalidades

### 1. Explorar Pokédex (Completado)
Interfaz interactiva para consultar el catálogo completo de Pokémon, con tiempos de respuesta instantáneos:
- **Búsqueda Dinámica:** Búsqueda en tiempo real por Nombre o por ID (Número de Pokédex) respaldada por una Tabla Hash $O(1)$.
- **Filtrado Avanzado:** Capacidad de filtrar el catálogo completo por Generación (1-9) y por Tipo Elemental. Dado que evalúa toda la Pokédex y luego ordena los resultados, esta operación tiene una complejidad temporal de $O(N \log N)$ (donde $N$ es la cantidad de Pokémon), lo cual sigue siendo imperceptiblemente rápido para el usuario.
- **Ficha Técnica:** Visualización completa de los Stats Base de cada Pokémon (HP, ATK, DEF, SPA, SPD, SPE) y su suma total (BST).

### 2. Gestión Estratégica de Equipo (Completado)
- **Construcción del Equipo:** Permite agregar hasta 6 integrantes seleccionándolos de la Pokédex.
- **Eliminación y Deshacer (Undo):** Capacidad de remover un Pokémon específico, o deshacer la última adición como en una pila LIFO $O(1)$.
- **Análisis Táctico en Tiempo Real:** El backend en C cruza los tipos del equipo entero contra una matriz de multiplicadores elementales, y la GUI te alerta visualmente (con colores verdes, rojos o amarillos) si tu equipo tiene balance positivo o debilidades descubiertas frente a cada uno de los 18 tipos elementales.
- **Alertas Críticas:** Identificación e informe automático de Pokémon que poseen debilidades críticas x4 a un tipo específico.

### 3. Exportación de Equipo a Archivo (Completado)
- Mediante un diálogo nativo de sistema, puedes exportar tu equipo actual. El motor en C procesa, formatea y guarda toda la ficha técnica en un archivo de texto plano para que lo compartas.

---

## Arquitectura y Estructuras de Datos (TDAs)

Para cumplir con las reglas del proyecto universitario, **toda la lógica, matemáticas y procesamiento de datos recaen 100% sobre el lenguaje C. Python solo actúa como una "vista tonta"** comunicándose con C vía formato JSON (Arquitectura JSON-RPC). Todos los TDAs de C se han implementado desde cero sin librerías externas:

1. **TDA Mapa (Tabla Hash con Chaining):**
   - Implementado en `map.c` usando una función de hashing (DJB2) y resolución de colisiones mediante listas enlazadas. Se utilizan dos instancias globales para lograr búsquedas instantáneas $O(1)$ tanto por Nombre como por ID.
2. **TDA Pila/Lista (Arreglo Estático de Equipo):**
   - Utilizado para gestionar el equipo activo. Al estar acotado estrictamente a 6 miembros, modela a la perfección la operación de deshacer (Undo) bajo la lógica LIFO (Last In, First Out).
3. **TDA Grafo (Matriz de Adyacencia):**
   - Modelado de multiplicadores elementales de daño como una matriz bidimensional estática de `float` de 18x18 (para los 18 tipos elementales), garantizando consultas de debilidades en tiempo $O(1)$.

## Integrantes y Tareas Realizadas

- **Cristóbal Sazo:** Coordinador de Proyecto.
  - Diseño e implementación de los TDAs Base (Tabla Hash y Listas Enlazadas).
  - Parser de datos (Carga desde `Pokemon.csv`).
  - Desarrollo del Gestor de Equipo (Lógica en C).
  - Implementación de búsqueda por ID.
  - Menú clásico de consola.
  - Desarrollo de la API JSON (Backend C).
  - Creación de la Interfaz Gráfica en Python (con asistencia de IA).
  - Lógica de exportación de equipos a archivo local.

- **Sebastián Riveros:** Comunicador.
  - Diseño de los TDAs Base.
  - Implementación de TDA Grafo (Matriz de adyacencia).
  - Algoritmo matemático de debilidades y cruce de tipos elementales.
  - Redacción y estructura de la documentación del proyecto.
  - Corrección de bugs.

- **Simón Guzmán:** Gestor de Calidad.
  - Diseño e implementación de funciones de busqueda con filtro.
  - Implementación de ranking de estadísticas.
  - Implementación de busqueda por tipo
  - Implementación de busqueda por generación.
  - Corrección de bugs.

- **Bruno Orellana:** Responsable de Integración y Consistencia.
  - Implementación de búsqueda por nombre.
  - Auditoría de consistencia de variables y testing general.

---

## Aspectos a Mejorar / Limitaciones
Como todo proyecto de software en desarrollo, existen áreas con oportunidades de mejora para futuras iteraciones:
1. **Top 10 Estadístico ausente en la GUI:** Aunque el código en C posee la lógica matemática para calcular y ordenar el Top 10 de Pokémon según sus estadísticas, no se construyó un panel visual en la Interfaz Gráfica para interactuar con esta función.
2. **Importación de Equipos:** El programa es capaz de exportar un equipo con éxito a un archivo de texto, pero actualmente no posee la función inversa (no se puede cargar un archivo `.txt` para restaurar un equipo guardado previamente).
3. **Ausencia de Habilidades (Abilities):** El cálculo táctico de inmunidades es puramente elemental basado en la matriz de Tipos. No toma en cuenta las Habilidades pasivas de los Pokémon que alteran las debilidades.
4. **Ausencia de Sprites (Imágenes):** Para mantener la aplicación ultraligera y libre de dependencias de internet, la GUI se basa puramente en texto y colores, sin almacenar imágenes.