
#include "pokehash.h"

int main() {
    int opcion = 0;
    Equipo miEquipo;
    
    // Inicializamos el equipo vacío al arrancar el programa
    inicializarEquipo(&miEquipo);

    while (opcion != 4) {
        mostrarMenu();
        scanf("%d", &opcion);

        switch (opcion) {
            case 1:
                printf("\n[!] Has entrado a Explorar Pokédex.\n");

                break;
            case 2:
                printf("\n[!] Has entrado a Gestión de Equipo.\n");
                
                break;
            case 3:
                printf("\n[!] Has seleccionado Exportar Equipo.\n");
                
                break;
            case 4:
                printf("\nSaliendo de PokeHash... ¡Hasta luego!\n");
                break;
            default:
                printf("\n[Error] Opción no válida. Intente nuevamente.\n");
        }
    }

    return 0;
}