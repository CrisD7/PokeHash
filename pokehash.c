#include "pokehash.h"
#include "tdas/extra.h"
#include <strings.h>
#include <ctype.h>

Map *pokedex = NULL;
Map *pokedex_by_id = NULL;
float matrizDebilidades[NUM_TIPOS][NUM_TIPOS];

void mostrarMenu() {
    printf("\n========================================\n");
    printf("        POKEHASH: GESTOR TÁCTICO        \n");
    printf("========================================\n");
    printf("1. Explorar Pokédex\n");
    printf("2. Gestión Estratégica de Equipo\n");
    printf("3. Exportar Equipo\n");
    printf("4. Salir\n");
    printf("========================================\n");
    printf("Seleccione una opción: ");
}

void inicializarEquipo(Equipo* e) {
    e->tope = 0;
    for(int i = 0; i < 6; i++) {
        e->integrantes[i] = NULL;
    }
}

// Función helper para comparar strings de forma case-insensitive
int string_is_equal(void *key1, void *key2) {
    if (key1 == NULL || key2 == NULL) return 0;
    return strcasecmp((char *)key1, (char *)key2) == 0;
}

void cargar_data(){
    FILE *archivo = fopen("Pokemon.csv", "r");
    if(archivo == NULL){
        perror("Error al abrir el archivo");
        return;
    }

    // Inicializar los mapas de la Pokédex
    pokedex = map_create(string_is_equal);
    pokedex_by_id = map_create(string_is_equal);
    if(pokedex == NULL || pokedex_by_id == NULL){
        fclose(archivo);
        printf("Error al crear los mapas de la Pokédex.\n");
        return;
    }

    char **campos;
    // Ignorar la línea de cabecera
    campos = leer_linea_csv(archivo, ',');

    while((campos = leer_linea_csv(archivo, ',')) != NULL){
        Pokemon *pmon = (Pokemon *)malloc(sizeof(Pokemon));
        if (pmon == NULL) {
            printf("Error: No se pudo asignar memoria para un Pokémon.\n");
            break;
        }

        pmon->id = atoi(campos[0]);

        // Procesar Nombre y Forma para tener nombres únicos y descriptivos
        char *name = campos[1];
        char *form = campos[2];
        
        // Omitir espacios en blanco al inicio del campo Form
        while (*form == ' ') form++;
        
        // Quitar espacios en blanco al final del campo Form
        char temp_form[100];
        strncpy(temp_form, form, sizeof(temp_form) - 1);
        temp_form[sizeof(temp_form) - 1] = '\0';
        int len = strlen(temp_form);
        while (len > 0 && temp_form[len - 1] == ' ') {
            temp_form[len - 1] = '\0';
            len--;
        }

        if (strlen(temp_form) > 0) {
            if (strstr(temp_form, name) != NULL) {
                // Si la forma ya contiene el nombre base (ej: "Mega Venusaur")
                strncpy(pmon->nombre, temp_form, sizeof(pmon->nombre) - 1);
            } else {
                // Si no, los combinamos de forma bonita (ej: "Meowstic (Male)")
                snprintf(pmon->nombre, sizeof(pmon->nombre), "%.45s (%.45s)", name, temp_form);
            }
        } else {
            strncpy(pmon->nombre, name, sizeof(pmon->nombre) - 1);
        }
        pmon->nombre[sizeof(pmon->nombre) - 1] = '\0';

        // Copiar tipos
        strncpy(pmon->tipo1, campos[3], sizeof(pmon->tipo1) - 1);
        pmon->tipo1[sizeof(pmon->tipo1) - 1] = '\0';

        strncpy(pmon->tipo2, campos[4], sizeof(pmon->tipo2) - 1);
        pmon->tipo2[sizeof(pmon->tipo2) - 1] = '\0';

        // Asignar estadísticas numéricas
        pmon->total_stats = atoi(campos[5]);
        pmon->hp = atoi(campos[6]);
        pmon->ataque = atoi(campos[7]);
        pmon->defensa = atoi(campos[8]);
        pmon->ataque_esp = atoi(campos[9]);
        pmon->defensa_esp = atoi(campos[10]);
        pmon->velocidad = atoi(campos[11]);
        pmon->gen = atoi(campos[12]);

        // Insertar en el mapa de nombres
        map_insert(pokedex, pmon->nombre, pmon);

        // Crear una clave de texto dinámica para el ID e insertar en el mapa por ID
        char *id_key = (char *)malloc(20 * sizeof(char));
        if (id_key != NULL) {
            sprintf(id_key, "%d", pmon->id);
            map_insert(pokedex_by_id, id_key, pmon);
        }
    }
    fclose(archivo);
}

