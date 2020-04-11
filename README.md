
# Willy*


[TOCM]
#H1 ¿Qué es?
#H2 ¿Cómo correrlo?
#H3 Versiones
##H4 Versión 2.1
##H5 Versión 2.0
##H6 Versión 1.0
#H3 Sobre la implementació

# ¿Qué es?

Willy **es un interpretador del lenguaje Willy***, que determina un ambiente de programación para un robot.

:robot: Este puede interactuar con objetos en un mundo y desplazarse por el mismo a través de cuadrículas de tamaño finito.

Para más detalles del lenguaje Willy > [willy.pdf](https://github.com/MaferMazu/Willy/blob/Parser/willy.pdf)

Este interpretador se hizo como proyecto para la materia de Traductores de la Universidad Simón Bolívar, el trimestre Ene-Mar de 2020

Y fue desarrollado por:
:boy: @jcellomarcano 
:girl:  @mafermazu

# ¿Cómo correrlo? 

1. Descargar el repositorio

2. Entrar en la terminal del sistema en la dirección del repositorio y realizar en la línea de comandos:

  `$ ./makefile` 

3. Luego se puede ejecutar el programa Willy, usando:

  `$ willy <nombredearchivoexistente>`

o

  `$ willy `

# Versiones
### Versión 2.1
05/04/2020 04:35

Se descubrió que falta resolver en la recursión lo que debe hacer el método de ejecución con los nodos intermedios a las producciones principales de instrucciones.

### Versión 2.0
05/04/2020 04:00

Actualizaciones:
- Se implementaron más archivos de prueba.
- Se realizó el árbol con las instrucciones para ser ejecutadas.
- Se acomodaron varios errores.

Falta: revisar porqué en parser al hacerle un método a un nodo en particular este no responde. (línea 548 en myparser.py)

### Versión 1.0
03/04/2020 23:50

El proyecto no se encuentra terminado en su totalidad, sin embargo esta implementado:

- El lexer.
- El parser con sus correspondientes validaciones.
- La tabla de símbolos.
- Las clases World y Task para la implementación.

Por terminar:
Hacer las instancias correspondientes del mundo para hacer la correcta ejecución del programa Willy.

# Sobre la implementación

Este proyecto se dividió en 3 etapas:

En la primera fase del proyecto se implementó el análisis lexicográfico, el cual consiste en reconocer una entrada y dividirla en pequeños pedazos llamados tokens. 

Para realizar el análisis lexicográfico se utilizó una herramienta de construcción de lexer y parser llamada PLY.

La segunda etapa consistió en implementar un módulo sintáctico que utilice el módulo lexicográfico de la primera entrega. Este analizador debe aceptar o rechazar un programa dependiendo de si la entrada pertenece o no al lenguaje Willy*, que es el que utiliza nuestro robot para transitar en los mundos definidos en ese mismo lenguaje.

Y la última entrega se concentraba en terminar el interpretador del lenguaje y el simulador para que se realizara correctamente la ejecución del programa.

## Sobre el Lexer

Primero se definió una lista de palabras reservadas y una lista de tokens, que son las que se consideraron convenientes para los requerimientos del problema. 


Luego se definieron los tokens ignorados.

Muchas de las definiciones de tokens se hicieron con ayuda de las expresiones regulares, que nos permitían agrupar las cadenas de texto que se necesitaban.


También se implementaron dos listas, una de tokens válidos y otra de no válidos, para llevar un control de los tokens que se van formando a medida que se va leyendo el archivo inicial del programa, y de haber existencia de tokens no válidos puedan ser redirigidos a un manejador de errores.

El manejador de errores es importante porque en este lenguaje puede que hayan símbolos que no existan, y hay que manejarlos. Para ello se almacenó información pertinente de los tokens como la columna y línea donde se manifiesta el error.

Si el arreglo de tokens inválidos tiene algún elemento se muestra dicho error en pantalla y termina la ejecución.

## Sobre el Parser

Para la implementación del Parser primero se tuvo que entender cómo funciona el constructor de sintaxis que provee PLY, este se denomina yacc, y toma un conjunto de definiciones y las convierte en la gramática de nuestro lenguaje. La forma que tienen las definiciones presentes en este módulo se asemejan a las vistas en clase de Traductores.

El diseño de esta gramática comprende la forma en que se determina si un programa es correcto o no en el mundo de Willy. Para ello se utilizaron las especificaciones del mundo, y se buscó generalizar reglas que permitan que con símbolos terminales (los tokens obtenidos de la etapa del lexer) y los no terminales representados por las definiciones en el parser se pueda determinar la forma que van a tener las instrucciones dentro de Willy*. 

## Sobre el Interpretador

Inicialmente se creó una **pila de símbolos** en donde se almacenan los distintos identificadores (ids) que son utilizados para cada mundo, tarea, variable booleana, nombre de función, objeto, etc. Esto con el objetivo de mantener un control de identificadores, y verificar que se utilicen correctamente; por ejemplo, no instanciar objetos que no fueron previamente definidos, o no definir dos funciones con el mismo nombre, incluso verificar que no existan dos mundos con el mismo nombre.

Con respecto a la ejecución del programa se puede dividir en dos partes:

### Interpretar los mundos

Se creó una clase mundo con ciertos métodos y a partir del parser estos métodos fueron invocados para así tener registradas las caricterísticas del mismo y poder mostrarlo.

Para esta etapa se crearon también algunos controladores en el parser para asegurar que la asignación de atributos del mundo esten correctas. Por ejemplo, detectar si se tiene un mundo de tamaño 1x1, no construir paredes en la columna 3.

### Interpretar las tareas 

Se aprovechó la estructura del parser para crear nodos (estructuras que tienen un tipo e hijos), para que al ejecutar el parser la creación de nodos se fuera creando recursivamente para así obtener una estructura de árbol con todas las instrucciones, similar a un árbol de derivación.

A partir de esta estructura se crearon varios métodos para manejar los nodos. Y los más importantes son:

finalGoalValue(): Para saber el valor booleano del final goal definido para cada mundo.

boolValue(): Para saber el valor booleano de las condiciones creadas en la tarea.

executeMyTask(): Quién es la función responsable de que se ejecuten todas las instrucciones de forma correcta dentro de Willy*.

# Archivos de Prueba

### PickStart.txt

:robot: :speech_balloon: :star: :dart:

PickStart en un programa en lenguaje Willy que consta de un mundo llamado sky con dimensiones 8 x 9 con estrellas.

El objetivo es que Willy logre llegar a la posición final con 3 estrellas en su cesta.

### WillyCleanItsRoom.txt

:running_shirt_with_sash: :jeans: :closed_book: :computer:

Este es un programa que tiene un mundo llamado room con dimensiones 4 x 5 que representa el cuarto de una persona.

El objetivo de este es que Willy recoja su cuarto colocando su celular, su laptop y los libros en su mesa de trabajo (en donde está inicialmente su laptop) y que coloque toda la ropa sucia en la cesta de la ropa sucia.

# Conclusión

Para desarrollar un interpretador correctamente es importante realizarlo paso a paso. Primero definir cuáles van a ser las palabras que formaran parte del lenguaje, luego definir la estructura sintáctica que tendrán las instrucciones, para luego de haber verificado eso se pueda implementar la ejecución de un programa escrito en ese lenguaje.

Para Willy se necesitaron estructuras como la pila de símbolos porque en el mundo se podían definir variables y funciones, y se necesitaba tener un control de eso.

Otra estructura importante que se utilizó fue la del árbol que es la responsable de que la ejecución de las tareas pueda realizarse de forma correcta. Sin embargo este no se puede crear de forma correcta si no se tiene una buena gramática (que no sea ambigua ) que cree la estructura.

Para finalizar es importante comentar que esto fue posible gracias a dividir la tarea de crear el interpretador en pequeñas etapas e ir resolviendo cada una de ellas para así lograr el resultado final y darle vida a Willy.

:robot: :speech_balloon: *- Hello, World! -* 
