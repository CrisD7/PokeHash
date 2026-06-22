#include "pokehash.h"
#include "tdas/extra.h"
#include <strings.h>
#include <ctype.h>

const char *NOMBRES_TIPOS[NUM_TIPOS] = {
        "Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison",
        "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon",
        "Dark", "Steel", "Fairy"
    };

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

    // Cargar la matriz de efectividades de tipos desde Tabla.csv
    cargar_matriz_debilidades();
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
    while (opcion_sub != 5) {
        limpiarPantalla();
        printf("\n========================================\n");
        printf("            EXPLORAR POKÉDEX            \n");
        printf("========================================\n");
        printf("1. Buscar por Nombre\n");
        printf("2. Buscar por Número de Pokédex\n");
        printf("3. Buscar con Filtro (Gen y Tipo)\n");
        printf("4. Mejores 10 por Estadística\n");
        printf("5. Volver al menú principal\n");
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
                mejores10PorStat();
                break;
            case 5:
                // Salir del submenú
                break;
            default:
                printf("\n[Error] Opción no válida. Intente nuevamente.\n");
        }
    }
}

// Obtiene el valor de la stat elegida
static int obtenerStat(Pokemon *p, int opcionStat)
{
    switch(opcionStat)
    {
        case 1: return p->hp;
        case 2: return p->ataque;
        case 3: return p->defensa;
        case 4: return p->ataque_esp;
        case 5: return p->defensa_esp;
        case 6: return p->velocidad;
        default: return 0;
    }
}

// Retorna el nombre de la stat
static const char* obtenerNombreStat(int opcionStat)
{
    switch(opcionStat)
    {
        case 1: return "HP";
        case 2: return "Ataque";
        case 3: return "Defensa";
        case 4: return "Ataque Especial";
        case 5: return "Defensa Especial";
        case 6: return "Velocidad";
        default: return "Stat inexistente.";
    }
}

