import os
from datetime import datetime
import sys
import csv
import time
def imprimirMenu():
    return input("Elige una opción\n1-Registrar Venta\n2-Consultar Venta\n3-Reporte\n4-Salir\n")
def leer(archivo):
    with open(archivo) as File:
        reader = csv.reader(File, delimiter=',')
        ventas=(list(reader))
        return ventas
def crear_archivo(archivo,headers):
    myFile = open(archivo, 'w',newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(headers)
def escribir(archivo,datos):
    myFile = open(archivo, 'a',newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(datos)
#separador
SEPARADOR = 15*"-"
#nombre archivo
archivo = 'ventas.csv'
fecha = ""
#iniciamos ciclo 
while True:
    #lista para almacenar los articulos(no venta,detalle,cantidad y precio total)
    transaccion = []
    #imprimimos menu
    respuesta = imprimirMenu()    #entrada de la opcion elegida
    if respuesta=="1":
        #condicional para ver si existe el csv
        if not os.path.exists(archivo):
            #si no existe este bloque de codigo crea el csv
            encabezados = [['Venta','Fecha','Desc.','Q','PU']]
            crear_archivo(archivo,encabezados)
            #definimos el numero de venta
            n_venta=1
        else:
                #llamado de funcion para leer csv
                ventas=leer(archivo)
                ultima_venta = ventas[-1][0]
                #obtenemos el numero de venta
                if ultima_venta=="No. Venta":
                    n_venta = 1
                else:
                    n_venta = int(ultima_venta)+1
        #se abre menú de ventas
        print(f"{SEPARADOR}Menú de Ventas{SEPARADOR}")
        while True: #bucle menú de ventas
            accion = input("1 para añadir artículo - 2 para cerrar venta\n")
            if accion=="1":
                while True:
                	if fecha !="":
                	    break
                	try:
                		print('Fecha')
                		respuesta = int(input('1-Actual 2-Introducir Fecha'))
                	except:
                		print('Opcion no valida')
                	else: 
                		if respuesta == 1:
                			fecha = datetime.now()
                			fecha= fecha.date()
                			break
                		else:
                			while True:
                				try:
                					dia = int(input('Dia:\n'))
                				except:
                					print('Valor introducido no valido')
                				else:
                					if dia in range(1,32):
                						dia=str(dia)
                						if len(dia)==1:
                							
                							dia =f'0{dia}'
                						break
                			while True:
                				try:
                					print('Mes:\n')
                					mes = int(input())
                				except:
                					print('Valor introducido no valido')
                				else:
                					if mes in range(1,13):
                						mes=str(mes)
                						if len(mes)==1:
                							mes=f'0{mes}'
                						break
                			while True:
                				try:
                					print('Año:\n')
                					anio = int(input())
                				except:
                					print('Valor introducido no valido')
                				else:
                					fecha = datetime.now()
                					anio_actual = fecha.year
                					
                					if anio in range(1901,anio_actual+1):
                						fecha=f'{anio}-{mes}-{dia}'	
                						break
                			break			
                desc = input("Descripcion:\n")#entrada articulo
                while True:
                    try:
                        q_piezas = int(input("Cantidad de articulos:\n"))#entrada cantidad
                    except:
                        print("Valor introducido no es correcto, Intente de nuevo.")
                    else:
                        break
                while True:
                    try:
                        p_uni = int(input("Precio unitario del producto:\n"))#entrada precio unitario
                    except:
                        print("Valor introducido no es correcto, Intente de nuevo.")
                    else:
                        break
                p_total = q_piezas*p_uni #calculamos el importe subtotal
                transaccion.append((n_venta,fecha,desc,q_piezas,p_total))#añadimos la venta a memoria con ayuda del diccionario -venta-
                print("Articulo añadido.")
            elif accion=="2":
                #cerramos la venta 
                importe_total = 0  #inicializamos variable para almacenar el importe total
                if len(transaccion)>0: #si la lista ventas es mayor a 0, quiere decir que hay ventas por lo tanto se puede procesar la venta
                    for i in transaccion: #recorremos cada venta 
                        importe_total = importe_total + i[4]#extraemos su precio 
                    print(f"Total : ${importe_total}")

                    finalizar= input("1 Cobrar y Finalizar - 2 Cancelar venta\n") 
                    if finalizar == "1": #finalizamos la venta cobrandola                        
                        
                        escribir(archivo,transaccion)
                        for i in transaccion:
                            print(i)

                        del transaccion
                        fecha = ""
                        print("Venta Finalizada.")
                        break
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
    elif respuesta=="2":
        if  os.path.exists(archivo):
            ventas = leer(archivo) 
        else:
            ventas=[]
        #menu para consultar ventas
        if len(ventas)>1: #si hay ventas entonces entramos al menú
            print(f"{SEPARADOR}Menú de Consulta{SEPARADOR}")
            while True:
                try:
                    venta = int(input("Introduce el numero de venta o presiona 0 Volver\n"))
                except:
                    print("Valor introducido no es correcto.")
                else:
                    if venta > len(ventas) or venta <= 0:
                        if venta>len(ventas):
                        	print("Venta no existente")
                        elif venta ==0:
                        	break
                    else:
                    	importe_total=0
                    	print("Venta\tFecha\t\t\tDescripcion\tCantidad\tImporte")
                    	for i in ventas:
                    		if i[0]==str(venta):
                    			print(f"{i[0]}\t\t{i[1]}\t\t{i[2]}\t\t{i[3]}\t\t{i[4]}")			    
                    			importe_total += int(i[4])
                    	print(f"Importe Total: {importe_total}")
        else:
            print("No hay ventas registradas")
    #bloque para obtener un reporte
    elif respuesta=="3":
        if  os.path.exists(archivo):
            ventas = leer(archivo) 
        else:
            ventas=[]
        while True:
            if len(ventas)==0:
                print("No hay ventas registradas")
                break
            else:
                while True:
                    try:
                        respuesta=int(input("1 Introducir Fecha 2 Salir\n"))
                    except:
                        pass
                    else:
                        break
                if respuesta==1:
                        while True:
                            try:
                                dia = int(input('Ingresa el día\n'))
                            except:
                                print('Valor introducido no valido')
                            else:
                                if dia in range(1,32):
                                    dia=str(dia)
                                    if len(dia)==1:
                                        dia =f'0{dia}'
                                    break
                        while True:
                            try:
                                mes = int(input('Ingresa el mes\n'))
                            except:
                                print('Valor introducido no valido')
                            else:
                                if mes in range(1,13):
                                    mes=str(mes)
                                    if len(mes)==1:
                                        mes=f'0{mes}'
                                    break
                        while True:
                            try:
                                anio = int(input('Ingrese el año\n'))
                            except:
                                print('Valor no valido')
                            else:
                                fecha = datetime.now()
                                anio_actual = fecha.year
                                if anio in range(1901,anio_actual+1):
                                    fecha=f'{anio}-{mes}-{dia}'
                                    break
                        print(f"{SEPARADOR}Reporte de Ventas del día {fecha} {SEPARADOR}")
                        print("Venta\t\tFecha\t\t\tDescripcion\tPiezas\t\tTotal")
                        con = 0
                        total = 0
                        for i in ventas:
                            #si la fecha coincide, extramos su detalle
                            if i[1]==fecha:
                                print(f"{i[0]}\t\t{i[1]}\t\t{i[2]}\t\t{i[3]}\t\t{i[4]}")
                                total = total + int(i[4])
                                con += 1
                        if con == 0:
                            print("Sin Ventas")
                        else:
                            print(f"Total de ventas: {total}")
                        print(SEPARADOR)
                        fecha = ""
                elif respuesta==2:
                    break
                else:
                    print("Opcion no valida") 
    #bloque para salir del programa
    elif respuesta=="4":
        print("Saliendo del programa...")
        time.sleep(2)
        sys.exit()
    #bloque -opcion no valida
    else:
        print("Opcion no válida")
