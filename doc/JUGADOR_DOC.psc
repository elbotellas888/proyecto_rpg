Algoritmo sin_titulo
	definir jugador Como Caracter
	definir vida Como Entero
	definir ataque Como Entero
	definir defensa Como Entero
	definir experiencia Como Entero
	definir nivel Como Entero
	vida=300
	ataque=70
	defensa=5
	experiencia=0
	nivel=0
	
	Definir   i    Como Entero
	definir x Como Entero
    x <- 1
    i <- 1
	
    Escribir "Usa W (arriba), A (izquierda), S (abajo), D (derecha) para mover al jugador."
    Escribir "Presiona"  "para salir."
	
    Repetir
        Escribir "Posición actual: (", x, ",", i, ")"
        Escribir "Introduce una tecla: "
        Leer tecla
        
        Segun tecla Hacer
            "W":
                i <- i + 1
                Escribir "Te moviste arriba."
            "A":
                x <- x - 1
                Escribir "Te moviste a la izquierda."
            "S":
                i <- i - 1
                Escribir "Te moviste abajo."
            "D":
                x <- x + 1
                Escribir "Te moviste a la derecha."
            "Q":
                Escribir "¡Has salido del juego!"
                
            De Otro Modo:
                Escribir "Tecla inválida. Usa W, A, S, D o Q."
        FinSegun
		
    Hasta Que tecla = "Q"
	
	
FinAlgoritmo
