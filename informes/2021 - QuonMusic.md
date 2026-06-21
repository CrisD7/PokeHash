## PONTIFICIA UNIVERSIDAD CATÓLICA DE VALPARAÍSO FACULTAD DE INGENIERÍA ESCUELA DE INGENIERÍA INFORMÁTICA 

## **Proyecto de Estructura de Datos QuonMusic** 

**Iván Patricio Galaz Robledo Jefté Benjamín Ponce Hidalgo Pablo Andrés Ortiz Leiva Darien Nicolás Pacheco Cantillana** 

Profesor: **Ignacio Araya** Asignatura: **Estructura de datos** 

**Julio 2021** 

## **Índice** 

|**1**|**Introducción**<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**1**|
|---|---|---|
|**2**|**Dominio del problema**<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**2**|
|**3**|**Descripción de la aplicación** . . . . . . . . . . . . . . . . . . . . . . . . . . .|**3**|
||3.1<br>Funciones menú inicio de sesión . . . . . . . . . . . . . . . . . . . . . . . .|3|
||3.2<br>Funciones menú principal . . . . . . . . . . . . . . . . . . . . . . . . . . . .|3|
|**4**|**Descripción de la solución** . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**5**|
||4.1<br>Descripción de tipos de datos<br>. . . . . . . . . . . . . . . . . . . . . . . . .|5|
||4.1.1<br>Estructura usuario . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
||4.1.2<br>Estructura canción . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
||4.1.3<br>Estructura artista . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||4.1.4<br>Estructura género . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
||4.2<br>Detalles de los TDA<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
||4.2.1<br>TDA Lista enlazada doble . . . . . . . . . . . . . . . . . . . . . . .|7|
||4.2.2<br>TDA Mapa<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
||4.2.3<br>TDA Árbol binario . . . . . . . . . . . . . . . . . . . . . . . . . . .|7|
||4.3<br>Implementación de las funcionalidades<br>. . . . . . . . . . . . . . . . . . . .|8|
|**5**|**Planifcación**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**10**|
|**6**|**Conclusión** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**11**|
|**7**|**Coevaluación** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|**12**|



i 

## **Lista de Figuras** 

|1|Estructura usuario<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|---|---|---|
|2|Estructura canción . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|5|
|3|Estructura artista . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
|4|Estructura género . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|6|
|5|Carta Gantt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|10|



ii 

## **1. Introducción** 

En el contexto de pandemia actual la salud mental se ha convertido en un problema gigante para toda la población global, las personas buscan la manera de “desconectarse” por un momento de la realidad para reducir el alto estrés que está presente en el día a día el cual se ve ampliado por las condiciones de la crisis sanitaria actual. Lo anterior ha llevado a las personas a explotar aún más las actividades que brindaban momentos de relajación, esto quiere decir que actividad de ocio como jugar videojuegos, redes sociales, ver películas o escuchar música por ejemplo, se realicen de manera mucho más frecuente que antes de la pandemia, tanto así que, desde el comienzo del aislamiento por el virus, el uso de internet en el mundo ha ido creciendo considerablemente, aumentando en un 7.3 por ciento en el último año (Galeano, 2021). A partir de lo mencionado anteriormente, una de las actividades que más afecta al cuerpo y cerebro humano es el escuchar música, esto debido a que la música contiene numerosos beneficios para el ser humano, tales como fortalecer el aprendizaje y la memoria, regular las hormonas relacionadas con el estrés y hasta permitir evocar experiencias y recuerdos (UDEP, 2020), teniendo incluso la capacidad de liberarnos por minutos de todo lo que está pasando. Es por ello que este grupo de trabajo se enfocará completamente en el desarrollo de una aplicación que recomiende de la manera más precisa canciones que no escapen del interés musical que tiene el auditor al momento de escuchar música. 

El objetivo principal de este proyecto es recomendar música de manera precisa y personalizada a partir de los gustos musicales de cada persona, de tal forma que el usuario no se vuelva a encontrar con la problemática de no saber qué escuchar o no estar a gusto con las recomendaciones de las aplicaciones tradicionales de reproducción de música. Además, esta aplicación permitirá a los usuarios expandir sus gustos musicales, desde poder encontrar nuevos artistas relacionados al género preferido hasta visualizar las mejores canciones escogidas por los propios usuarios que utilicen la aplicación. 

1 

## **2. Dominio del problema** 

