PONTIFICIA UNIVERSIDAD CATÓLICA DE VALPARAÍSO FACULTAD DE INGENIERÍA ESCUELA DE INGENIERÍA INFORMÁTICA 

## **Proyecto: Aplicación en C** 

**Benjamín Díaz Benjamín Fernández Thomas Molina Jorge Palacios** 

Profesor: **Ignacio Araya** Asignatura: **Estructura de Datos** Fecha de entrega: **27/06/2022** 

**Junio 2022** 

## **Índice** 

|**1**|**Introducción**<br>. . . . . .|**Introducción**<br>. . . . . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**1**|
|---|---|---|---|---|---|
|**2**|**Dominio del problema**||. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**2**|
|**3**|**Descripción de la Aplicación**|||. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**3**|
||3.1|Menú Principal . . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|3|
||3.2|Como Usar<br>. . . . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|3|
||3.3|Opciones . . . . . . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|3|
||3.4|Descripción del Juego|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|4|
||3.5|Diferencias con el Original||. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|4|
|**4**|**Descripción de la Solución** .|||. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**5**|
||4.1|Structs a implementar|. .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|||4.1.1<br>Tipo Entidad|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|||4.1.2<br>Tipo Usuario|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|||4.1.3<br>Tipo CurrentState o||Nivel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|||4.1.4<br>Tipo LeaderBoard||. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|||4.1.5<br>Tipo Nave . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
|||4.1.6<br>Tipo Misil . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||4.2|TDAs a utilizar . . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||4.3|Implementación . . .|. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
|**5**|**Planifcación**. . . . . . .||. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**8**|
|**6**|**Conclusión** . . . . . . . .||. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**9**|
|**7**|**Coevaluación** . . . . . .||. . .|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**10**|



i 

## **1. Introducción** 

En la actualidad los videojuegos son una importante rama del entretenimiento, hoy en día están hechos con mucho trabajo detrás gracias a las herramientas que se han ido creando con el paso del tiempo, generalmente con diseños y gráficas que se asemejan a la realidad, sin embargo en sus origines no era así, poseían diseños simples los cuales eran atractivos para la época, por esta razón marcaron generaciones desde su creación. Por estos motivos se planteó la siguiente interrogante: ¿Será posible implementar un juego retro utilizando los conocimientos de la asignatura? 

El objetivo principal de la aplicación es implementar una versión del videojuego retro "SpaceInvaders", utilizando las distintas herramientas otorgadas durante el curso y las habilidades aprendidas con la práctica. Se demostrará que el curso otorga los conocimientos suficientes como para implementar estructuras de datos y TDAs en una aplicación para que sea rápida, eficiente y estable. 

Entre las desafíos que se pondrán a prueba es el trabajo en equipo, ya que se establecerán objetivos grupales y con límite de tiempo. El grupo deberá organizar responsablemente para construir las funciones del código de mejor forma y más rápido, para entregarlo en los plazos que son necesarios. 

A continuación se explicarán temas como el dominio del problema, las distintas características que tendrá, sus funcionalidades, estructuras utilizadas y se declarará como serán implementadas cada una de ellas, además se mostrara una planificación inicial para el desarrollo del proyecto, finalmente se mostrara una conclusión evaluando el proceso y resultados de este trabajo. 

1 

## **2. Dominio del problema** 

Una gran inquietud que existe hoy en día es el tiempo dedicado a los videojuegos por parte de los jóvenes y como los afecta. El ambiente generado llega a saturar a una persona con estrés, ira u otra emoción de frustración, por ejemplo tenemos títulos como League of Legends, el cual demanda mucho mentalmente por lo competitivo, su comunidad y la complejidad de este. En base a lo anterior, el objetivo del proyecto es ofrecer una entretención sana recreando un clásico de los retro-game. 

El juego esta centrado en partidas cortas, así el usuario no ocupara demasiado tiempo, este podrá guardar su progreso y ajustar la dificultad de su partida, el objetivo para lo anterior es dar control a la persona de ajustar la aplicación a su nivel. Se proporcionara una mini guia, esta introduce al individuo a los conceptos básicos para aventurarse en este videojuego. En conjunto se registra un ranking para que este sienta que hay una meta a superar y así dar un incentivo para superar los siguiente niveles, pero sin existir competencias externas de otros usuarios, solamente personas que estén en el mismo dispositivo. 

