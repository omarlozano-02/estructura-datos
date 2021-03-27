import sys
import time
#funcion que imprime el menú
def imprimirMenu():
    print("Elige Una opción\n1-Registrar Venta\n2-Consultar Venta\n3-Salir")
#separador
SEPARACION = 15*"-"
#diccionario que contendrá las ventas
ventas = {}
#iniciamos ciclo 
while True:
    #lista para almacenar los articulos(detalle,cantidad y precio total)
    venta = []
    #imprimimos menu
    imprimirMenu()
    opcion = input()    #entrada de la opcion elegida
    if opcion=="1":
        #se abre menú de ventas
        print(f"{SEPARACION}Menú de Ventas{SEPARACION}")
        while True: #bucle menú de ventas
            print("1 para añadir artículo - 2 para cerrar venta")
            eleccion = input()
            if eleccion=="1":
                print("Descripcion del artículo")
                _descripcion = input()#entrada articulo
                while True:

                    print("Cantidad de articulos")
                    try:
                        _cantidad_piezas = int(input())#entrada cantidad
                    except:
                        print("Valor introducido no es correcto, Intente de nuevo.")
                    else:
                        break
                while True:

                    print("Precio unitario")
                    try:
                        _precio_unitario = int(input())#entrada precio unitario
                    except:
                        print("Valor introducido no es correcto, Intente de nuevo.")
                    else:
                        break
                _precio_total = _cantidad_piezas*_precio_unitario #calculamos el importe subtotal
                venta.append((_descripcion,_cantidad_piezas,_precio_total))#añadimos la venta a memoria con ayuda del diccionario -venta-
                print("Articulo añadido.")
            elif eleccion=="2":
                #cerramos la venta 
                importe_total = 0  #inicializamos variable para almacenar el importe total
                if len(venta)>0: #si la lista ventas es mayor a 0, quiere decir que hay ventas por lo tanto se puede procesar la venta
                    for i in venta: #recorremos cada venta 
                        importe_total = importe_total + i[2]#extraemos su precio subtotal 
                    print(f"El importe total a pagar es de ${importe_total}")
                    print("1 para cobrar y finalizar - 2 para cancelar venta")
                    finalizar= input() #entrada para ver si se finalizará o cancelará la venta
                    if finalizar == "1": #finalizamos la venta cobrandola
                        ventas[f'Venta {len(ventas)+1}']={"Detalles":venta,"Importe_Total":importe_total}#almacenamos venta en diccionario ventas
                        del venta #eliminamos de memoria principal la lista venta
                        print("Venta Finalizada.")
                        break #terminamos con el ciclo del menú de ventas

                    elif finalizar == "2": #cancelamos venta
                        print("Venta cancelada")
                        break #terminamos con el ciclo del menú de ventas
                    else:
                        print("Opcion no existe.")
                else:
                    print("Ningun artículo añadido.") 
                    break
            else:
                print("Opcion no existe.")
    elif opcion=="2":
        #menu para consulatr ventas
        if len(ventas)>0: #si hay ventas entonces entramos al menú
            print(f"{SEPARACION}Menú de Consulta{SEPARACION}")
            print("Escoja un numero de venta para ver los detalles")
            #imprimimos las ventas
            for i in ventas:
                print(i,"\tImporte Total: $",ventas[i]['Importe_Total'])
            while True:
                try:
                    _venta = int(input())
                except:
                    print("Valor introducido no es correcto.")
                else:
                    break
            if _venta > len(ventas) or _venta <= 0:
                print("Venta no existente")
            else:
                _contador = 0 #contador para saber en que parte del diccionario estamos
                #print(ventas[f"Venta {_venta}"])
                for i in ventas[f"Venta {_venta}"]:
                    if _contador == 0:#condicional para darnos cuenta si el ciclo esta en la seccion de detalle
                        print("Artículo\tCantidad\tSub Total")
                        for y in ventas[f"Venta {_venta}"][i]: #si esta entonces esa sección del diccionario recorremos la lista
                            for z in y: #y por consiguiente recorremos la tupla
                                print(z,end="\t\t")#imprimimos los elementos de la tupla
                            print("")
                        _contador += 1 #añadimos uno al contador ya que pasa por aquí
                    else:
                        print("\nImporte Total:",ventas[f"Venta {_venta}"][i])#imprimimos el importe ttal
        else:
            print("No hay ventas registradas")
    #opcion para salir del programa
    elif opcion=="3":
        print("Saliendo del programa...")
        time.sleep(2)
        sys.exit()
    #si no se ingreso una opcion correcta entonces será tomada como opción no válida
    else:
        print("Opcion no válida")