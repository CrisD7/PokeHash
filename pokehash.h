// pokehash.h
#ifndef POKEHASH_H
#define POKEHASH_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tdas/map.h"

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

void mostrarMenu();
void inicializarEquipo(Equipo* e);
void cargar_data();
void explorar_pokedex();
void liberar_pokedex();

#endif