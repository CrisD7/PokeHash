## PONTIFICIA UNIVERSIDAD CATÓLICA DE VALPARAÍSO FACULTAD DE INGENIERÍA ESCUELA DE INGENIERÍA INFORMÁTICA 

# **The Binding of Isaac: Companion App** 

**José Osega Bryan López** 

Profesor: **Ignacio Araya** Asignatura: **Estructura de Datos** 

**Junio 2021** 

## **Índice** 

|**1**|**Introducción**<br>. . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|**1**|
|---|---|---|---|
|**2**|**Dominio del Problema**<br>. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|**2**|
|**3**|**Descripción de la Aplicación**|. . . . . . . . . . . . . . . . . . . . . . . . . .|**3**|
||3.1<br>Funcionalidades de la aplicación . . . . . . . . . . . . . . . . . . . . . . . .||3|
||3.1.1<br>Menú de Opciones|. . . . . . . . . . . . . . . . . . . . . . . . . . .|3|
||3.1.2<br>Menú de Desbloqueo . . . . . . . . . . . . . . . . . . . . . . . . . .||4|
||3.2<br>¿Qué no puede hacer la aplicación? . . . . . . . . . . . . . . . . . . . . . .||4|
|**4**|**Descripción de la Solución** .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|**5**|
||4.1<br>Librería ncurses . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
||4.2<br>Tipos de datos<br>. . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
||4.3<br>TDAs y Estructuras de Datos . . . . . . . . . . . . . . . . . . . . . . . . .||5|
||4.3.1<br>Mapa<br>. . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||4.3.2<br>Lista . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||4.4<br>Implementación de las funciones anteriormente nombradas . . . . . . . . .||6|
||4.4.1<br>Menú de Opciones|. . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||4.4.2<br>Menú de desbloqueos . . . . . . . . . . . . . . . . . . . . . . . . . .||7|
|**5**|**Planifcación**. . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|**9**|
|**6**|**Conclusión** . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|**10**|
|**7**|**Coevaluación** . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . . .|**11**|



i 

## **Lista de Figuras** 

1 Primera habitación de TBOI Flash . . . . . . . . . . . . . . . . . . . . . . 1 2 Ítem con descripción ambigua . . . . . . . . . . . . . . . . . . . . . . . . . 2 3 Carta Gantt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9 

ii 

## **1. Introducción** 

The Binding of Isaac, o en sus siglas TBOI, es uno de los juegos indies más famosos y conocidos en la actualidad, creado por Edmund McMillen, con una base de jugadores de más 5 millones de personas, el juego se ha mantenido en el podio de los juegos roguelike desde el comienzo, cuando se estreno TBOI Flash en el año 2011. 3 años después, con el apoyo de Nicalis, se desarrollo el remake de este juego, y el más conocido, TBOI Rebirth, consiguiendo 3 actualizaciones en forma de DLC, Afterbirth, Afterbirth+ y el recientemente lanzado Repentance, siendo el cierre final de la historia de Isaac. 

La historia de TBOI esta basado en referencias bíblicas, además de las experiencias personales del desarrollador Edmund McMillen, al haber vivido en una familia de fanáticos religiosos, específicamente de los conflictos entre los familiares que eran católicos y los que eran cristianos, y como el se veía afectado por esta situación. Resumidamente, la historia es de la confrontación entre Isaac y su Madre, debido a que la última lo trata de sacrificar, para probar su fe a Dios. 

La principal mecánica del juego, es avanzar a través de mazmorras generadas aleatoriamente, cuya principal inspiración como se puede observar en la figura 1, es The Legend of Zelda o TLOZ. Además, para que el jugador pueda avanzar a través del juego posee una extensa cantidad de ítems para usar, siendo en la actual versión del juego 714 ítems con diversos efectos, pero cabe decir que no están todos estos objetos desbloqueados desde el principio, sino que el jugador debe de desbloquearlos a través de las distintas partidas que el juegue, adentrándose más aun en la historia de Isaac, mientras trata de entender todo lo que esta pasando. 