En definitiva, se ha tomado el desafió de desarrollar un videojuego que cumpla funciones de satisfacción, logro de metas y sin una exigencia que este lejos de manejar por el usuario, puesto que tampoco se busca que la persona sienta frustración. Por ello se decidió crear una experiencia gratificante mediante un videojuego, en este caso se tomará como referencia los juegos de los años 1970-1980 por ser relativamente simples pero muy icónicos y entretenidos. 

2 

## **3. Descripción de la Aplicación** 

La aplicación que se describirá a continuación consistirá en una nueva interpretación del videojuego de 1978 _«Space Invaders»_ . Para desarrollar la aplicación se tomaron en cuenta las principales características de aquel juego arcade clásico. A continuación se darán detalles sobre el funcionamiento de la aplicación. 

## **3.1. Menú Principal** 

El videojuego contará con una interfaz principal que muestre a su vez un menú en pantalla. El menú principal funcionará como mecanismo para acceder a las demás funcionalidades, entre ellas: Ejecutar el juego, Cambiar el nivel de dificultad y acceder a un sistema de _«Leadboards»_ (un sistema de Rankings que mostrará en pantalla a los 10 mejores jugadores basados en sus puntuaciones). 

## **3.2. Como Usar** 

El usuario ejecutará la aplicación y se desplegará el menú principal, en el que se podrá mover libremente entre las diferentes opciones utilizando las flechas de navegación. 

## **3.3. Opciones** 

**Jugar:** Iniciará una partida nueva. Para ello eliminará la pantalla del menú principal para reemplazarla por la interfaz de juego. En la sección siguiente se describirá a detalle como jugar. 

**Tutorial:** Se mostrará un texto en el que se explica el objetivo y las distintas mecánicas que tiene el juego. El objetivo de este apartado es que el usuario pueda entender previamente el funcionamiento del juego. **Dificultad:** El usuario podrá elegir entre tres niveles de dificultad, «Fácil», «Medio» y «Difícil». La dificultad alterará ciertos factores del juego para que le sea más o menos difícil al usuario. 

**Rankings:** Se mostrará un cuadro en el que aparecerán los 10 mejores jugadores basados en su puntuación. De esta forma el usuario puede comparar sus registros actuales con los de partidas anteriores. **Salir:** Finaliza la aplicación. 

3 

## **3.4. Descripción del Juego** 

El juego coloca al usuario al control de una nave espacial, la cual está bajo ataque por naves extraterrestres. El objetivo básicamente consiste en destruir a todas las naves enemigas, las cuales se acercaran realizando un movimiento perpetuo en zigzag, mientras disparan en línea recta hacía la nave del jugador. Para conseguir el objetivo, el usuario dispone de su propia arma, la cual dispara de la misma forma que las naves enemigas, pero a merced del jugador (al momento de apretar un botón). también para esquivar los disparos enemigos, se le concederá al jugador la habilidad de desplazarse lateralmente (hacia la izquierda y derecha). El nivel acaba cuando el jugador destruye todas las naves enemigas del escenario o al contrario, estas destruyen la nave del jugador. 

## **3.5. Diferencias con el Original** 

Si bien la aplicación busca basarse en el juego de las recreativas antiguas, existen ciertos añadidos o extras que se agregarán al videojuego, algunas diferencias serán: 

1. **Ataque/Nave Especial:** Existirá la posibilidad en el juego, de que aparezca en el nivel una nave única que entrará y saldrá de la pantalla. En caso de que el usuario consiga dispararle a la nave, se le concederán puntos extra, una vida extra o ganará la habilidad de ejecutar 3 disparos más poderosos que pueden darle a todos los enemigos que estén en la linea/radio de disparo. 

2. **Variación de Dificultad:** Esta variación consistirá en 3 factores, la disposición de las naves enemigas, la frecuencia de disparo, y la velocidad del movimiento.La primera consiste en la cercanía de las naves enemigas con respecto al jugador y la cantidad de estas por ronda, además aumenta la frecuencia de dispara en naves enemigas, por lo cual el usuario deberá estar más atento para evitar perder todas sus vidas y se vuelva más desafiantes las rondas, también puede llegar a aparecer un "Jefe final". La segunda variación, consiste en modificar una variable que definirá cada cuantos segundos dispara una nave enemiga (este factor trabaja con probabilidades). La tercera variación dependerá de un porcentaje asignado a cada dificultad, la cual definirá que tan rápido se moverán todas las naves enemigas en el nivel. 

   - La aparición del "jefe final"varia según la dificultad, si es fácil aparecerá después de 7 niveles, en medio después de 5 y en difícil después de 3. 