static void mostrar_detalles_pokemon(Pokemon *p) {
    if (p == NULL) return;

    // Normalizar la visualización de tipo2 si está vacío
    char t2_display[30];
    char *t2 = p->tipo2;
    while (*t2 == ' ') t2++;
    if (strlen(t2) == 0) {
        strcpy(t2_display, "Ninguno");
    } else {
        strcpy(t2_display, t2);
    }

    printf("\n========================================\n");
    printf("        DETALLES DEL POKÉMON            \n");
    printf("========================================\n");
    printf(" Nombre:      %-20s (ID: %d)\n", p->nombre, p->id);
    printf(" Tipo 1:      %-20s Tipo 2: %s\n", p->tipo1, t2_display);
    printf("----------------------------------------\n");
    printf(" Estadísticas Base:\n");
    printf("   Puntos de Vida (PS): %-4d | Velocidad:  %d\n", p->hp, p->velocidad);
    printf("   Ataque:              %-4d | Defensa:    %d\n", p->ataque, p->defensa);
    printf("   Ataque Especial:     %-4d | Def. Esp:   %d\n", p->ataque_esp, p->defensa_esp);
    printf("   Total Estadísticas:  %d\n", p->total_stats);
    printf("----------------------------------------\n");
    printf(" Generación:  %d\n", p->gen);
    printf("========================================\n");
}

static void buscar_por_nombre() {
    if (pokedex == NULL) return;

    char nombre_buscado[100];
    printf("\nIngrese el nombre del Pokémon a buscar: ");

    // Limpiar buffer de entrada si queda algún residuo
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF);

    if (fgets(nombre_buscado, sizeof(nombre_buscado), stdin) != NULL) {
        // Quitar el salto de línea al final
        nombre_buscado[strcspn(nombre_buscado, "\r\n")] = '\0';

        // Eliminar espacios al inicio y final del nombre buscado
        char *trimmed = nombre_buscado;
        while (*trimmed == ' ') trimmed++;
        int len = strlen(trimmed);
        while (len > 0 && trimmed[len - 1] == ' ') {
            trimmed[len - 1] = '\0';
            len--;
        }

        if (strlen(trimmed) == 0) {
            printf("\n[Error] Nombre inválido.\n");
        } else {
            MapPair *pair = map_search(pokedex, trimmed);
            if (pair == NULL) {
                printf("\n[!] Pokémon \"%s\" no encontrado en la Pokédex.\n", trimmed);
            } else {
                Pokemon *p = (Pokemon *)pair->value;
                mostrar_detalles_pokemon(p);
            }
        }
    }
    ungetc('\n', stdin);
    presioneTeclaParaContinuar();
}

