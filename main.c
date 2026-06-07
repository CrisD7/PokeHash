
#include "pokehash.h"
#include "tdas/extra.h"

void cargar_data(){
    FILE *archivo = fopen('Pokemon.csv', 'r');
    if(archivo == NULL){
        perror(
            "Error al abrir el archivo");
        return;
    }

    char **campos;

    campos = leer_linea_csv(archivo, ',');

    while((campos = leer_linea_csv(archivo, ',')) != NULL){
        Pokemon *pmon = (Pokemon *)malloc(sizeof(Pokemon));
        pmon -> id, campos[0];
        strcpy(pmon -> nombre, campos[1]);
        strcpy(pmon -> tipo1, campos[3]);
        strcpy(pmon -> tipo2, campos[4]);
        pmon -> total_stats = campos[5];
        pmon -> hp = campos[6];
        pmon -> ataque = campos[7];
        pmon -> defensa = campos[8];
        pmon -> ataque_esp = campos[9];
        pmon -> defensa_esp = campos[10];
        pmon -> velocidad = campos[11];
        pmon -> gen = campos[12];
        
    }
}



int main() {
    int opcion = 0;
    Equipo miEquipo;
    
    cargar_data();

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