La música está presente en el día a día de todas las personas, tanto así que la mayoría de las personas del mundo escuchan en promedio 17,8 horas semanales de cualquier tipo de música (IFPI, 2018). Sin embargo, encontrar música o géneros de los estilos que apetece escuchar no siempre resulta sencillo, ya que aplicaciones como Youtube o Spotify normalmente te recomiendan canciones que ya has escuchado antes o música que no encaja con lo que se quiere escuchar en el momento, volviéndose todo muy repetitivo y cumpliendo las expectativas del usuario. Esto condiciona a las personas a pasar mucho tiempo indagando en la web buscando música que se acomode los gustos de cada uno. 

A partir de todo lo anterior, en este proyecto se plantearon las siguientes preguntas, ¿qué pasa con las personas que no saben qué escuchar? ¿las personas saben cuáles son sus gustos? 

Específicamente el problema que busca resolver este proyecto es la dificultad que puedan tener algunas personas para encontrar nuevas canciones o nuevos géneros a los cuales escuchar. A partir de esto, es necesario considerar que esta problemática no se le presenta a todas las personas, es más bien dirigida a un grupo con poco tiempo de ocio (no tengan mucho tiempo para estar buscando canciones nuevas), que sean nuevos en el mundo de la música y/o del género que está escuchando y quieran descubrir nuevas canciones, artistas o géneros musicales, para así tener la posibilidad de expandir sus gustos en el mundo de la música; sin embargo puede ser perfectamente aplicable para alguien que ya se maneje en el tema pero tenga curiosidad por descubrir nuevos aires. 

Tomando en consideración todo lo anterior, se creará una aplicación que se enfocará en recomendar música al usuario en muy poco tiempo, permitiendo a las personas que usen esta aplicación encontrar nueva música que se adecúe al género o estilo de música que deseen escuchar. 

2 

## **3. Descripción de la aplicación** 

A partir de todo lo expresado anteriormente, QuonMusic es una aplicación que recomendará música a sus usuarios según los gustos de este, tanto como gustos generales (géneros) hasta los gustos más específicos de cada uno (artistas y canciones). 

Esta aplicación está orientada a personas que les gusta la música y están buscando ampliar su repertorio de canciones en busca de algo nuevo, en el momento de iniciar la aplicación el usuario tendrá en su pantalla un menú de inicio de sesión para que este pueda registrarse o iniciar sesión si ya había usado la aplicación anteriormente, además de definir sus gustos musicales para que el programa pueda comenzar a trabajar. Posteriormente existirán variados menús en que el usuario tendrá la posibilidad de revisar todas las canciones existentes en la base de datos, revisar sus listas de canciones/géneros/artistas favoritas o utilizar la función de recomendar música. 

## **3.1. Funciones menú inicio de sesión** 

- Registrarse: En el registro se le pedirá al usuario un nombre único, una contraseña e ingresar sus géneros musicales y artistas preferidos, se pedirán dos de cada uno. 

- Iniciar sesión: En el inicio de sesión el usuario ingresará su nombre y contraseña anteriormente creados en el registro. 

- Salir: Se cierra la aplicación de forma segura. 

## **3.2. Funciones menú principal** 

- Explorar canciones: Esta opción mostrará la base de datos de canciones alfabéticamente. Se despliega un submenú en la cual el usuario podrá agregar cualquiera de estas canciones a su lista de favoritos o retroceder hacia el menú principal. 

- Recomendaciones: Se despliega un submenú donde el usuario deberá seleccionar una opción para recibir recomendaciones. A continuación, se tendrán tres opciones a elegir. 

   - Según tus gustos: En este submenú se tomarán en cuenta los géneros o artistas que haya seleccionado el usuario al momento de registrarse y los que ha agregado posteriormente. 

      1. Artistas favoritos: Esta opción recomendará artistas que estén relacionadas con los géneros de los artistas que el usuario tenga ingresado en su lista de artistas favoritos. 

      2. Géneros favoritos: Esta opción recomendará canciones que estén relacionadas con los géneros que el usuario tenga en su lista de géneros favoritos. 

3 

   - Tú escoges: En este submenú se pedirá que el usuario ingrese un artista o un género para recomendar canciones. 

      1. Un género de música escogido: En esta opción el usuario ingresará un género de música y la aplicación mostrará las canciones con ese género musical. 

      2. Un artista escogido: En esta opción el usuario ingresará un artista presente en la base de datos de la aplicación y está entregará las canciones del artista. 

   - TOP: En esta opción se tomarán en cuenta las canciones más agregadas a favoritos de los usuarios y las mostrará de mayor a menor en un TOP 10. 

