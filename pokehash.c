#include "pokehash.h"

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