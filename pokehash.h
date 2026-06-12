// pokehash.h
#ifndef POKEHASH_H
#define POKEHASH_H
#define NUM_TIPOS 18

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tdas/map.h"

typedef enum {
    NORMAL, FIRE, WATER, ELECTRIC, GRASS, ICE, FIGHTING, POISON,
    GROUND, FLYING, PSYCHIC, BUG, ROCK, GHOST, DRAGON,
    DARK, STEEL, FAIRY
} PokemonType;

typedef struct {
    int id;
    char nombre[100];
    char tipo1[20];
    char tipo2[20];
    int total_stats;
    int hp;
    int ataque;
    int defensa;
    int ataque_esp;
    int defensa_esp;
    int velocidad;
    int gen;
} Pokemon;

typedef struct {
    Pokemon* integrantes[6];
    int tope;
} Equipo;

extern Map *pokedex;
extern Map *pokedex_by_id;

void mostrarMenu();
void inicializarEquipo(Equipo* e);
void cargar_data();
void menu_explorar_pokedex();
void mejores10PorStat();
void liberar_pokedex();

void cargar_matriz_debilidades();
void menu_gestion_equipo(Equipo* e);
void agregar_pokemon_equipo(Equipo* e);
void ver_equipo_actual(Equipo* e);

#endif