// pokehash_api.c — Backend JSON API para la GUI (stdin/stdout)
// Toda la lógica reside en pokehash.c; este archivo solo parsea
// comandos JSON, invoca las funciones de C, y responde con JSON.

#include "pokehash.h"
#include "tdas/extra.h"
#include <strings.h>
#include <ctype.h>

// Variable global del equipo activo (gestionada exclusivamente aquí)
static Equipo miEquipo;

// ============================================================
// Helpers para parsear JSON manualmente (sin dependencias externas)
// ============================================================

// Extrae el valor string de un campo JSON: "key":"value"
// Retorna puntero a buffer estático (se sobreescribe en cada llamada)
static char* json_get_str(const char *json, const char *key) {
    static char buf[512];
    char pattern[128];
    snprintf(pattern, sizeof(pattern), "\"%s\":\"", key);
    const char *start = strstr(json, pattern);
    if (!start) return NULL;
    start += strlen(pattern);
    const char *end = strchr(start, '"');
    if (!end) return NULL;
    int len = (int)(end - start);
    if (len >= (int)sizeof(buf)) len = (int)sizeof(buf) - 1;
    strncpy(buf, start, len);
    buf[len] = '\0';
    return buf;
}

// Extrae el valor entero de un campo JSON: "key":123
static int json_get_int(const char *json, const char *key, int default_val) {
    char pattern[128];
    snprintf(pattern, sizeof(pattern), "\"%s\":", key);
    const char *start = strstr(json, pattern);
    if (!start) return default_val;
    start += strlen(pattern);
    while (*start == ' ' || *start == '\t') start++;
    if (*start == '"') return default_val; // Es string, no int
    return atoi(start);
}

// ============================================================
// Helpers para generar JSON de salida
// ============================================================

// Imprime un string JSON-safe (escapa " y \)
static void print_json_str(const char *s) {
    putchar('"');
    for (; *s; s++) {
        if (*s == '"') printf("\\\"");
        else if (*s == '\\') printf("\\\\");
        else putchar(*s);
    }
    putchar('"');
}

// Imprime un Pokemon como objeto JSON (sin newline)
static void print_pokemon_json(const Pokemon *p) {
    // Normalizar tipo2 (quitar espacios)
    const char *t2 = p->tipo2;
    while (*t2 == ' ') t2++;
    if (strlen(t2) == 0) t2 = "";

    printf("{\"id\":%d,\"nombre\":", p->id);
    print_json_str(p->nombre);
    printf(",\"tipo1\":");
    print_json_str(p->tipo1);
    printf(",\"tipo2\":");
    print_json_str(t2);
    printf(",\"total\":%d,\"hp\":%d,\"ataque\":%d,\"defensa\":%d,"
           "\"ataque_esp\":%d,\"defensa_esp\":%d,\"velocidad\":%d,\"gen\":%d}",
           p->total_stats, p->hp, p->ataque, p->defensa,
           p->ataque_esp, p->defensa_esp, p->velocidad, p->gen);
}

// Helper para obtener stat por índice (duplicado de pokehash.c static)
static int api_get_stat(Pokemon *p, int stat) {
    switch (stat) {
        case 1: return p->hp;
        case 2: return p->ataque;
        case 3: return p->defensa;
        case 4: return p->ataque_esp;
        case 5: return p->defensa_esp;
        case 6: return p->velocidad;
        default: return 0;
    }
}

// ============================================================
// Handlers de comandos
// ============================================================

// Helper para qsort (ordenar por ID)
static int cmp_pokemon_id(const void *a, const void *b) {
    Pokemon *p1 = *(Pokemon **)a;
    Pokemon *p2 = *(Pokemon **)b;
    return p1->id - p2->id;
}