Debido a la inmensidad del juego, decidimos hacer una aplicación que logre apoyar al usuario nuevo y al experimentado, para que puedan revisar lo que les falta para poder llegar al 100 % del juego de forma clara y sin rodeos, además de poder revisar la información respectiva de los personajes, items, logros y enemigos. 

Figura 1: Primera habitación de TBOI Flash 

1 

## **2. Dominio del Problema** 

Debido a la extensidad del juego que se nombro anteriormente, además del hecho de que a Edmund McMillen quería retratar en el aspecto de jugabilidad sus experiencias de la infancia al jugar los primeros juegos de la saga TLOZ, el tratar de buscar con lo que proporcionaba el juego, como avanzar en su historia, fallando una gran cantidad de veces, pero al poder completarlo sentir como todo sus esfuerzos valieron la pena. 

Esta situación se retrata específicamente en los ítems, dado que sus descripciones son bastantes ambiguas, como es la mostrada en la Figura 2 en lo que conlleva a su función, siendo muy pocos los ítems que los explican de forma directa, haciendo que el jugador tenga que aprender de la prueba y error, entendiendo cuales ítems conviene llevar durante la partida y cuales no. 

La situación anteriormente nombrada, se reitera para lograr avanzar en el juego, ya que los objetivos de como hacerlo no son claros, siendo indicadores minimos los presentados, como son los jefes finales que el jugador haya derrotado a lo largo de sus diversas partidas. Sucede lo mismo para poder desbloquear nuevos ítems, zonas, personajes, entre otros, ya que no se le indica al jugador los pasos que debe seguir para poder desbloquearlos. 

He ahí, donde entra nuestro programa, ya que almacena la información importante para el jugador de los 4 apartados principales para poder conseguir el 100 % del juego, los personajes, los ítems, los logros y los enemigos, para que los jugadores puedan ver con mayor claridad lo que les falta conseguir para poder terminar el juego y como poder conseguirlo en el caso en que no lo sepan. 

Con todo lo anteriormente dicho, para el desarrollo de la aplicación decidimos enfocarnos en la versión del juego TBOI Afterbirth+, debido a que es la que la mayor cantidad de usuarios actualmente poseen, debido a que no han podido comprar TBOI Repentance o porque lo juegan en consolas, como Xbox One o Nintendo Switch, ya que el nuevo DLC para las consolas estará disponible recién a final de año. 

Figura 2: Ítem con descripción ambigua 

2 

## **3. Descripción de la Aplicación** 

Por todo lo anteriormente dicho, The Binding of Isaac: Companion APP surge, como una aplicación para poder guiar al jugador nuevo, mostrando toda la información que le pueda hacer falta, tales como, descripción de los ítems, que estadísticas suben, la descripción de los enemigos, entre otros. También ayudará a los jugadores más experimentados, ya que podrá guardar de forma ordenada la información de su avance, revisar lo que le falta por desbloquear y el como desbloquearlo. Se utilizan 4 archivos .txt creados de antemano, donde se guarda la información de los personajes, ítems, logros y enemigos, haciendo que el usuario solamente actualice la información de su avance en el juego. 

## **3.1. Funcionalidades de la aplicación** 

Aquí se presentan las funciones que puede realizar el programa para que pueda ser usado por el usuario correctamente. 

## **3.1.1. Menú de Opciones** 

Este es el primer menú que se le muestra al usuario, y el principal del programa, que entre sus funcionalidades están: 

- **menuDesbloqueo()** : El usuario ingresa al menú de desbloqueo, que aparece de forma detallada sus funcionalidades en el apartado 3.1.2. 

- **guardarInformación(HashMap * mapaPersonajes, HashMap * mapaItems, * *** 

- **HashMap mapaLogros, HashMap mapaEnemigo)** : Guarda toda la información ingresada por el usuario en los mismos archivo que carga toda la información de los personajes, ítems, logros y enemigos. 

- **buscarItemEspecifico(HashMap * mapaItems, char * nombreItem)** : Busca un ítem en específico, con la respectiva información de lo que hace. 

- 