void mejores10PorStat(){
    if (pokedex == NULL){
    printf("\n[!] La Pokédex no ha sido cargada aún.\n");
    presioneTeclaParaContinuar();
    return;
    }

    int opcion_menu = 0;
    while (opcion_menu != 3){
        limpiarPantalla();
        printf("\n========================================\n");
        printf("              MEJORES 10 POR STAT         \n");
        printf("========================================\n");
        printf("1. Top 10 por UNA unica stat\n");
        printf("2. Top 10 por DOS stats\n");
        printf("3. Volver al menú anterior\n");
        printf("========================================\n");
        printf("Seleccione una opción : ");

        if (scanf("%d", &opcion_menu) != 1){
            printf("\n[ERROR] Selección invalida.\n");
            int c;
            while ((c = getchar()) != '\n' && c != EOF);
            opcion_menu = 0;
            presioneTeclaParaContinuar();
            continue;
        }

        if (opcion_menu == 3) break;

        if (opcion_menu == 1 || opcion_menu == 2){
            int opcionFiltro = 0;
            int genFiltro = 0;
            char tipoFiltro[50] = "";

            printf("\n========================================\n");
            printf(" ¿Desea aplicar un filtro a la busqueda? \n");
            printf("========================================\n");
            printf("1. No. (Toda la Pokédex)\n");
            printf("2. Filtrado por GENERACIÓN\n");
            printf("3. Filtrado por TIPO\n");
            printf("========================================\n");
            printf("Seleccione una opción : ");
            scanf("%d", &opcionFiltro);

            if (opcionFiltro == 2){
                printf("Ingrese la generación a filtrar (1-9) : ");
                scanf("%d", &genFiltro);
            }
            else if (opcionFiltro == 3){
                printf("Ingrese el tipo a filtrar : ");
                int ch;
                while ((ch = getchar()) != '\n' && ch != EOF);
                if (fgets(tipoFiltro, sizeof(tipoFiltro), stdin) != NULL){
                    tipoFiltro[strcspn(tipoFiltro, "\r\n")] = '\0';
                    char *t = tipoFiltro;
                    while (*t == ' ') t++;
                    int len = strlen(t);
                    while (len > 0 && t[len - 1] == ' ') { t[len - 1] = '\0'; len--; }
                    strcpy(tipoFiltro, t);
                }
            }
            else if (opcionFiltro != 1){
                printf("\n[ERROR] Selección invalida.\n");
                presioneTeclaParaContinuar();
                continue;
            }
            limpiarPantalla();
            printf("\n==================================================================================\n");
            printf("Stats disponibles : \n");
            printf("1. HP | 2. Ataque | 3. Defensa | 4. Ataque Esp. | 5. Defensa Esp. | 6. Velocidad\n");
            printf("==================================================================================\n");

            int stat1 = 0, stat2 = 0;
            printf("Seleccione la %sstat (1-6) : ", opcion_menu == 2 ? "primera" : "");
            scanf("%d", &stat1);

            if (opcion_menu == 2){
                printf("Seleccione la segunda stat (1-6) : ");
                scanf("%d", &stat2);
            }

            if (stat1 < 1 || stat1 > 6 || (opcion_menu == 2 && (stat2 < 1 || stat2 > 6))){
                printf("\n[ERROR] Selección de stat invalida.\n");
                int c;
                while ((c = getchar()) != '\n' && c != EOF);
                presioneTeclaParaContinuar();
                continue;
            }

            Pokemon* top10_pokemons[10];
            int top10Puntaje[10];
            for (int i = 0 ; i < 10 ; i++){
                top10_pokemons[i] = NULL;
                top10Puntaje[i] = -1;
            }

            MapPair *pair = map_first(pokedex);
            int evaluados = 0;

            while (pair != NULL){
                Pokemon *p = (Pokemon *) pair->value;

                if (opcionFiltro == 2 && p->gen != genFiltro){
                    pair = map_next(pokedex);
                    continue;
                }

                if (opcionFiltro == 3){
                    if (strcasecmp(p->tipo1, tipoFiltro) != 0 && strcasecmp(p->tipo2, tipoFiltro) != 0){
                        pair = map_next(pokedex);
                        continue;
                    }
                }

                evaluados++;

                int puntaje = obtenerStat(p, stat1);
                if (opcion_menu == 2){
                    puntaje += obtenerStat(p, stat2);
                }

                if (puntaje > top10Puntaje[9]){
                    int pos = 9;
                    while (pos > 0 && puntaje > top10Puntaje[pos-1]){
                        pos--;
                    }
                    for (int i = 9 ; i > pos ; i--){
                        top10Puntaje[i] = top10Puntaje[i-1];
                        top10_pokemons[i] = top10_pokemons[i-1];
                    }
                    top10Puntaje[pos] = puntaje;
                    top10_pokemons[pos] = p;
                }
                pair = map_next(pokedex);
            }
            limpiarPantalla();
            printf("\n=================================================================\n");
            printf(" TOP 10 POKÉMON POR : %s", obtenerNombreStat(stat1));
            if (opcion_menu == 2) printf(" + %s", obtenerNombreStat(stat2));

            if (opcionFiltro == 2) printf(" (Filtro: Gen %d)\n", genFiltro);
            else if (opcionFiltro == 3) printf(" (Filtro: Tipo %s)\n", tipoFiltro);
            else printf(" (Global)\n");
            printf("=================================================================\n");

            if (evaluados == 0){
                printf(" [!] No se encontraron Pokémon que cumplan con el filtro.\n");
                printf("=================================================================\n");
            }
            else{
                printf(" %-4s | %-30s | %-10s\n", "Pos", "Nombre (ID)", "Puntaje");
                printf("=================================================================\n");

                for (int i = 0 ; i < 10 ; i++){
                    if (top10_pokemons[i] != NULL)
                    {
                        char nombreConId[120];
                        snprintf(nombreConId, sizeof(nombreConId), "%s (%d)", top10_pokemons[i]->nombre, top10_pokemons[i]->id);
                        printf(" %-4d | %-30s | %-10d\n", i + 1, nombreConId, top10Puntaje[i]);
                    }
                }
                printf("=================================================================\n");
            }
            
            int c;
            while ((c = getchar()) != '\n' && c != EOF);
            presioneTeclaParaContinuar();
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

const char* obtener_nombre_tipo (int indice) {
    if (indice < 0 || indice >= NUM_TIPOS) return NULL;
    return NOMBRES_TIPOS[indice];
}

int obtener_indice_tipo(const char *tipo) {
    if (tipo == NULL) return -1;
    for (int i = 0; i < NUM_TIPOS; i++) {
        if (strcasecmp(tipo, NOMBRES_TIPOS[i]) == 0) {
            return i;
        }
    }
    return -1; // Tipo no encontrado
}

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

void analizar_debilidades(Equipo *e) {
    if (e == NULL) return;
    if (e->tope == 0) {
        printf("\n[!] El equipo está vacío. No hay Pokémon para analizar.\n");
        presioneTeclaParaContinuar();
        return;
    }

    // Nombres de tipos en español y mayúsculas para la salida
    static const char *TIPOS_ES[NUM_TIPOS] = {
        "NORMAL", "FUEGO", "AGUA", "ELÉCTRICO", "PLANTA", "HIELO",
        "LUCHA", "VENENO", "TIERRA", "VOLADOR", "PSÍQUICO", "BICHO",
        "ROCA", "FANTASMA", "DRAGÓN", "SINIESTRO", "ACERO", "HADA"
    };

    // Arreglos de análisis por Pokémon
    int conteo_debilidades[NUM_TIPOS] = {0};
    int es_x4[6][NUM_TIPOS];    // 1 si el Pokémon i tiene debilidad x4 al tipo j
    int es_inmune[6][NUM_TIPOS]; // 1 si el Pokémon i es inmune al tipo j
    memset(es_x4, 0, sizeof(es_x4));
    memset(es_inmune, 0, sizeof(es_inmune));

    // === PRIMERA PASADA: recopilar datos ===
    for (int i = 0; i < e->tope; i++) {
        Pokemon *p = e->integrantes[i];

        char *t2 = p->tipo2;
        while (*t2 == ' ') t2++;
        int tiene_tipo2 = (strlen(t2) > 0);

        int tipo1_idx = obtener_indice_tipo(p->tipo1);
        int tipo2_idx = tiene_tipo2 ? obtener_indice_tipo(t2) : -1;

        for (int j = 0; j < NUM_TIPOS; j++) {
            float mult = 1.0f;
            if (tipo1_idx != -1) mult *= matrizDebilidades[j][tipo1_idx];
            if (tipo2_idx != -1) mult *= matrizDebilidades[j][tipo2_idx];

            if (mult > 1.0f) {
                conteo_debilidades[j]++;
                if (mult > 2.0f) es_x4[i][j] = 1;
            }
            if (mult == 0.0f) es_inmune[i][j] = 1;
        }
    }

    // === SEGUNDA PASADA: imprimir resultados ===
    printf("\n==================================================\n");
    printf("        ANÁLISIS TÁCTICO DEL EQUIPO\n");
    printf("==================================================\n");

    // --- Sección 1: Resumen de Vulnerabilidades ---
    printf("\n[-] RESUMEN DE VULNERABILIDADES:\n");
    int hay_alerta = 0;
    for (int j = 0; j < NUM_TIPOS; j++) {
        if (conteo_debilidades[j] >= 3) {
            printf("    * [ALERTA] %d integrantes son débiles al tipo %s.\n",
                   conteo_debilidades[j], TIPOS_ES[j]);
            hay_alerta = 1;
        }
    }
    if (!hay_alerta) {
        printf("    * El equipo está balanceado. Ningún tipo amenaza a más de 2 integrantes.\n");
    }

    // --- Sección 2: Debilidades Extremas (x4) ---
    printf("\n[-] DEBILIDADES EXTREMAS (Cuidado con los x4):\n");
    int hay_x4 = 0;
    for (int i = 0; i < e->tope; i++) {
        for (int j = 0; j < NUM_TIPOS; j++) {
            if (es_x4[i][j]) {
                printf("    * %s (Débil x4 a %s)\n",
                       e->integrantes[i]->nombre, TIPOS_ES[j]);
                hay_x4 = 1;
            }
        }
    }
    if (!hay_x4) {
        printf("    * Ningún integrante tiene debilidades x4. ¡Excelente!\n");
    }

    // --- Sección 3: Inmunidades del Equipo ---
    printf("\n[-] INMUNIDADES DEL EQUIPO (Cambios seguros):\n");
    int hay_inmunidad = 0;
    for (int i = 0; i < e->tope; i++) {
        // Recopilar índices de inmunidades de este Pokémon
        int indices[NUM_TIPOS];
        int num_inmune = 0;
        for (int j = 0; j < NUM_TIPOS; j++) {
            if (es_inmune[i][j]) indices[num_inmune++] = j;
        }

        if (num_inmune > 0) {
            hay_inmunidad = 1;
            printf("    * %s es INMUNE a ", e->integrantes[i]->nombre);
            for (int k = 0; k < num_inmune; k++) {
                if (k > 0 && k == num_inmune - 1)
                    printf(" y %s", TIPOS_ES[indices[k]]);
                else if (k > 0)
                    printf(", %s", TIPOS_ES[indices[k]]);
                else
                    printf("%s", TIPOS_ES[indices[k]]);
            }
            printf(".\n");
        }
    }
    if (!hay_inmunidad) {
        printf("    * Ningún integrante tiene inmunidades.\n");
    }

    printf("==================================================\n");
    presioneTeclaParaContinuar();
}

void agregar_pokemon_equipo(Equipo *e) {
    limpiarPantalla();
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
        limpiarPantalla();
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
    while (opcion_sub != 5) {
        limpiarPantalla();
        printf("\n========================================\n");
        printf("       GESTIÓN ESTRATÉGICA DE EQUIPO    \n");
        printf("========================================\n");
        printf("1. Agregar Pokémon al Equipo\n");
        printf("2. Ver Equipo Actual\n");
        printf("3. Deshacer última adición\n");
        printf("4. Analizar Debilidades del Equipo\n");
        printf("5. Volver al menú principal\n");
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
                // Deshacer última adición: operación LIFO O(1)
                if (e->tope > 0) {
                    e->tope--;
                    printf("\n[!] Última acción revertida. ");
                    printf("El equipo vuelve a tener %d integrante(s).\n", e->tope);
                } else {
                    printf("\n[!] El equipo ya está vacío. No hay nada que deshacer.\n");
                }
                presioneTeclaParaContinuar();
                break;
            case 4:
                limpiarPantalla();
                analizar_debilidades(e);
                break;
            case 5:
                // Volver
                break;
            default:
                printf("\n[Error] Opción no válida. Intente nuevamente.\n");
                presioneTeclaParaContinuar();
        }
    }
}