// {"cmd":"list_all"} → Lista completa de Pokémon
static void cmd_list_all(void) {
    Pokemon *arr[2000];
    int count = 0;
    MapPair *pair = map_first(pokedex);
    while (pair != NULL) {
        if (count < 2000) arr[count++] = (Pokemon *)pair->value;
        pair = map_next(pokedex);
    }
    qsort(arr, count, sizeof(Pokemon *), cmp_pokemon_id);

    printf("{\"status\":\"ok\",\"data\":[");
    for (int i = 0; i < count; i++) {
        if (i > 0) printf(",");
        print_pokemon_json(arr[i]);
    }
    printf("]}\n");
}

// {"cmd":"search_name","name":"Charizard"} → Buscar por nombre
static void cmd_search_name(const char *json) {
    char *name = json_get_str(json, "name");
    if (!name) {
        printf("{\"status\":\"error\",\"message\":\"Missing name\"}\n");
        return;
    }
    char name_copy[256];
    strncpy(name_copy, name, sizeof(name_copy) - 1);
    name_copy[sizeof(name_copy) - 1] = '\0';

    MapPair *pair = map_search(pokedex, name_copy);
    if (!pair) {
        printf("{\"status\":\"error\",\"message\":\"Pokemon not found\"}\n");
    } else {
        printf("{\"status\":\"ok\",\"data\":");
        print_pokemon_json((Pokemon *)pair->value);
        printf("}\n");
    }
}

// {"cmd":"search_id","id":6} → Buscar por número de Pokédex
static void cmd_search_id(const char *json) {
    int id = json_get_int(json, "id", -1);
    if (id < 0) {
        printf("{\"status\":\"error\",\"message\":\"Invalid id\"}\n");
        return;
    }
    char id_str[20];
    sprintf(id_str, "%d", id);
    MapPair *pair = map_search(pokedex_by_id, id_str);
    if (!pair) {
        printf("{\"status\":\"error\",\"message\":\"Pokemon not found\"}\n");
    } else {
        printf("{\"status\":\"ok\",\"data\":");
        print_pokemon_json((Pokemon *)pair->value);
        printf("}\n");
    }
}

// {"cmd":"filter","gen":1,"type":"Fire","query":"char"} → Filtrar por gen y/o tipo y/o nombre/id
static void cmd_filter(const char *json) {
    int gen = json_get_int(json, "gen", 0);
    
    char *type_raw = json_get_str(json, "type");
    char type_copy[50] = "";
    if (type_raw && strlen(type_raw) > 0) {
        strncpy(type_copy, type_raw, sizeof(type_copy) - 1);
        type_copy[sizeof(type_copy) - 1] = '\0';
    }

    char *query_raw = json_get_str(json, "query");
    char query_copy[100] = "";
    if (query_raw && strlen(query_raw) > 0) {
        strncpy(query_copy, query_raw, sizeof(query_copy) - 1);
        query_copy[sizeof(query_copy) - 1] = '\0';
        for(int i = 0; query_copy[i]; i++) {
            query_copy[i] = tolower((unsigned char)query_copy[i]);
        }
    }

    Pokemon *arr[2000];
    int count = 0;

    MapPair *pair = map_first(pokedex);
    while (pair != NULL) {
        Pokemon *p = (Pokemon *)pair->value;
        int matches = 1;

        if (gen > 0 && p->gen != gen) matches = 0;
        
        if (matches && strlen(type_copy) > 0) {
            if (strcasecmp(p->tipo1, type_copy) != 0 &&
                strcasecmp(p->tipo2, type_copy) != 0) {
                matches = 0;
            }
        }
        
        if (matches && strlen(query_copy) > 0) {
            int is_num = 1;
            for(int i = 0; query_copy[i]; i++) {
                if(!isdigit((unsigned char)query_copy[i])) { is_num = 0; break; }
            }
            if (is_num) {
                char id_str[20];
                sprintf(id_str, "%d", p->id);
                if (strstr(id_str, query_copy) == NULL) matches = 0;
            } else {
                char name_lower[256];
                strncpy(name_lower, p->nombre, sizeof(name_lower)-1);
                name_lower[sizeof(name_lower)-1] = '\0';
                for(int i = 0; name_lower[i]; i++){
                    name_lower[i] = tolower((unsigned char)name_lower[i]);
                }
                if (strstr(name_lower, query_copy) == NULL) matches = 0;
            }
        }

        if (matches && count < 2000) {
            arr[count++] = p;
        }
        pair = map_next(pokedex);
    }
    
    qsort(arr, count, sizeof(Pokemon *), cmp_pokemon_id);

    printf("{\"status\":\"ok\",\"data\":[");
    for (int i = 0; i < count; i++) {
        if (i > 0) printf(",");
        print_pokemon_json(arr[i]);
    }
    printf("]}\n");
}