- **buscarLogroEspecifico(HashMap mapaLogros, int ID)** : Busca un logro en específico del juego, a través de su ID, indicando lo que desbloqueo el usuario. Si se encuentra bloqueado, se indica los pasos para poder desbloquearlo. 

- **buscarEnemigoEspecifico(HashMap * mapaEnemigos, char * nombreEnemigo)** : Busca un enemigo en específico, indicando si se encontró o no, mostrando donde se puede encontrar y la cantidad de vida de el mismo. 

- 

- **mostrarTodosPersonajes(List listaPersonajes)** : Muestra un menú con los 15 personajes existentes en el juego, permitiendo elegir al usuario el personaje que quiera ver, mostrando su respectiva información. 

- 

- **mostrarTodosItems(List listaItems)** : Muestra todos los nombres de los ítem, indicando si se han encontrado aunque sea 1 vez o no. 

- 

- **mostrarLogros(List listaLogros)** : Muestra todos los IDs de los logros, con su respectivo nombre e indicando si se han desbloqueado o no. 

3 

- 

- **mostrarEnemigos(List listaEnemigos)** : Muestra todos los nombres de los enemigos, indicando si se han encontrado aunque sea 1 vez o no. 

- **mostrarPorcentajes(List * listaPersonajes, List * listaItems,List * lista*** 

- **Logros, List listaEnemigos)** : Muestra el porcentaje de los avances del usuario respecto a los personajes, ítems, logros, enemigos y el calculo del porcentaje total. 

## **3.1.2. Menú de Desbloqueo** 

Este es un submenú del programa, cuya función principal es mostrarle al usuario las funciones relacionadas con los desbloqueos de los distintos .txt, cuyas funciones respectivas son: 

- **desbloquearPersonaje(List * listaPersonajes, HashMap * mapaPersonajes)** : Se muestra un menú que esta compuesto por todos los personajes que no hayan sido desbloqueado por el usuario, y el usuario puede elegir el personaje que quiere desbloquear. 

- **marcaLogradaEnPersonaje(List * listaPersonajes, HashMap * mapaPersonajes)** : Se muestra un menú compuesto por todos los personajes desbloqueados y que no hayan sido completados totalmente, el usuario elige uno de los personajes, después elige una marca de logro a actualizar e ingresa la dificultad en la que la completo (siendo estas, normal o difícil). 

- **encontrarItem(HashMap * mapaItems, char * nombreItem)** : Busca un ítem que no haya sido encontrado por nombre, e ingresa si el usuario lo encontró. 

- 

- **desbloquearLogro(HashMap mapaLogros, int ID)** : Busca un logro que no haya sido desbloqueado por ID, e ingresa si el usuario lo desbloqueo. 

- ***** 

- **encontrarEnemigo(HashMap mapaEnemigos, char nombreEnemigo)** : Busca un enemigo no que no haya sido encontrado por nombre, e ingresa si el usuario lo encontró. 

## **3.2. ¿Qué no puede hacer la aplicación?** 

Entre las cosas que el programa no puede hacer, se encuentran: 

No se puede jugar, ya que es una aplicación de apoyo de información. 

- Agregar nuevos personajes, ítems, logros o enemigos, ya que tan solo se utiliza la versión base del juego. 

No puede guardar la partida del juego real. 

No se puede obtener los datos/archivos directamente del juego. 

4 

## **4. Descripción de la Solución** 

La aplicación usara una serie de tipos de datos, TDAs y Estructuras de Datos, para lograr una correcta y eficiente ejecución cada vez que se utilice el programa, los cuales respectivamente son: 

## **4.1. Librería ncurses** 

Esta librería permite la creación interfaces gráficas o GUI basadas en texto fácilmente para los sistemas Linux, siendo la librería similar en Windows, conocida como _conio.h_ . En el programa, se utiliza para mostrar texto con color, poder centrar el texto sin importar el tamaño de la terminal en la que se ejecuta, limpiar la pantalla de la terminal, el poder delimitar una parte de la terminal y utilizarla para generar un menú de opciones, además de activar las teclas de arriba y abajo para poder moverse entre opciones, y la tecla ENTER para poder elegir una opción. 

