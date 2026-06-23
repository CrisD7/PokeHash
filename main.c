#include "pokehash.h"
#include "tdas/extra.h"

int main() {
    int opcion = 0;
    Equipo miEquipo;
    
    cargar_data();
    inicializarEquipo(&miEquipo);

    while (opcion != 4) {
        limpiarPantalla();
        mostrarMenu();
        scanf("%d", &opcion);

        switch (opcion) {
            case 1:
                menu_explorar_pokedex();
                break;
            case 2:
                menu_gestion_equipo(&miEquipo);
                break;
            case 3: {
                limpiarPantalla();
                printf("\n[!] Has seleccionado Exportar Equipo.\n");
                printf("Ingrese el nombre del archivo (ejemplo: mi_equipo.txt): ");
                char filename[256];
                if (scanf("%255s", filename) == 1) {
                    exportar_equipo(&miEquipo, filename);
                }
                presioneTeclaParaContinuar();
                break;
            }
            case 4:
                limpiarPantalla();
                printf("\nSaliendo de PokeHash... ¡Hasta luego!\n");
                break;
            default:
                limpiarPantalla();
                printf("\n[Error] Opción no válida. Intente nuevamente.\n");
        }
    }

    liberar_pokedex();
    return 0;
}