// {"cmd":"top10","stat1":2,"stat2":0,"filter_gen":0,"filter_type":""}
static void cmd_top10(const char *json) {
    int stat1 = json_get_int(json, "stat1", 0);
    int stat2 = json_get_int(json, "stat2", 0);
    int filter_gen = json_get_int(json, "filter_gen", 0);
    char *ft = json_get_str(json, "filter_type");
    char type_copy[50] = "";
    if (ft && strlen(ft) > 0) strncpy(type_copy, ft, sizeof(type_copy) - 1);

    if (stat1 < 1 || stat1 > 6) {
        printf("{\"status\":\"error\",\"message\":\"Invalid stat1\"}\n");
        return;
    }

    Pokemon *top[10];
    int scores[10];
    for (int i = 0; i < 10; i++) { top[i] = NULL; scores[i] = -1; }

    MapPair *pair = map_first(pokedex);
    while (pair != NULL) {
        Pokemon *p = (Pokemon *)pair->value;
        if (filter_gen > 0 && p->gen != filter_gen) { pair = map_next(pokedex); continue; }
        if (strlen(type_copy) > 0) {
            if (strcasecmp(p->tipo1, type_copy) != 0 &&
                strcasecmp(p->tipo2, type_copy) != 0) {
                pair = map_next(pokedex);
                continue;
            }
        }
        int score = api_get_stat(p, stat1);
        if (stat2 >= 1 && stat2 <= 6) score += api_get_stat(p, stat2);

        if (score > scores[9]) {
            int pos = 9;
            while (pos > 0 && score > scores[pos - 1]) pos--;
            for (int i = 9; i > pos; i--) {
                scores[i] = scores[i - 1];
                top[i] = top[i - 1];
            }
            scores[pos] = score;
            top[pos] = p;
        }
        pair = map_next(pokedex);
    }

    printf("{\"status\":\"ok\",\"data\":[");
    for (int i = 0; i < 10 && top[i] != NULL; i++) {
        if (i > 0) printf(",");
        printf("{\"rank\":%d,\"score\":%d,\"pokemon\":", i + 1, scores[i]);
        print_pokemon_json(top[i]);
        printf("}");
    }
    printf("]}\n");
}

// {"cmd":"team_add","name":"Charizard"}
static void cmd_team_add(const char *json) {
    char *name = json_get_str(json, "name");
    if (!name) {
        printf("{\"status\":\"error\",\"message\":\"Missing name\"}\n");
        return;
    }
    char name_copy[256];
    strncpy(name_copy, name, sizeof(name_copy) - 1);
    name_copy[sizeof(name_copy) - 1] = '\0';

    if (miEquipo.tope >= 6) {
        printf("{\"status\":\"error\",\"message\":\"Team full (6/6)\"}\n");
        return;
    }
    MapPair *pair = map_search(pokedex, name_copy);
    if (!pair) {
        printf("{\"status\":\"error\",\"message\":\"Pokemon not found\"}\n");
        return;
    }
    miEquipo.integrantes[miEquipo.tope] = (Pokemon *)pair->value;
    miEquipo.tope++;
    printf("{\"status\":\"ok\",\"team_size\":%d}\n", miEquipo.tope);
}

// {"cmd":"team_undo"}
static void cmd_team_undo(void) {
    if (miEquipo.tope <= 0) {
        printf("{\"status\":\"error\",\"message\":\"Team is empty\"}\n");
        return;
    }
    Pokemon *removed = miEquipo.integrantes[miEquipo.tope - 1];
    miEquipo.tope--;
    miEquipo.integrantes[miEquipo.tope] = NULL;
    printf("{\"status\":\"ok\",\"removed\":");
    print_json_str(removed->nombre);
    printf(",\"team_size\":%d}\n", miEquipo.tope);
}