## **4.2. Tipos de datos** 

En este apartado, indicaremos los tipos de datos que creamos para poder manejar la información a utilizar y que guardaremos en los mapas y en las listas. 

- **tipoPersonaje** ,contiene un string para almacenar el nombre del personaje, que se usa como clave para el HashMap mapaPersonajes, un entero para almacenar si el personaje se encuentra desbloqueado o no y un arreglo de enteros de largo 10, para almacenar las marcas de logros de cada personaje, siendo 0 que no se haya logrado terminar aun, 1 si se logro completar pero en la dificultad normal y 2 si se logro completar en la dificultad difícil. 

- **tipoItem** ,contiene un string para almacenar el nombre del ítem, que es el usado como clave en el HashMap mapaItems y otro string, que almacena la descripción del ítem. 

- **tipoLogros** ,contiene un entero que almacena el ID, que sirve tanto como clave para el HashMap mapaLogros y para ordenarlos cuando se necesite mostrar por pantalla , un entero que guarda si se desbloqueo o no el logro, siendo 1 y 0 respectivamente, un string que guarda la descripción del logro y otro string que guarda la forma de desbloquearlo en el juego. 

- **tipoEnemigo** , contiene un entero que almacena el ID del enemigo, un string que almacenara el nombre del enemigo, y que servirá como clave para el HashMap mapaEnemigos, un entero que indicara si se ha encontrado o no el enemigo, 1 y 0 respectivamente, otro entero que indicara la cantidad de vida del enemigo y un string que almacenara la ubicación del enemigo. 

## **4.3. TDAs y Estructuras de Datos** 

Las estructuras de datos que vamos a ocupar para desarrollar el programa son: 

5 

## **4.3.1. Mapa** 

En el mapa se guardara la información respectiva de los tipos de datos, para este proyecto, usaremos 4 mapas. Las razones por la que usamos un mapa es debido a que necesitamos un TDA que sea eficiente en la búsqueda con una gran cantidad de datos, y que a la vez pueda almacenar las características asociadas a los datos. 

- **mapaPersonajes** : Como clave se guardará el nombre, y como dato almacenaran todo lo demás que se almacena en el tipoPersonaje. 

- **mapaItems** : Como clave se guardará el nombre, y como dato almacenaran todo lo demás que se almacena en el tipoItems. 

- **mapaLogros** : Como clave se guardará el ID del logro, y como dato almacenaran los datos que se guardan en tipoLogros. 

- **mapaEnemigos** : Como clave se guardará el nombre, y como dato almacenaran los datos que se guardan en tipoEnemigo. 

## **4.3.2. Lista** 

En la lista, vamos a guardar la información respectiva de los tipos de datos que usamos, al igual que el mapa, se usaran 4 listas, para almacenar los personajes, ítems, logros y enemigos, respectivamente. Las razones por la que usamos una lista, es para guardar de forma ordenada la información en su respectivo archivo .txt, además de poder mostrar la información de forma ordenada al usuario. 

## **4.4. Implementación de las funciones anteriormente nombradas** 

## **4.4.1. Menú de Opciones** 

- **menuDesbloqueo()** : Esta función mostrará otro submenú que indique otra categoría de opciones relacionadas con el desbloqueo o encuentro de ítems, personajes, logros o enemigos. 

- **guardarInformación(List * listaPersonajes, List * listaItems, List * lis*** 

- **taLogros, List listaEnemigo)** : Esta función guardará la información que fue ingresada por el usuario, para que a posteriori, cuando el usuario quiera volver a ingresar al programa no tenga que volver a desbloquear cosas que ya había desbloqueado con anterioridad. 

- ***** 

- **buscarItemEspecifico(HashMap mapaItems, char nombreItem)** : El usuario ingresa el nombre de algún ítem del juego, el programa lo busca dentro del mapaItems, si se encuentra dentro del mapa, muestra por pantalla el nombre del ítem y el efecto que otorga al jugador. Si no se encuentra, se muestra por pantalla un mensaje indicando que se equivoco de ítem. 

6 

- 

