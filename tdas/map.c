#include "map.h"
#include "list.h"
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define BUCKETS_LIMIT 200

struct Map {
    List *buckets[BUCKETS_LIMIT];
    int size;
    int (*is_equal)(void *key1, void *key2);
    int current_bucket;
};

// Función Hash DJB2 sensible a mayúsculas/minúsculas pero normalizada a minúsculas
// para lograr insensibilidad a mayúsculas en la búsqueda.
static unsigned long hash_string(void *key) {
    if (key == NULL) return 0;
    char *str = (char *)key;
    unsigned long hash = 5381;
    int c;
    while ((c = (unsigned char)*str++)) {
        hash = ((hash << 5) + hash) + tolower(c);
    }
    return hash;
}

Map *map_create(int (*is_equal)(void *key1, void *key2)) {
    Map *newMap = (Map *)malloc(sizeof(Map));
    if (newMap == NULL) return NULL;

    for (int i = 0; i < BUCKETS_LIMIT; i++) {
        newMap->buckets[i] = list_create();
        if (newMap->buckets[i] == NULL) {
            // Si falla la inicialización de alguna lista, liberamos las creadas
            for (int j = 0; j < i; j++) {
                free(newMap->buckets[j]);
            }
            free(newMap);
            return NULL;
        }
    }
    newMap->size = 0;
    newMap->is_equal = is_equal;
    newMap->current_bucket = -1;
    return newMap;
}

Map *sorted_map_create(int (*lower_than)(void *key1, void *key2)) {
    // Las tablas hash son inherentemente desordenadas.
    // Retornamos NULL ya que para este proyecto utilizaremos map_create.
    (void)lower_than;
    return NULL;
}

void map_insert(Map *map, void *key, void *value) {
    if (map == NULL || key == NULL) return;

    // Evitar duplicados
    if (map_search(map, key) != NULL) return;

    unsigned long h = hash_string(key);
    int bucket = h % BUCKETS_LIMIT;

    MapPair *pair = (MapPair *)malloc(sizeof(MapPair));
    if (pair == NULL) return;

    pair->key = key;
    pair->value = value;

    list_pushBack(map->buckets[bucket], pair);
    map->size++;
}

MapPair *map_remove(Map *map, void *key) {
    if (map == NULL || key == NULL) return NULL;

    unsigned long h = hash_string(key);
    int bucket = h % BUCKETS_LIMIT;

    List *l = map->buckets[bucket];
    MapPair *pair = (MapPair *)list_first(l);
    while (pair != NULL) {
        if (map->is_equal(pair->key, key)) {
            list_popCurrent(l);
            map->size--;
            return pair;
        }
        pair = (MapPair *)list_next(l);
    }
    return NULL;
}

MapPair *map_search(Map *map, void *key) {
    if (map == NULL || key == NULL) return NULL;

    unsigned long h = hash_string(key);
    int bucket = h % BUCKETS_LIMIT;

    List *l = map->buckets[bucket];
    MapPair *pair = (MapPair *)list_first(l);
    while (pair != NULL) {
        if (map->is_equal(pair->key, key)) {
            return pair;
        }
        pair = (MapPair *)list_next(l);
    }
    return NULL;
}

MapPair *map_first(Map *map) {
    if (map == NULL) return NULL;

    for (int i = 0; i < BUCKETS_LIMIT; i++) {
        List *l = map->buckets[i];
        MapPair *pair = (MapPair *)list_first(l);
        if (pair != NULL) {
            map->current_bucket = i;
            return pair;
        }
    }
    map->current_bucket = -1;
    return NULL;
}

MapPair *map_next(Map *map) {
    if (map == NULL || map->current_bucket == -1) return NULL;

    // Primero intentamos avanzar en la lista del bucket actual
    List *l = map->buckets[map->current_bucket];
    MapPair *pair = (MapPair *)list_next(l);
    if (pair != NULL) {
        return pair;
    }

    // Si no quedan más elementos en el bucket actual, buscamos en los siguientes
    for (int i = map->current_bucket + 1; i < BUCKETS_LIMIT; i++) {
        l = map->buckets[i];
        pair = (MapPair *)list_first(l);
        if (pair != NULL) {
            map->current_bucket = i;
            return pair;
        }
    }

    map->current_bucket = -1;
    return NULL;
}

void map_clean(Map *map) {
    if (map == NULL) return;

    for (int i = 0; i < BUCKETS_LIMIT; i++) {
        List *l = map->buckets[i];
        MapPair *pair = (MapPair *)list_first(l);
        while (pair != NULL) {
            MapPair *to_free = pair;
            pair = (MapPair *)list_next(l);
            free(to_free);
        }
        list_clean(l);
    }
    map->size = 0;
    map->current_bucket = -1;
}

void map_destroy(Map *map) {
    if (map == NULL) return;
    map_clean(map);
    for (int i = 0; i < BUCKETS_LIMIT; i++) {
        if (map->buckets[i] != NULL) {
            free(map->buckets[i]);
        }
    }
    free(map);
}