// {"cmd":"team_remove","index":2}
static void cmd_team_remove(const char *json) {
    int idx = json_get_int(json, "index", -1);
    if (idx < 0 || idx >= miEquipo.tope) {
        printf("{\"status\":\"error\",\"message\":\"Invalid index\"}\n");
        return;
    }
    Pokemon *removed = miEquipo.integrantes[idx];
    for (int i = idx; i < miEquipo.tope - 1; i++) {
        miEquipo.integrantes[i] = miEquipo.integrantes[i + 1];
    }
    miEquipo.tope--;
    miEquipo.integrantes[miEquipo.tope] = NULL;
    printf("{\"status\":\"ok\",\"removed\":");
    print_json_str(removed->nombre);
    printf(",\"team_size\":%d}\n", miEquipo.tope);
}

// {"cmd":"team_view"}
static void cmd_team_view(void) {
    printf("{\"status\":\"ok\",\"team_size\":%d,\"team\":[", miEquipo.tope);
    for (int i = 0; i < miEquipo.tope; i++) {
        if (i > 0) printf(",");
        print_pokemon_json(miEquipo.integrantes[i]);
    }
    printf("]}\n");
}

// {"cmd":"team_analyze"} — Análisis táctico completo
// Retorna: grid (18 tipos × {weak,resist,immune,x4}),
//          x4_alerts, inmunidades
static void cmd_team_analyze(void) {
    extern float matrizDebilidades[NUM_TIPOS][NUM_TIPOS];

    printf("{\"status\":\"ok\",\"team_size\":%d,\"grid\":[", miEquipo.tope);

    // Grid de vulnerabilidades por tipo atacante
    for (int j = 0; j < NUM_TIPOS; j++) {
        int weak = 0, resist = 0, immune = 0, x4 = 0;

        for (int i = 0; i < miEquipo.tope; i++) {
            Pokemon *p = miEquipo.integrantes[i];
            float mult = 1.0f;

            int t1 = obtener_indice_tipo(p->tipo1);
            if (t1 != -1) mult *= matrizDebilidades[j][t1];

            const char *t2s = p->tipo2;
            while (*t2s == ' ') t2s++;
            if (strlen(t2s) > 0) {
                int t2 = obtener_indice_tipo(t2s);
                if (t2 != -1) mult *= matrizDebilidades[j][t2];
            }

            if (mult == 0.0f) immune++;
            else if (mult > 1.0f) { weak++; if (mult > 2.0f) x4++; }
            else if (mult < 1.0f) resist++;
        }

        if (j > 0) printf(",");
        printf("{\"type\":\"%s\",\"weak\":%d,\"resist\":%d,\"immune\":%d,\"x4\":%d}",
               NOMBRES_TIPOS[j], weak, resist, immune, x4);
    }

    // Alertas x4
    printf("],\"x4_alerts\":[");
    int first = 1;
    for (int i = 0; i < miEquipo.tope; i++) {
        Pokemon *p = miEquipo.integrantes[i];
        const char *t2s = p->tipo2;
        while (*t2s == ' ') t2s++;
        int t1_idx = obtener_indice_tipo(p->tipo1);
        int t2_idx = (strlen(t2s) > 0) ? obtener_indice_tipo(t2s) : -1;

        for (int j = 0; j < NUM_TIPOS; j++) {
            float mult = 1.0f;
            if (t1_idx != -1) mult *= matrizDebilidades[j][t1_idx];
            if (t2_idx != -1) mult *= matrizDebilidades[j][t2_idx];
            if (mult > 2.0f) {
                if (!first) printf(",");
                printf("{\"pokemon\":");
                print_json_str(p->nombre);
                printf(",\"type\":\"%s\"}", NOMBRES_TIPOS[j]);
                first = 0;
            }
        }
    }

    // Inmunidades
    printf("],\"immunities\":[");
    first = 1;
    for (int i = 0; i < miEquipo.tope; i++) {
        Pokemon *p = miEquipo.integrantes[i];
        const char *t2s = p->tipo2;
        while (*t2s == ' ') t2s++;
        int t1_idx = obtener_indice_tipo(p->tipo1);
        int t2_idx = (strlen(t2s) > 0) ? obtener_indice_tipo(t2s) : -1;

        int imm_indices[NUM_TIPOS];
        int num_imm = 0;
        for (int j = 0; j < NUM_TIPOS; j++) {
            float mult = 1.0f;
            if (t1_idx != -1) mult *= matrizDebilidades[j][t1_idx];
            if (t2_idx != -1) mult *= matrizDebilidades[j][t2_idx];
            if (mult == 0.0f) imm_indices[num_imm++] = j;
        }

        if (num_imm > 0) {
            if (!first) printf(",");
            printf("{\"pokemon\":");
            print_json_str(p->nombre);
            printf(",\"types\":[");
            for (int k = 0; k < num_imm; k++) {
                if (k > 0) printf(",");
                printf("\"%s\"", NOMBRES_TIPOS[imm_indices[k]]);
            }
            printf("]}");
            first = 0;
        }
    }
    printf("]}\n");
}