- **buscarLogroEspecifico(HashMap mapaLogros, int ID)** : El usuario ingresa el ID del logro que desea revisar, el programa lo busca dentro del mapaLogros, si se encuentra, se muestra por pantalla el nombre del objeto, si se desbloqueo y el efecto que le otorga al jugador al conseguirlo. Si no lo encuentra dentro del mapa, se indica que tal ítem no existe. 

- **buscarEnemigoEspecifico(HashMap * mapaEnemigos, char * nombreEnemigo)** : El usuario ingresa el nombre del respectivo enemigo que desea encontrar, el programa busca al enemigo dentro del mapaEnemigo, si lo encuentra, indicara su nombre, si el jugador lo ha encontrado, su cantidad de salud y donde se puede encontrar en el juego. Si no lo encuentra, indicara que tal enemigo no existe. 

- 

- **mostrarTodosPersonajes(List listaPersonajes)** : Se muestra por pantalla a los 15 personajes existentes en TBOI Afterbirt+, mostrando los nombres de cada personaje y permitiendo al usuario elegir uno, para desplegar por pantalla su nombre, si se encuentra desbloqueado y sus marcas de logro, indicando si las ha terminado o no, siendo tres instancias dependiendo si lo ha hecho y en que dificultad la completo (NO, NORMAL, DIFICIL). 

- 

- **mostrarTodosItems(List mapaItems)** : Se muestran los nombres de todos los items del juego existentes hasta TBOI Afterbirth+, e indica si el usuario ha encontrado o no el objeto. 

- **mostrarLogros(List * mapaLogros)** : Se muestran todos los IDs de los logros del juego hasta TBOI Afterbirth+, indicando el nombre del logro y si se el jugador los desbloqueo o no. 

- **mostrarEnemigos(List * mapaEnemigos)** : Se muestran todos los enemigos existentes hasta TBOI Afterbirth+, indicando el nombre del enemigo y si se el usuario lo ha encontrado o no. 

- **mostrarPorcentajes(List * listaPersonajes, List * listaItems,List * listaLogros, List * listaEnemigos)** : Se calcula el total de los avances del jugador en cada aspecto almacenado, para los personajes se suma 1 si se encuentran desbloqueado y por cada marca de logro, 1 si se completo en dificultad normal y 2 si se completo en dificultad difícil, para los ítems, logros y enemigos se suma 1 por si se ha encontrado/desbloqueado. Posteriormente, cada uno se divide en el total de puntos que puede obtener el jugador, consiguiendo los porcentajes individuales. Para finalizar, el porcentaje total es la suma de los porcentajes anteriores, dividido en 4. 

## **4.4.2. Menú de desbloqueos** 

- ***** 

- **desbloquearPersonaje(List listaPersonajes, HashMap tipoPersonaje)** : Primero se muestra un menú con todos los personajes que el usuario no ha desbloqueado, posteriormente el usuario tiene que ingresar la tecla ENTER en algún personaje, y se mostrara por pantalla un mensaje indicando que lo desbloqueo. En el caso, que no se quiera desbloquear algún personaje, existe una opción para salir del menú. 

7 