3. **Vidas:** Tanto el usuario como los enemigos pueden tener una cantidad específica de "vidas". Ambos pierden una vida por cada disparo recibido. La cantidad de vidas del usuario dependerá de la dificultad con la que desee jugar. La cantidad de vida de los enemigos se mantendrá constante (1 vida) en todas las dificultades. 

4 

## **4. Descripción de la Solución** 

La aplicación consta principalmente con dos tipos de «structs», la primera son las tipo entidad y la segunda son tipo dato. Las tipo _entidad_ sirven para guardar la información de las distintos objetos que pueden llegar a aparecer en el desarrollo del juego, como por ejemplo: el jugador, enemigos de rango bajo o jefes. Los tipo _dato_ son aquellas que van a guardar información global, por nombrar algunos: dimensiones de pantalla a «dibujar», cantidad de entidades en una partida, puntos obtenidos en la ronda, etc. Toda esta información nos permitirá desarrollar nuestra aplicación en lo previsto. 

## **4.1. Structs a implementar** 

## **4.1.1. Tipo Entidad** 

La _struct_ «Entidad» permite representar todo tipo de entidades que existen en el juego. Las variables del dato especificarán a su vez, características del objeto necesarias para establecer parámetros. Los campos de la _struct_ «Entidad» son: «vida», que almacenara las vidas que posea un objeto; «rectángulo», otra struct que guarda las dimensiones de un paralelogramo; un tipo booleano, «permitirDisparar», que será como el çooldown", que junto con la variable razonDisparo"se maneja "municiones"de una entidad y finalmente una struct de tipo Misil que almacena los disparos. 

## **4.1.2. Tipo Usuario** 

La _struct_ «Usuario» se compone de un «puntaje» y un «user», el primero guarda los puntos que va acumulando el jugador a lo largo de los niveles, en cambio, «user» guardará nombre de máximo 3 letras que representa el nombre que lleve el jugador, en el siguiente campo esta un entero denominado «round», que almacena el nivel al cual llegó el jugador y finalmente hay una variable que guardará la vida de esta entidad. 

## **4.1.3. Tipo CurrentState o Nivel** 

El tipo de dato «CurrentState» servirá para representar el juego como estados o grafos, este se modificará si ocurre un evento que puede desencadenar una serie de acciones (funciones) que dirijan el juego (avanzar al siguiente nivel, morir o algún otro). Tiene una matriz de entidades para representar a los enemigos, el «nivel» que es un entero, el cual guarda el número del nivel, otro entero que dice cuantos enemigos hay en total y un X e Y que nos dicen las dimensiones de la matriz. 

## **4.1.4. Tipo LeaderBoard** 

La _struct_ se utilizará para manejar los datos que se implementarán en la lista de mejores puntajes en el juego. Se toman en cuenta dos variable: «dataList», que es una lista que almacena los datos de la «leaderboard» actual; y «amountRegs», que guarda la cantidad de registros en la lista. 

5 

## **4.1.5. Tipo Nave** 

Esta struct representa la nave del jugador, tiene siete componentes de X e Y, que sirven para modelar la nave, y una velocidad para el eje x y otra para el eje y, también posee un tipo Misil que representa a los misiles que este va soltando. 

## **4.1.6. Tipo Misil** 

Como el nombre indica la struct representa a los Misiles en juego, tienen dos componentes x e y, la primera representa la parte superior y la segunda su parte inferior, además posee un entero para representar la velocidad en x e y, por ultimo tiene un tipo Misil que sirve como lista. 

## **4.2. TDAs a utilizar** 

1. **Grafo:** La _struct_ «CurrentState» se encargará de dirigir el grafo. Se aplicará una TDA en función de representar con nodos los niveles de juego. Ciertos nodos representarán eventos dependiendo de las variables de la _struct_ , por ejemplo: si en un estado un disparo y un enemigo se encuentran en la misma posición, entonces el enemigo perderá una vida. Esto puede llegar a desencadenar una serie de eventos (el enemigo tiene 0 vidas ahora, por lo tanto se elimina. No quedan enemigos en la pantalla se avanza de nivel.) que dirijan el juego. Se eligió la TDA de grafo para poder tener más libertad con las conexiones, además que los grafos son mucho más capaces que otras TDAs de representar situaciones o problemas complejos que tengan más de una solución posible. 