- Ver mis Canciones: Acá se muestran todas las canciones dentro de la lista canciones favoritas, seguidamente el usuario tendrá la posibilidad de agregar una canción a su lista de favoritos o eliminar una canción que ya esté en su lista. 

- Ver mis Artistas: Acá se muestran todos los artistas dentro de la lista artistas favoritos, seguidamente el usuario tendrá la posibilidad de agregar un artista a su lista de favoritos o eliminar una artista que ya esté en su lista. 

- Ver mis Géneros: Acá se muestran todos los géneros dentro de la lista géneros favoritos, seguidamente el usuario tendrá la posibilidad de agregar un género a su lista de favoritos o eliminar un género que ya esté en su lista. 

- Cerrar sesión: El usuario tendrá la posibilidad de “desloguearse” de la aplicación, volviendo así al menú inicio de sesión mencionado anteriormente. 

- Salir: Se cierra la aplicación de forma segura. 

La aplicación no puede hacer: 

- Una lista de reproducción, solo recomienda canciones, artistas y/o géneros musicales. 

- No puedes agregar canciones, artistas y/o géneros a la base de datos. 

- No se puede reproducir música. 

4 

## **4. Descripción de la solución** 

En la siguiente sección se verán las estructuras de datos utilizadas, los TDA seleccionados, como también las funcionalidades del programa explicadas más a detalle. 

## **4.1. Descripción de tipos de datos** 

## **4.1.1. Estructura usuario** 

La estructura de usuario es una de las partes más importantes de las estructuras, ya que aquí se guardarán los datos de cada usuario, tales como, su nombre de usuario, su contraseña (con la que puede iniciar sesión), lista de canciones favoritas, lista de artistas favoritos y lista de géneros favoritos. Con todas estas listas se podrá diferenciar los gustos del usuario. 

Figura 1: Estructura usuario 

## **4.1.2. Estructura canción** 

La estructura canción es de las estructuras más importantes en la realización de este proyecto, en esta estructura se guardarán datos como el id de la canción, el nombre, el artista principal de la canción, su género, su subgénero y un puntaje que variará entre las veces que se haya agregado o quitado a la lista de favoritos del usuario. 

Figura 2: Estructura canción 

5 

## **4.1.3. Estructura artista** 

La estructura artista guardará datos fundamentales del artista que se necesitarán para implementar la aplicación, cuenta con dos variables char correspondientes a género y subgénero, además de una lista de canciones pertenecientes al artista. 

Figura 3: Estructura artista 

## **4.1.4. Estructura género** 

La última estructura creada es la de géneros, esta contará con una variable char en donde se guardará el nombre del género, y una lista de canciones en donde se almacenarán las canciones correspondientes a su género. 

Figura 4: Estructura género 

6 

## **4.2. Detalles de los TDA** 

## **4.2.1. TDA Lista enlazada doble** 

- Lista de canciones favoritas: Cada usuario tendrá una lista de canciones la cual almacenará las canciones que haya agregado para que, cuando se requiera, el usuario pueda ver su lista de canciones y también para cuando se necesite recomendar canciones. 

- Lista de artistas favoritos: Cada usuario tendrá una lista de artistas la cual almacenará los artistas que haya agregado el usuario. 

- Lista de géneros favoritos: Cada usuario tendrá una lista de géneros la cual almacenará los géneros que haya agregado el usuario. 

- Lista de canciones artista: Es una lista en donde se almacenarán las canciones respectivas a un artista para luego guardar en tipo de dato artista. 

## **4.2.2. TDA Mapa** 

- Mapa usuarios: Es un mapa en donde se almacenarán los datos de los usuarios existentes en la aplicación. Para este TDA se usará una tabla hash que utilizará como key el Nombre de usuario. 

- Mapa canciones: Es un mapa en donde se almacenarán los datos de las canciones existentes en la base de datos. Para este TDA se usará una tabla hash que utilizará como key el id de la canción. 

- Mapa artistas: Es un mapa en donde se almacenarán los datos de los artistas existentes en la base de datos. Para este TDA se usará una tabla hash que utilizará como key el nombre del artista. 

- Mapa géneros: Es un mapa en donde se almacenarán los datos de los géneros que hay en la base de datos. Para este TDA se usará una tabla hash que utilizará como key el nombre del género. 

## **4.2.3. TDA Árbol binario** 