static void buscar_por_id() {
    if (pokedex_by_id == NULL) return;

    int id_buscado;
    printf("\nIngrese el número de Pokédex a buscar: ");
    if (scanf("%d", &id_buscado) != 1) {
        printf("\n[Error] Entrada no válida.\n");
        int c;
        while ((c = getchar()) != '\n' && c != EOF);
    } else {
        // Limpiar buffer
        int c;
        while ((c = getchar()) != '\n' && c != EOF);

        // Convertir ID a string para buscar en el mapa pokedex_by_id
        char id_str[20];
        sprintf(id_str, "%d", id_buscado);

        MapPair *pair = map_search(pokedex_by_id, id_str);
        if (pair == NULL) {
            printf("\n[!] Pokémon con número %d no encontrado en la Pokédex.\n", id_buscado);
        } else {
            Pokemon *p_encontrado = (Pokemon *)pair->value;
            mostrar_detalles_pokemon(p_encontrado);
        }
    }
    ungetc('\n', stdin);
    presioneTeclaParaContinuar();
}

static void buscar_por_filtro_gen_tipo() {
    if (pokedex == NULL) return;

    int gen_buscada;
    char tipo_buscado[50];

    printf("\nIngrese la generación (1-9): ");
    if (scanf("%d", &gen_buscada) != 1) {
        printf("\n[Error] Entrada no válida.\n");
        int c;
        while ((c = getchar()) != '\n' && c != EOF);
    } else {
        printf("Ingrese el tipo de Pokémon: ");
        // Limpiar buffer antes de leer string
        int ch;
        while ((ch = getchar()) != '\n' && ch != EOF);

        if (fgets(tipo_buscado, sizeof(tipo_buscado), stdin) != NULL) {
            tipo_buscado[strcspn(tipo_buscado, "\r\n")] = '\0';

            // Eliminar espacios al inicio y final
            char *trimmed_type = tipo_buscado;
            while (*trimmed_type == ' ') trimmed_type++;
            int len = strlen(trimmed_type);
            while (len > 0 && trimmed_type[len - 1] == ' ') {
                trimmed_type[len - 1] = '\0';
                len--;
            }

            if (strlen(trimmed_type) == 0) {
                printf("\n[Error] Tipo inválido.\n");
            } else {
                printf("\n============================================================\n");
                printf(" POKÉMON ENCONTRADOS (Gen: %d | Tipo: %s)\n", gen_buscada, trimmed_type);
                printf("============================================================\n");
                printf(" %-5s | %-25s | %-12s | %-12s | %-5s\n", "ID", "Nombre", "Tipo 1", "Tipo 2", "BST");
                printf("------------------------------------------------------------\n");

                int encontrados = 0;
                MapPair *pair = map_first(pokedex);
                while (pair != NULL) {
                    Pokemon *p = (Pokemon *)pair->value;
                    if (p->gen == gen_buscada) {
                        if (strcasecmp(p->tipo1, trimmed_type) == 0 || strcasecmp(p->tipo2, trimmed_type) == 0) {
                            // Normalizar la visualización de tipo2
                            char t2_display[20];
                            char *t2 = p->tipo2;
                            while (*t2 == ' ') t2++;
                            if (strlen(t2) == 0) {
                                strcpy(t2_display, "Ninguno");
                            } else {
                                strcpy(t2_display, t2);
                            }

                            printf(" %-5d | %-25s | %-12s | %-12s | %-5d\n",
                                   p->id, p->nombre, p->tipo1, t2_display, p->total_stats);
                            encontrados++;
                        }
                    }
                    pair = map_next(pokedex);
                }

                printf("============================================================\n");
                printf(" Total: %d Pokémon encontrados.\n", encontrados);
            }
        }
    }
    ungetc('\n', stdin);
    presioneTeclaParaContinuar();
}