2. **Lista:** La _struct_ «LeaderBoard» depende de una lista. Esta lista almacenará variables tipo «data» con toda la información de los jugadores que están entre los mejores del registro. Se importará un archivo _.csv_ que contenga los datos del registro ordenados por el ranking, estos a su vez, serán traspasados a una lista que contenga las variables tipo «data». Al finalizar una partida, los datos se guardarán en una variable auxiliar tipo «Usuario» y se comparará el «finalScore» obtenido (variable finalScore) en la partida reciente con los demás registros, en cuanto el puntaje final haya superado a un registro se realiza un pushCurrent para insertar el nuevo registro en la lista. La variable ranking de la struct actual y las siguientes en la lista, se modificarán para calzar con el nuevo orden. La lista finalmente se exporta (sobreescribe) al antiguo _.csv_ . La lista se eligió porque es capaz de dar un orden a los datos ingresados, también permite un recorrido lineal y más simple de los datos. 

6 

## **4.3. Implementación** 

1. **Menú principal:** Primero se mostrará un menú con distintas opciones, para abordar su ejecución, el usuario podrá desplazarse a través de las opciones del menú utilizando dos teclas representen las entradas (direccionales) arriba y abajo. Al momento de estar en la opción deseada, el jugador presionará la tecla _enter_ para ejecutar dicha función. 

2. **Jugar:** En este apartado se ejecutara principalmente el juego, tendremos dos opciones, Iniciar una Partida Nueva o Continuar una Partida Anterior, una opción creará una nueva struct tipo Üsuario otra buscara en alguna estructura si hay algún perfil que coincida. 

3. **Iniciar una Partida Nueva:** Esta función ejecuta los niveles generados por un sistema previamente definido, se podrá guardar el progreso de los niveles a medida que estos sean completados y funcionará mediante un ciclo que rescate la acción tomada por el usuario, si este quiere ir hacia la derecha presionara una tecla y si quiere ir hacia la izquierda presionara otra y así con cada interacción que se vaya desarrollar, si el usuario desea salir de esto puede presionar otra tecla que será predefinida para volver al menú o puede perder su progreso cometiendo suicidio en el juego perdiendo todos sus intentos. 

4. **Continuar una Partida Anterior:** Si un usuario desea ingresar a su progreso previamente guardado, debe pulsar la tecla _enter_ en la opción «continue». De aquí en adelante solo se recorren los niveles restantes hasta finalizar el juego. Para identificar la partida guardada con anterioridad, se utilizará un archivo .txt que almacenará información como: "Último nivel Jugado", Çantidad de Vidas "Puntaje Acumulado". De esta forma al cargar la partida, se abre el archivo .txt y la aplicación recopilará esa información para insertarla en el juego. Luego de ser procesada la información del archivo, este se cierra y se carga la pantalla de juego. 

5. **Sistema de Ranking:** La opción «´Leaderboard» permite ejecutar y visualizar un sistema de Ranking por pantalla. Se mostrará mediante la impresión de una lista con los 10 mejores _scores_ que hubo en todo el registro del videojuego. Se implementará gracias a un archivo .csv que estará dentro de los archivos del juego y almacenará variables tipo «data» de las partidas de los jugadores, además de utilizar listas para el manejo de la información (insertar un nuevo registro, mover de lugar cierto registro, eliminar todos los registros). 

6. **Dificultad:** Dicha opción modifica las dificultades generales del sistema de juego, ya sea velocidad, frecuencia de disparo o el número de entidades. Se mostrara por pantalla las tres dificultades (fácil, medio y difícil), además se indicará como son afectadas las entidades, el usuario podrá escoger con las fechas de arriba y abajo cual desea seleccionar, una vez sobre su opción solo deberá presionar la tecla espacio o enter para modificar los datos y el sistema lo devolverá al menú principal. 

7. **Fin de Ejecución:** Función que finaliza el programa y cierra todos los archivos abiertos si es que los hay. Se debe pulsar la opción «exit». 

7 

## **5. Planificación** 

La planificación de este proyecto está detallada en la siguiente tabla: 

