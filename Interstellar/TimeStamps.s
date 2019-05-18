.data
	salida: .asciz "%lu"		@ cadena de salida que imprime un long int unsigned. Pone un caracter nulo al final de la cadena.
	size: .zero 8 				@ definir un espacio en memoria de 8 bytes

.text
	.global main

main:
	ldr r9, = size 				@ cargar en el registro 9 la direccion de memoria de size. Equivale a &variable en c
	bl _time_stone 				@ bl es un branch que va a llamar a la funcion
	ldr r1, [r9]				@ obtener el contenido del registro 9. Equivale a *variable en c
	bl escribe

exit:
	mov r7, #1
	mov r0, #0
	svc #0

escribe:
	push {r1-r3, lr}			@ guarda el estado de los registros 1 a 3 en la pila
	ldr r0, = salida
	bl printf
	mov r0, #0
	bl fflush
	pop {r1-r3, pc}				@ el valor que estaba en el registro de lr se va al program counter

_time_stone:
	push {r1-r3, lr}
	mov r7, #78					@ 78 es la lectura de la hora del sistema (unix time)
	ldr r0, = size
	eor r1, r1 					@ lo que esta en el registro 1 lo vuelve 0
	svc #0
	pop {r1-r3, pc} 