- Árbol top 10: Es un árbol binario en donde se almacenarán todas las canciones de la base de datos usando como key al puntaje, para así poder ordenarlas de mayor puntaje a menor puntaje, dando como resultado un top 10. 

- Árbol canciones: Es un árbol binario en donde se almacenarán todas las canciones de la base de datos usando como key el nombre de la canción, de esta manera podemos ordenarlas de manera alfabética. 

7 

## **4.3. Implementación de las funcionalidades** 

- Registro de usuario: Se leen los datos que se le piden al usuario, un nombre de usuario (único), una contraseña alfanumérica, sus dos géneros musicales favoritos y sus dos artistas favoritos. Todo esto quedará guardado en un archivo.txt para ingresos futuros. 

- Ingreso de usuario: Se leen los datos que se le piden al usuario, el nombre de usuario y su contraseña y se comparan con los que tenemos en el mapa usuarios, en caso de no existir se le notificará que su usuario no existe y en caso de ingresar la contraseña incorrectamente se le pedirá ingresar sus datos nuevamente. En caso de introducir sus datos correctamente se les dará acceso a las funciones del programa. 

- Explorar canciones: Esta función despliega un submenú donde el usuario podrá seleccionar si quiere ver la lista de canciones de la base datos según artista (para lo cual se mostrará el contenido del mapa artistas) o según el nombre de la canción (para lo cual se mostrará el contenido del mapa canciones). Luego, el usuario podrá seleccionar una canción para agregarla a su lista de canciones favoritas, en caso de ya tener esta canción en su lista de favoritos no se podrá agregar dos veces (los géneros de la canción se almacenarán en la lista de géneros favoritos del usuario en caso de no estar) (cada vez que un usuario añada una canción a sus favoritos, se le sumará puntaje a la canción). 

Recomendaciones: En esta función se despliegan 3 opciones de recomendación. 

- Recomendación según gustos: En esta función despliega 2 opciones entre las cuales deberá elegir el usuario: la primera opción recomendará artistas según los artistas que tenga agregados el usuario, se buscará en el mapa de artistas cuáles comparten géneros con los artistas que ya tiene agregados y serán mostrados por pantalla para que el usuario pueda agregarlas a sus favoritos si lo desea. La segunda opción recomendará canciones que tengan el mismo género de las que le gustan al usuario, la cual buscará esas coincidencias en el mapa de canciones y las mostrará para que el usuario pueda agregarlas a sus favoritos si lo desea. 

- Recomendación según el artista o género seleccionado: En esta función se desplegarán dos opciones: la primera opción desplegará una lista de los géneros de música que tenemos en el mapa de géneros, entre las cuales el usuario deberá escoger un género y se desplegará una lista de canciones que coinciden con ese género para que el usuario pueda agregarlas a sus favoritos si lo desea. La segunda opción desplegará una lista con todos los artistas que hay en el mapa de artistas y el usuario deberá escoger uno de los que se le muestran para luego mostrar canciones que compartan el mismo género que tiene el artista para que el usuario pueda agregarlas a sus favoritos si lo desea. 

- Recomendaciones según el TOP: Esta función buscará en el mapa de canciones las 10 canciones con mayor puntaje y se mostrarán por pantalla para que el usuario pueda agregarlas a sus favoritos si lo desea. 

8 

- Ver mis Canciones: Se buscará en el mapa usuarios el usuario que está usando la sesión activa y se ingresará a su lista de canciones favoritas, para mostrarlas por pantalla, desplegando un submenú con dos opciones. 

   1. Agregar: Se mostrarán todas las canciones favoritas del usuario, para que posteriormente se pueda seleccionar la canción que quiera agregar a través del id de esta, se añadirá a su lista de canciones favoritas. 

   2. Quitar: Se mostrarán todas las canciones de la lista de favoritos y se pedirá que ingrese el nombre de la canción a la cual eliminar. 

- Ver mis Artistas: Se buscará en el mapa usuarios el usuario que está usando la sesión activa y se ingresará a su lista de artistas favoritos, para mostrarlos por pantalla, desplegando un submenú con dos opciones. 

   1. Agregar: Se mostrarán todos los artistas y el usuario podrá seleccionar el artista que quiera agregar y a través del nombre se añadirá a su lista de canciones favoritas. 

   2. Quitar: Se mostrarán todos los artistas de la lista y se pedirá que ingrese el nombre del artista que quiera eliminar de la lista. 