|**MES**|**MAYO**|**MAYO**|**MAYO**|**MAYO**|**MAYO**|**MAYO**|**MAYO**|**MAYO**|**MAYO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**|**JUNIO**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**ACTIVIDAD**|**DIA**||||||||||||||||||||||||||||||||||||
|**PREVIO INFORME**|23|24|25|26|27|28|29|30|31|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|**Encargado(s):**|
|Elección Tema||||||||||||||||||||||||||||||||||||Todos|
|**DESARROLLO INFORME**|||||||||||||||||||||||||||||||||||||
|Introducción||||||||||||||||||||||||||||||||||||Todos|
|Dominio del problema||||||||||||||||||||||||||||||||||||Todos|
|Descripción de la aplicación||||||||||||||||||||||||||||||||||||Todos|
|Descripción de la solución||||||||||||||||||||||||||||||||||||Todos|
|Planifcación||||||||||||||||||||||||||||||||||||Todos|
|Conclusión||||||||||||||||||||||||||||||||||||Todos|
|**DESARROLLO APLICACIÓN**|||||||||||||||||||||||||||||||||||||
|Menú Principal||||||||||||||||||||||||||||||||||||Thomas Molina/Jorge Palacios|
|Interfaz gráfca||||||||||||||||||||||||||||||||||||Benjamín D./Benjamín F.|
|Implementar entidades||||||||||||||||||||||||||||||||||||Todos|
|Implementar disparos y habilidades||||||||||||||||||||||||||||||||||||Todos|
|Sistema de niveles||||||||||||||||||||||||||||||||||||Benjamín F./Thomas Molina|
|Sistema de Rankings||||||||||||||||||||||||||||||||||||Benjamín D/Jorge Palacios|
|Habilitar ajustes de difcultad||||||||||||||||||||||||||||||||||||Benjamín F./Thomas Molina|
|Integrar funciones al código principal||||||||||||||||||||||||||||||||||||Todos|
|Pulir las distintas funciones||||||||||||||||||||||||||||||||||||Todos|
|Testeo y depuración||||||||||||||||||||||||||||||||||||Todos|



8 

## **6. Conclusión** 

En un inicio la problemática planteada era que los jóvenes dedicaban mucho tiempo a los videojuegos y muchas veces eso llega a traer malas emociones por como están hechos en la actualidad (La competitividad existente, las comunidades que se forman, etc.). El principal objetivo de este proyecto era desarrollar un juego que no tuviera las características negativas de los actuales y de paso tomar de referencia un clásico de la década de los 70, Space-Invaders. En general, se logró el propósito inicial del trabajo y se consideró que la problemática planteada fue solucionada gracias a este trabajo. 

En la codificación se ocupó principalmente SDL para trabajar con las animaciones y darle un toque más estético. Se hizo uso de varias _structs_ y algunas TDAs para administrar información, se buscó hacer la implementación más simple posible para intentar cumplir con los plazos. El trabajo llevado con esta herramienta (SDL) presentó un desafío, puesto que era algo nuevo, lo que determinaría una investigación previa para poder desarrollar la interfaz de juego. 

Se considera como fortaleza principal el compromiso que el equipo demostró con el desarrollo del proyecto, tanto en el informe como en el código y la unidad para la toma de decisiones, puesto a que el grupo fue capaz de sacar ideas y modelarlas durante el proceso de trabajo. Sin embargo, la principal debilidad a mencionar, es la alta expectativa que se generó durante las etapas iniciales del proyecto, lo que llevó a abarcar más de lo que se podía manejar. A causa de lo anterior, es que se sufrió un retraso en los tiempos, por ejemplo, se llegó a modelar un sistema de grafos entre enemigos y eventos, pero dado a que otras características recaudaron más tiempo este sistema resultó cancelado. En general, hay varios aspectos que pudieron ser mejorados o previstos, pero el resultado obtenido es cercano a lo esperado por parte del equipo. 

9 

## **7. Coevaluación** 

[ASPECTOS-POSITIVOS] 

- Benjamín Díaz: Compromiso, Proactivo. 

- Benjamín Fernández: Flexibilidad, Esfuerzo. 

- Thomas Molina: Resiliente, Optimista. 

- Jorge Palacios: Creatividad, Compañerismo. 

[ASPECTOS-A-MEJORAR] 

- Benjamín Díaz: Mejorar organización del tiempo. 

- Benjamín Fernández: Organización general, Planificación de metas. 

- Thomas Molina: Mejorar tiempo de organización, Emplear mayor tiempo a codificación. 

- Jorge Palacios: Mejorar los tiempos de programación. 

[PUNTOS] 

- Benjamin Diaz: 0 

- Benjamin Fernandez: 0 

- Thomas Molina: 0 

- Jorge Palacios: 0 

10 