void menu_explorar_pokedex() {
    if (pokedex == NULL) {
        printf("\n[!] La Pokédex no ha sido cargada aún.\n");
        return;
    }

    int opcion_sub = 0;
    while (opcion_sub != 4) {
        limpiarPantalla();
        printf("\n========================================\n");
        printf("            EXPLORAR POKÉDEX            \n");
        printf("========================================\n");
        printf("1. Buscar por Nombre\n");
        printf("2. Buscar por Número de Pokédex\n");
        printf("3. Buscar con Filtro (Gen y Tipo)\n");
        printf("4. Volver al menú principal\n");
        printf("========================================\n");
        printf("Seleccione una opción: ");

        if (scanf("%d", &opcion_sub) != 1) {
            printf("\n[Error] Opción no válida. Intente nuevamente.\n");
            int c;
            while ((c = getchar()) != '\n' && c != EOF);
            opcion_sub = 0;
            continue;
        }

        switch (opcion_sub) {
            case 1:
                buscar_por_nombre();
                break;
            case 2:
                buscar_por_id();
                break;
            case 3:
                buscar_por_filtro_gen_tipo();
                break;
            case 4:
                // Salir del submenú
                break;
            default:
                printf("\n[Error] Opción no válida. Intente nuevamente.\n");
        }
    }
}

void liberar_pokedex() {
    // 1. Liberar memoria de los Pokémon
    if (pokedex != NULL) {
        MapPair *pair = map_first(pokedex);
        while (pair != NULL) {
            Pokemon *pmon = (Pokemon *)pair->value;
            free(pmon);
            pair = map_next(pokedex);
        }
        map_destroy(pokedex);
        pokedex = NULL;
    }

    // 2. Liberar las claves dinámicas creadas para el mapa de ID y destruirlo
    if (pokedex_by_id != NULL) {
        MapPair *pair = map_first(pokedex_by_id);
        while (pair != NULL) {
            char *id_key = (char *)pair->key;
            free(id_key);
            pair = map_next(pokedex_by_id);
        }
        map_destroy(pokedex_by_id);
        pokedex_by_id = NULL;
    }
}


/*
void analizar_debilidades(Equipo *e) {
    if (e == NULL) return;
    if (e->tope == 0) {
        printf("\n[!] El equipo está vacío. No hay Pokémon para analizar.\n");
        return;
    }

    for (int i = 0 ; i < e->tope ; i++) {
        Pokemon *p = e->integrantes[i];
        printf("\nDebilidades de %s:\n", p->nombre);
        printf("Tipo 1: %s | Tipo 2: %s\n", p->tipo1, strlen(p->tipo2) > 0 ? p->tipo2 : "Ninguno");

        
        
        //El algoritmo itera sobre los ‘k’ Pokémon actualmente en
        //la Pila. Por cada uno, extrae sus tipos y consulta la Matriz de Adyacencia
        //iterando sobre los ‘t’ tipos posibles (18), acumulando los multiplicadores en un
        //arreglo temporal de vulnerabilidades.
        

    }
}
*/

void cargar_matriz_debilidades(){
    FILE *archivo = fopen("Tabla.csv", "r");
    if(archivo == NULL){
        perror("Error al abrir el archivo");
        return;
    }

    char linea[200];
    // Ignora la línea de cabecera
    if (fgets(linea, sizeof(linea), archivo) == NULL) {
        fclose(archivo);
        return;
    }

    int fil = 0;
    while (fgets(linea, sizeof(linea), archivo) && fil < NUM_TIPOS) {
        char *token = strtok(linea, ","); // guarda la palabra (el tipo)
        int col = 0;
        token = strtok(NULL, ",");
        while (token != NULL && col < NUM_TIPOS) {
            matrizDebilidades[fil][col] = atof(token);
            token = strtok(NULL, ",");
            col++;
        }
        fil++;
    }
    fclose(archivo);
}

