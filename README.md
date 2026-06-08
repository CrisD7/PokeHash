# PokeHash: Gestor Táctico de Pokémon

**PokeHash** es un gestor táctico e interactivo de consola diseñado en lenguaje C para administrar información del universo Pokémon. La aplicación resuelve la necesidad de los jugadores (casuales y competitivos VGC/Smogon) de planificar y evaluar matemáticamente sus equipos antes de los combates, permitiéndoles consultar rápidamente estadísticas y debilidades sin depender de herramientas externas.

---

## 🚀 Cómo Empezar

### Requisitos
- Compilador GCC instalado en el sistema.

### ⚙️ Compilación
Para compilar el proyecto junto con sus estructuras de datos auxiliares (TDAs):
```bash
gcc -Wall -Wextra main.c pokehash.c tdas/extra.c tdas/list.c tdas/map.c -o pokehash
```

### 🎮 Ejecución
Para iniciar el programa:
```bash
./pokehash
```

---

## 🛠️ Estado de las Funcionalidades

### 1. Explorar Pokédex (Completado)
Submenú interactivo para consultar el catálogo de Pokémon importado masivamente desde `Pokemon.csv` al iniciar el programa:
- **1.1. Buscar por Nombre:** Búsqueda directa case-insensitive en la tabla hash. (Eficiencia: promedio $O(1)$).
- **1.2. Buscar por Número de Pokédex (ID):** Búsqueda directa indexada en una tabla secundaria de IDs en $O(1)$.
- **1.3. Buscar con Filtro:** Filtra Pokémon ingresando la generación y el tipo, mostrando los resultados en una tabla alineada en consola.

### 2. Gestión Estratégica de Equipo (En desarrollo)
- **2.1. Agregar Pokémon al Equipo:** Selección de hasta 6 integrantes para el equipo activo.
- **2.2. Ver Equipo Actual:** Visualización del equipo y sus estadísticas base.
- **2.3. Analizar Debilidades del Equipo:** Reporte de vulnerabilidades tipo cruzando multiplicadores elementales.
- **2.4. Deshacer última adición (Undo):** Remoción del último Pokémon añadido usando la estructura LIFO de una pila.

### 3. Exportar Equipo a Archivo (En desarrollo)
- Guardado del equipo actual y su correspondiente análisis estratégico de tipos en un archivo de texto local.

---

## 🏗️ Arquitectura y Estructuras de Datos (TDAs)

Para cumplir con las reglas del proyecto universitario, **todos los TDAs se han implementado desde cero sin librerías externas**:

1. **TDA Mapa (Tabla Hash con Chaining):**
   - Implementado en [map.c](file:///home/cris/PokeHash/PokeHash/tdas/map.c) usando una función de hashing (DJB2) y resolución de colisiones mediante listas enlazadas. Se utilizan dos instancias globales para lograr búsquedas instantáneas $O(1)$ tanto por Nombre como por ID.
2. **TDA Pila (Stack de Arreglo Estático):**
   - Utilizado para gestionar el equipo activo. Al estar acotado estrictamente a 6 miembros, modela a la perfección la operación de deshacer (Undo) bajo la lógica LIFO (Last In, First Out).
3. **TDA Grafo (Matriz de Adyacencia):**
   - Modelado de multiplicadores elementales de daño como una matriz bidimensional estática de `float` de 18x18 (para los 18 tipos elementales), garantizando consultas de debilidades en tiempo $O(1)$.

---

## 👥 Integrantes y Roles
- **Cristóbal Sazo:** Coordinador de Proyecto (Planificación y ritmos de desarrollo).
- **Sebastián Riveros:** Comunicador (Documentación y contacto con cátedra).
- **Simón Guzmán:** Gestor de Calidad (Metodología ágil y Git).
- **Bruno Orellana:** Responsable de Integración y Consistencia (Auditoría de consistencia de variables y testing).