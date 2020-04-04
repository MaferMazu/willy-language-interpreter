
# Willy*

Willy* es un proyecto que consiste en la implementación de un ambiente de programación para un robot de nombre Willy.

Este robot puede interactuar con objetos en un mundo y desplazarse por el mismo a través de cuadrículas de tamaño finito.

# Cómo correr el programa

Se realiza la en la línea de comandos:
./makefile

y luego se puede ejecutar el programa Willy, usando:


willy [nombredearchivoexistente]
  
o con willy exclusivamente. (Luego se le pedira ingresar el txt)

# Estado Actual del Programa
03/04/2020 23:50

El proyecto no se encuentra terminado en su totalidad, sin embargo esta implementado:

- El lexer.
- El parser con sus correspondientes validaciones.
- La tabla de símbolos.
- Las clases World y Task para la implementación.

Por terminar:
Hacer las instancias correspondientes del mundo para hacer la correcta ejecución del programa Willy.

# Sobre el proyecto:

La implementación de este programa se dividió en 3 etapas:

En la primera fase del proyecto se implementó el análisis lexicográfico, el cual consiste en reconocer una entrada y dividirla en pequeños pedacitos que llamaremos tokens. Estos luego serán utilizados para crear el análisis sintáctico, que sería nuestro siguiente paso.

Para realizar el análisis lexicográfico se utilizó una herramienta de construcción de lexer y parser llamada PLY.

La segunda etapa consistió en implementar un módulo sintáctico que utilice el módulo lexicográfico de la primera entrega. Este analizador debe aceptar o rechazar un programa dependiendo de si la entrada pertenece o no al lenguaje Willy*, que es el que utiliza nuestro robot para transitar en los mundos definidos en ese mismo lenguaje.

Y por último en la tercera entrega se concentraba en terminar el interpretador del lenguaje y el simulador para que se realizara correctamente la ejecución del programa.

## Sobre el Lexer

Primero se realizó una lista de tokens, que son los que se consideraron convenientes para los requerimientos del problema. Esta posee los nombres que se usarán posteriormente para identificar las palabras o grupos de palabras que queremos agrupar y dividir, y así empezar a interpretar todo lo que nos provee la entrada al software.

También se tiene una lista de palabras reservadas (tokens), que es añadida posteriormente en la lista inicial de tokens.

Luego se definieron los tokens ignorados, esto y muchas de las definiciones de tokens se hicieron con ayuda de las expresiones regulares, que nos permitían agrupar lo que necesitaramos.

Se tienen dos listas, una de Tokens válidos y otra de no válidos, para llevar un control de los tokens que se van formando a medida que se va leyendo el programa.

El manejador de errores es importante porque en este lenguaje puede que hayan símbolos que no existan, y es importante que como implementador se le notifique al usuario que quiere realizar alguna prueba, la columna y línea donde se manifiesta el error.

Las siguientes instrucciones fueron para construir el lexer con PLY, verificar las longitudes de entradas del prompt, leer el archivo de entrada que nuestro analizador lexicográfico va a procesar y hacer las consideraciones pertinentes para que el formato de salida del programa sea el especificado.

Si el arreglo de tokens inválidos tiene algún elemento se muestra dicho error en pantalla y termina la ejecución.

## Sobre el Parser

Para la implementación del Parser primero se tuvo que entender cómo funciona el constructor de sintaxis que provee PLY, este se denomina yacc, y toma un conjunto de definiciones y las convierte en la gramática de nuestro lenguaje. De hecho, la forma que tienen las definiciones presentes en este módulo se asemejan a las vistas en clase de Traductores.

El diseño de esta gramática comprende la forma en que se determina si un programa es correcto o no en el mundo de Willy*. Para ello se utilizaron las especificaciones del mundo, y se buscó generalizar reglas que permitan que con símbolos terminales (los tokens obtenidos del módulo 1) y los no terminales representados por las definiciones en el parser (myparser.py), que son quienes generan las producciones correspondientes.

La gramática consta de varios elementos: las variables (que vienen a ser las definiciones que se crearon para que el constructor del parser funcionara), los símbolos terminales que son los tokens, las reglas de producción que también están especificadas en el archivo myparser.py y el símbolo inicial que es representado por “program”. 

## Sobre el Interpretador



# Conclusión

Para desarrollar un interpretador es importante usar la estrategia de dividir y vencer.

Dividiendo la entrada con el programa en tokens y almacenar información pertinente sobre la línea en la que se encuentra o la columna ayudará a que luego podamos darle estructura al lenguaje que se está leyendo y así lograr entender e implementar de forma correcta el funcionamiento del programa de entrada.

Un paso a la vez.

Para la siguiente etapa se aseguró de que la estructura de las instrucciones fueran las indicadas, y que el programa de Willy no pueda ser ejecutado si existe alguna instrucción con errores de sintaxis.

Además se creo una tabla de símbolos que permite llevar el control de las variables del mundo.

Finalmente se crearon estructuras como World y Task que proveen distintas funciones para implementar y ejecutar los programas en lenguaje Willy.

De esta forma se fueron realizando paso a paso todos los procedimientos para crear un interpretador de lenguaje y darle vida a Willy.