// {"cmd":"team_export","path":"/ruta/archivo.txt"}
static void cmd_team_export(const char *json) {
    char *path = json_get_str(json, "path");
    if (!path) {
        printf("{\"status\":\"error\",\"message\":\"Missing path\"}\n");
        return;
    }
    if (exportar_equipo(&miEquipo, path)) {
        printf("{\"status\":\"ok\"}\n");
    } else {
        printf("{\"status\":\"error\",\"message\":\"No se pudo exportar el equipo (¿está vacío?)\"}\n");
    }
}

// ============================================================
// MAIN — Bucle de lectura de comandos JSON
// ============================================================
int main(void) {
    // Cargar datos (Pokédex + matriz de debilidades)
    cargar_data();
    inicializarEquipo(&miEquipo);

    char line[4096];
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\r\n")] = '\0';
        if (strlen(line) == 0) continue;

        // Extraer campo "cmd"
        char *cmd = json_get_str(line, "cmd");
        if (!cmd) {
            printf("{\"status\":\"error\",\"message\":\"Missing cmd\"}\n");
            fflush(stdout);
            continue;
        }
        // Copiar cmd antes de que json_get_str sobreescriba el buffer
        char cmd_copy[64];
        strncpy(cmd_copy, cmd, sizeof(cmd_copy) - 1);
        cmd_copy[sizeof(cmd_copy) - 1] = '\0';

        // Dispatch
        if      (strcmp(cmd_copy, "list_all")     == 0) cmd_list_all();
        else if (strcmp(cmd_copy, "search_name")  == 0) cmd_search_name(line);
        else if (strcmp(cmd_copy, "search_id")    == 0) cmd_search_id(line);
        else if (strcmp(cmd_copy, "filter")        == 0) cmd_filter(line);
        else if (strcmp(cmd_copy, "top10")         == 0) cmd_top10(line);
        else if (strcmp(cmd_copy, "team_add")      == 0) cmd_team_add(line);
        else if (strcmp(cmd_copy, "team_undo")     == 0) cmd_team_undo();
        else if (strcmp(cmd_copy, "team_remove")   == 0) cmd_team_remove(line);
        else if (strcmp(cmd_copy, "team_view")     == 0) cmd_team_view();
        else if (strcmp(cmd_copy, "team_analyze")  == 0) cmd_team_analyze();
        else if (strcmp(cmd_copy, "team_export")   == 0) cmd_team_export(line);
        else if (strcmp(cmd_copy, "quit")          == 0) break;
        else printf("{\"status\":\"error\",\"message\":\"Unknown command\"}\n");

        fflush(stdout);
    }

    liberar_pokedex();
    return 0;
}
