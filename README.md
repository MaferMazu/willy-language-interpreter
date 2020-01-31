
# Willy*
Lexer

Este es el inicio de la implementación de un ambiente de programación basado en Willy, un robot que interactúa con objetos en un mundo hecho de cuadrículas de tamaño finito y paredes.

Willy es controlado por un programa que tiene varias definiciones del mundo, y para ello se creó este proyecto.

Este se dividió en etapas:

En esta primera fase del proyecto se implementó el análisis lexicográfico, el cual consiste en reconocer una entrada y dividirla en pequeños pedacitos que llamaremos tokens. Estos luego serán utilizados para crear el análisis sintáctico, que sería nuestro siguiente paso.

Para realizar el análisis lexicográfico se utilizó una herramienta de construcción de lexer y parser llamada PLY.   


# Cómo correr el programa

Se realiza la en la línea de comandos:
./makefile

y luego se puede ejecutar el programa Willy, usando:


willy <nombredearchivoexistente>
  
o con willy exclusivamente. (Luego se le pedira ingresar el txt)

# Sobre el Lexer

Primero se realizó una lista de tokens, que son los que se consideraron convenientes para los requerimientos del problema. Esta posee los nombres que se usarán posteriormente para identificar las palabras o grupos de palabras que queremos agrupar y dividir, y así empezar a interpretar todo lo que nos provee la entrada al software.

También se tiene una lista de palabras reservadas (tokens), que es añadida posteriormente en la lista inicial de tokens.

Luego se definieron los tokens ignorados, esto y muchas de las definiciones de tokens se hicieron con ayuda de las expresiones regulares, que nos permitían agrupar lo que necesitaramos.

Se tienen dos listas, una de Tokens válidos y otra de no válidos, para llevar un control de los tokens que se van formando a medida que se va leyendo el programa.

El manejador de errores es importante porque en este lenguaje puede que hayan símbolos que no existan, y es importante que como implementador se le notifique al usuario que quiere realizar alguna prueba, la columna y línea donde se manifiesta el error.

Las siguientes instrucciones fueron para construir el lexer con PLY, verificar las longitudes de entradas del prompt, leer el archivo de entrada que nuestro analizador lexicográfico va a procesar y hacer las consideraciones pertinentes para que el formato de salida del programa sea el especificado.

Si el arreglo de tokens inválidos tiene algún elemento se muestra dicho error en pantalla y termina la ejecución.

## Conclusión
