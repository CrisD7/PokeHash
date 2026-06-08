#include "pokehash.h"
#include "tdas/extra.h"
#include <strings.h>
#include <ctype.h>

Map *pokedex = NULL;

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

    // Inicializar el mapa de la Pokédex
    pokedex = map_create(string_is_equal);
    if(pokedex == NULL){
        fclose(archivo);
        printf("Error al crear el mapa de la Pokédex.\n");
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

        // Insertar en el mapa de la Pokédex usando el nombre como clave única
        map_insert(pokedex, pmon->nombre, pmon);
    }
    fclose(archivo);
}

void explorar_pokedex() {
    if (pokedex == NULL) {
        printf("\n[!] La Pokédex no ha sido cargada aún.\n");
        return;
    }

    char nombre_buscado[100];
    printf("\nIngrese el nombre del Pokémon a buscar: ");
    
    // Limpiar buffer de entrada si queda algún residuo
    fflush(stdin);
    
    // Leer línea con soporte para espacios en blanco
    // Usamos getchar() si hay un salto de línea acumulado en el buffer
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF);
    
    if (fgets(nombre_buscado, sizeof(nombre_buscado), stdin) == NULL) return;
    
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
        return;
    }

    MapPair *pair = map_search(pokedex, trimmed);
    if (pair == NULL) {
        printf("\n[!] Pokémon \"%s\" no encontrado en la Pokédex.\n", trimmed);
        return;
    }

    Pokemon *p = (Pokemon *)pair->value;

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

void liberar_pokedex() {
    if (pokedex == NULL) return;

    // Iterar y liberar la memoria dinámica asignada a cada Pokémon
    MapPair *pair = map_first(pokedex);
    while (pair != NULL) {
        Pokemon *pmon = (Pokemon *)pair->value;
        free(pmon);
        pair = map_next(pokedex);
    }

    // Destruir el TDA Mapa y sus listas internas
    map_destroy(pokedex);
    pokedex = NULL;
}