void agregar_pokemon_equipo(Equipo *e) {
    if (pokedex == NULL) {
        printf("\n[!] La Pokédex no ha sido cargada aún.\n");
        return;
    }

    if (e->tope >= 6) {
        printf("\n[Error] El equipo está completo (máximo 6 Pokémon).\n");
        presioneTeclaParaContinuar();
        return;
    }

    char nombre_buscado[100];
    printf("\nIngrese el nombre del Pokémon a agregar al equipo: ");

    // Limpiar buffer de entrada si queda algún residuo
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF);

    if (fgets(nombre_buscado, sizeof(nombre_buscado), stdin) != NULL) {
        // Quitar el salto de línea al final
        nombre_buscado[strcspn(nombre_buscado, "\r\n")] = '\0';

        // Eliminar espacios al inicio y final del nombre buscado
        char *trimmed = nombre_buscado;
        while (*trimmed == ' ') trimmed++;
        int len = strlen(trimmed);
        while (len > 0 && trimmed[len - 1] == ' ') {
            trimmed[len - 1] = '\0';
            len--;
        }

        if (strlen(trimmed) == 0) {
            printf("\n[Error] Nombre inválido.\n");
        } else {
            MapPair *pair = map_search(pokedex, trimmed);
            if (pair == NULL) {
                printf("\n[!] Pokémon \"%s\" no encontrado en la Pokédex.\n", trimmed);
            } else {
                Pokemon *p = (Pokemon *)pair->value;
                e->integrantes[e->tope] = p;
                e->tope++;
                printf("\n[!] ¡%s ha sido añadido exitosamente al equipo! (Espacios ocupados: %d/6)\n", p->nombre, e->tope);
            }
        }
    }
    ungetc('\n', stdin);
    presioneTeclaParaContinuar();
}

void ver_equipo_actual(Equipo *e) {
    if (e->tope == 0) {
        printf("\n[!] El equipo está vacío. Agregue Pokémon primero.\n");
        presioneTeclaParaContinuar();
        return;
    }

    printf("\n================================================================================\n");
    printf("                            INTEGRANTES DEL EQUIPO                              \n");
    printf("================================================================================\n");
    for (int i = 0; i < e->tope; i++) {
        Pokemon *p = e->integrantes[i];
        
        // Normalizar la visualización de tipo2 si está vacío
        char t2_display[30];
        char *t2 = p->tipo2;
        while (*t2 == ' ') t2++;
        if (strlen(t2) == 0) {
            strcpy(t2_display, "Ninguno");
        } else {
            strcpy(t2_display, t2);
        }

        printf(" [%d] %-20s (ID: %-3d) | Tipo 1: %-8s | Tipo 2: %-8s\n", i + 1, p->nombre, p->id, p->tipo1, t2_display);
        printf("     HP: %-3d | ATK: %-3d | DEF: %-3d | SPA: %-3d | SPD: %-3d | SPE: %-3d | Total: %d\n", 
               p->hp, p->ataque, p->defensa, p->ataque_esp, p->defensa_esp, p->velocidad, p->total_stats);
        printf("--------------------------------------------------------------------------------\n");
    }
    printf(" Espacios ocupados: %d/6\n", e->tope);
    printf("================================================================================\n");
    presioneTeclaParaContinuar();
}

void menu_gestion_equipo(Equipo *e) {
    int opcion_sub = 0;
    while (opcion_sub != 3) {
        limpiarPantalla();
        printf("\n========================================\n");
        printf("       GESTIÓN ESTRATÉGICA DE EQUIPO    \n");
        printf("========================================\n");
        printf("1. Agregar Pokémon al Equipo\n");
        printf("2. Ver Equipo Actual\n");
        printf("3. Volver al menú principal\n");
        printf("========================================\n");
        printf("Seleccione una opción: ");

        if (scanf("%d", &opcion_sub) != 1) {
            printf("\n[Error] Opción no válida. Intente nuevamente.\n");
            int c;
            while ((c = getchar()) != '\n' && c != EOF);
            opcion_sub = 0;
            continue;
        }

        switch (opcion_sub) {
            case 1:
                agregar_pokemon_equipo(e);
                break;
            case 2:
                ver_equipo_actual(e);
                break;
            case 3:
                // Volver
                break;
            default:
                printf("\n[Error] Opción no válida. Intente nuevamente.\n");
                presioneTeclaParaContinuar();
        }
    }
}