- **marcaLogradaEnPersonaje(List * listaPersonajes, HashMap * mapaPersonajes** : Al igual que la opción anterior, se muestra un menú con todos los personajes, pero en este caso, aquellos que se encuentren desbloqueados y que no hayan sido totalmente completados (Todas las marcas de logro en dificultad difícil). Tras esto, se mostrara la información del personaje y se le preguntara al usuario cual marca quiere actualizar, y en que dificultad la completo. 

- ***** 

- **encontrarItem(HashMap mapaItems, char nombreItem)** : El usuario ingresa el nombre del ítem que encontró, si no se equivoca al escribirlo, se muestra por pantalla al usuario que se actualizo la información del ítem, indicando que lo encontró. De caso contrario, se le indicara al usuario por pantalla que le indica que se ha equivocado al escribir el nombre del ítem. 

- **desbloquearLogro(HashMap * mapaLogros, int ID)** :El usuario ingresa el ID del logro que ha desbloqueado, el programa busca en el mapaLogros el logro con el ID ingresado, si lo encuentra se indica por pantalla que se realizo el cambio de información. En el caso contrario, se le indica al usuario que el ID ingresado no se encuentra asociado a ningún logro. 

- **encontrarEnemigo(HashMap * mapaEnemigos, char * nombreEnemigo)** :El usuario ingresa el nombre de un enemigo que haya encontrado, el programa lo busca en el mapaEnemigos, si lo encuentra le indica al usuario por pantalla que la información acerca de ese enemigo, ha sido actualizada. Si es el caso contrario, se le indica al usuario que el nombre ingresado no se encuentra asociado a ningún enemigo del juego. 

8 

## **5.** 

La planificación de nuestro proyecto, con la división de las tareas en el tiempo estipulado se puede observar, en la presente Carta Gantt. 

Figura 3: Carta Gantt 

9 

## **6. Conclusión** 

Lo que podemos concluir del trabajo realizado, The Binding of Isaac: Companion App. Podemos concluir, que a través de nuestro programa más personas tratara de adentrarse a este juego, ya que la principal característica por la cual una cantidad de jugadores no avanza en el juego o ni siquiera lo trata de probar, es la poca claridad que posee durante las primeras 100 horas de juego, logrando guiar mejor a los jugadores novatos, mientras que a los jugadores más experimentados, lo utilizarán para poder tener de forma más ordenada los avances que han llevado en su partida. 

Esta aplicación sirve para que los jugadores puedan tener sus datos organizados, con los datos nos referimos a los ítem, personajes, enemigos y logros, que tiene el juego The Binding of Isaac, hasta su expansión Afterbirth plus. Con esto nos referimos a que el usuario podrá llevar un orden de los objetos/enemigos que ha encontrado/desbloqueado en el juego, así llevar un porcentaje de avance que indica cuanto has avanzado en el juego. También es capaz de mostrar todos los datos o buscar uno en especifico, y dependiendo del dato puede mostrar más información. 

Al principio optamos por usar un hashmap para guardar los datos, ya que nos era más fácil a la hora de buscar algún objeto, ítem, logro o enemigo, pero más tarde cuando implementamos el código tomamos la decisión de implementar a la vez una lista que nos sirve a la hora de mostrar todos los datos de forma ordenada. Al principio también queríamos hacer un menú con imágenes, pero no se vio factible, debido a que las posibles soluciones eran imágenes pero en una ventana aparte a la terminal, entonces se descartó la idea, luego, José Osega encontró una biblioteca _ncurses_ que permitía hacer un menú, centrarlo en la terminal y poder implementar las _páginas_ , con esto nos referimos a mostrar los datos que quepan en la terminal, y para ver los siguientes, apretar _ENTER_ , esto se muestra en las funciones que se muestran los ítem, logros y enemigos. 

10 

## **7. Coevaluación** 

Consideramos que ambos trabajamos en general bien, logrando aportar para el trabajo en igual cantidad. La evaluación respectiva es la siguiente: 

- **José Osega** : Como aspecto positivos, trabajó en todo el desarrollo del proyecto, revisando que todo estuviera bien en todo momento. Cabe destacar que trabajó desde antes que el profesor nos enviara las instrucciones, teniendo las ideas claras del programa que íbamos a hacer y así pudimos ver desde el primer momento alguna opción de hacer un código bonito e innovador. Además, descubrió la librería _ncurses.h_ que nos sirvió para que el código se vea muy bien. Como aspecto a mejorar, es la explicación de lo que tenía en mente como programa, ya que fue un poco confuso al principio. 

- **Bryan López** : En los aspectos positivos, cabe decir que se organizo de mejor manera para trabajar en todo el proyecto, situación que mas se noto durante la elaboración del código y la edición del video. También dio varias ideas para la estética del programa, y entendió de forma rápida la inclusión de la librería _ncurses.h_ que no habíamos usado nunca anteriormente. De puntos a mejorar, es la confianza en sus habilidades, ya que no era muy optimista con lo que hacia, además de tener confianza con sus compañeros de forma general, por la misma situación anterior. 

11 