- Ver mis Géneros: A partir del usuario que haya iniciado sesión actualmente, se buscará en el mapa usuarios la lista de géneros favoritos para mostrarlas por pantalla. Posteriormente se desplegará un submenú con dos opciones para que el usuario pueda modificar su lista de géneros. 

   1. Agregar: Se mostrarán todos los géneros y el usuario podrá seleccionar el género que quiera agregar y a través del nombre se añadirá a su lista de canciones favoritas. 

   2. Quitar: Se mostrarán todos los géneros de la lista y se pedirá que ingrese el nombre del género que quiera eliminar de la lista. 

- Cerrar sesión: Con esta opción el usuario podrá desloguearse de la aplicación, se limpiarán las variables que hayan almacenado el inicio de sesión y será redirigido al menú principal. 

- Salir: Con esta opción el usuario podrá salir del programa, se cerrará la ventana de la aplicación. 

9 

## **5.** 

A continuación, se muestra la planificación realizada por todos los integrantes del grupo en donde las principales tareas están divididas en tres puntos, el primer punto es previo al informe, el segundo es el desarrollo del informe y por último el desarrollo del software. Cada uno de estos puntos tendrá una fecha estipulada y en general todas las actividades serán llevadas a cabo desde el día cinco de junio hasta el seis de julio. 

Figura 5: Carta Gantt 

10 

## **6. Conclusión** 

En el presente proyecto se elaboró una aplicación dedicada a la recomendación de artistas y canciones en base a los gustos específicos de cada usuario, esta aplicación cumple de forma eficiente el objetivo principal planteado, permitiendo al usuario, al momento de registrarse, escoger los primeros gustos en artistas y géneros para que posteriormente esta información sea usada correctamente por la aplicación y así aguzar el procedimiento de recomendación de esta. Además, esta aplicación satisface la necesidad de expandir los gustos musicales de cada persona gracias a la amplia lista de artistas y canciones incluidas en la base de datos, la cual contiene más de 40 géneros y 250 canciones que fueron seleccionadas en base a su popularidad histórica desde los años 50’ hasta la actualidad. 

Durante el avance del proyecto el principal problema fue el tiempo que se estimó para el desarrollo de cada una de las partes de la aplicación, ya que estas tomaban más tiempo del que se creía necesario para implementarlas. Por otra parte, la falta de experiencia en la programación por parte del equipo de trabajo significó el atraso de cada actividad a realizar en función del tiempo estimado. Sin embargo, la participación de todos los integrantes del grupo permitió que el proyecto haya sido realizado satisfactoriamente según los tiempos finales establecidos. 

En definitiva, la realización de este proyecto ha requerido gran parte de la información aprendida en el curso, como la implementación de árboles binarios para ordenamiento, mapas para almacenar datos, la lectura de archivos CSV para la base de datos, entre otras. Si bien a este proyecto le faltan varias mejoras que se esperan lleguen en un futuro, todas las herramientas mencionadas anteriormente han sido de utilidad para cumplir los objetivos establecidos en un principio y así el funcionamiento total de la aplicación. 

11 

## **7. Coevaluación** 

En general, el desempeño del grupo de trabajo en este proyecto fue muy bueno, todos los integrantes participaron de manera equitativa y fueron responsables al entregar sus partes, el único punto negativo a destacar fue la cantidad de tiempo que pensamos que tomaría cada parte del proyecto, lo que nos retrasó, sin embargo, todos cumplieron con los plazos de entrega. El aspecto a mejorar es principalmente definir de manera más precisa las estructuras y funciones a desarrollar, para así facilitar y agilizar el trabajo en futuros trabajos. 

## Aspectos positivos 

Pablo Ortiz: Facilidad para encontrar las soluciones a la hora de crear funciones. Jefté Ponce: Reconoce con facilidad los errores y los soluciona(debuger). Iván Galaz: Síntesis y cohesión de las ideas del equipo. 

Darien Pacheco: Buen trabajo de investigación y recopilación de información para la base de datos. 

## Aspectos a mejorar 

Pablo Ortiz: Comunicar con anterioridad los problemas para no retrasar el trabajo. Jefté Ponce: Falta responsabilidad a la hora de conectarse para trabajar, y poco conocimiento de listas enlazadas y árboles binarios. 

Iván Galaz: Preocuparse más por el desarrollo del proyecto en general y no dejar todo para el final. 

Darien Pacheco: Profundizar de mejor manera la materia de árboles binarios para aumentar la eficacia de ciertas funciones. 

12 

