from datetime import datetime
import sys
import time
import sqlite3
def imprimirMenu():
    return input("Elige una opción\n1-Registrar Venta\n2-Consultar Venta\n3-Salir\n")

def conectar(bd):
    try:
        conexion=sqlite3.connect(bd)
    except sqlite3.Error as e:
        print(e)
    else:        
        return conexion

def select_last_folio(conexion,bd):
    cursor = conexion.cursor()
    try:

        cursor.execute(f'SELECT folio FROM ventas ORDER BY folio DESC LIMIT 1;')
    except sqlite3.OperationalError as e:
        last_folio=0
       
    else:
        last_folio = cursor.fetchall()
        if last_folio:
            pass
        else:
            last_folio=1
    finally:
        cursor.close()
       

    return last_folio
def close(conexion):
    try:
        conexion.close()
    except sqlite3.Error as e:
        print(e)
    else:
        pass
    
def crear_tablas(base):
    con =conectar(base)
    cursor = con.cursor()
    try:
        cursor.execute("""CREATE TABLE ventas (
                folio INTEGER PRIMARY KEY,
                fecha DATE NOT NULL,
                total_venta DEFAULT 0
        );""")
        cursor.execute("""CREATE TABLE detalle (
                folio INTEGER,
                desc TEXT NOT NULL,
                piezas INTEGER NOT NULL,
                total_detalle INTEGER DEFAULT 0,
                FOREIGN KEY (folio) REFERENCES ventas(folio)
        );""")

    except sqlite3.OperationalError as e:
        print(str(e))
        return False
    except:
        return False
    else:
        print("Tablas creadas correctamente.")
        return True
    finally:
        cursor.close()
        close(con)

def try_transaction(sql,values,con,cursor):
    try:
        cursor.execute(sql,values)
        con.commit()
    except sqlite3.OperationalError as e:
        print(e)
    else:
        pass
    finally:
        cursor.close()
        close(con)

def insertar_venta(folio,fecha):
    values = {'folio':folio,"fecha":fecha}
    sql = "INSERT INTO ventas (folio,fecha) VALUES (:folio,:fecha)"
    con = conectar(bd)
    cursor = con.cursor()
    try_transaction(sql,values,con,cursor)

def eliminar_venta(folio):
    values = {"folio":folio}
    sql = "DELETE FROM ventas WHERE folio = :folio"
    con = conectar(bd)
    cursor = con.cursor()
    try_transaction(sql,values,con,cursor)

def insertar_detalle(folio,desc,piezas,total_detalle):
    values = {"folio":folio,"descripcion":desc,"piezas":piezas,"total":total_detalle}
    sql = "INSERT INTO detalle VALUES(:folio,:descripcion,:piezas,:total)"
    con = conectar(bd)
    cursor = con.cursor()
    try_transaction(sql,values,con,cursor)

def finalizar_venta(folio,total):
    values = {"folio":folio,"total":total}
    sql = "UPDATE ventas SET total_venta=:total WHERE folio=:folio"
    con = conectar(bd)
    cursor = con.cursor()
    try_transaction(sql,values,con,cursor)

def try_select(sql,con,cursor,values):
    try:
        if values==False:
            cursor.execute(sql)
        else:
            #print(values)
            cursor.execute(sql,values)

    except sqlite3.OperationalError as e:
        print(e)
    else:
        return cursor.fetchall()
    finally:
        cursor.close()
        close(con)
     


    
def select_ventas():
    sql = "SELECT * FROM ventas"
    con = conectar(bd)
    cursor = con.cursor()
    resultados = try_select(sql,con,cursor,False)
    return resultados
    
    
def select_detalle(folio):
    values = {"folio":folio}
    sql = "SELECT * FROM detalle WHERE folio = :folio"
    con = conectar(bd)
    cursor = con.cursor()
    resultados = try_select(sql,con,cursor,values)
    return resultados

def select_fecha(fecha):
    values = {"fecha":fecha}
    sql = "SELECT folio,total_venta FROM ventas WHERE fecha = :fecha"
    con = conectar(bd)
    cursor = con.cursor()
    resultados = try_select(sql,con,cursor,values)
    return resultados



bd='bd.db'
#separador
SEPARADOR = 15*"-"
#nombre archivo

#iniciamos ciclo 
while True:
    #lista para almacenar los articulos(no venta,detalle,cantidad y precio total)
    transaccion = []
    #imprimimos menu
    respuesta = imprimirMenu()    #entrada de la opcion elegida
    fecha = ""
    if respuesta=="1":
        con = conectar(bd)
        last_folio = select_last_folio(con,bd)
        #print(last_folio)
        close(con)
        #condicional para ver si existe el csv
        if last_folio==0:
            status = crear_tablas(bd)
            if status:
                n_venta=1
            else:
                continue
        elif last_folio==1:
            n_venta = last_folio
        else:
            #print(last_folio)
            n_venta = last_folio[0][0]+1
        #print(n_venta)
        #se abre menú de ventas
        print(f"{SEPARADOR}Menú de Ventas{SEPARADOR}")
        while True: #bucle menú de ventas
            while True:
                    print(f"No. Venta {n_venta}")
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
                            insertar_venta(n_venta,fecha)

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
                                        insertar_venta(n_venta,fecha)

                                        break
                            
                            break 
            #print(n_venta)          
            
            accion = input("1 para añadir artículo - 2 para cerrar venta\n")
            if accion=="1":
                while True:

                    desc = input("Descripcion:\n")#entrada articulo
                    if len(desc.strip(" "))>0:
                        break
                while True:
                    try:
                        q_piezas = int(input("Cantidad de articulos:\n"))#entrada cantidad
                    except:
                        print("Valor introducido no es correcto, Intente de nuevo.")
                    else:
                        if q_piezas>0:
                            break
                        else:
                            print("Valores negativos no son admitidos.")
                while True:
                    try:
                        p_uni = int(input("Precio unitario del producto:\n"))#entrada precio unitario
                    except:
                        print("Valor introducido no es correcto, Intente de nuevo.")
                    else:
                        if p_uni>0:
                            break
                        else:
                            print("Valores negativos no son admitidos.")
                p_total = q_piezas*p_uni #calculamos el importe subtotal
                transaccion.append((n_venta,desc,q_piezas,p_total))#añadimos la venta a memoria con ayuda del diccionario -venta-
                print("Articulo añadido.")
            elif accion=="2":
                #cerramos la venta 
                importe_total = 0  #inicializamos variable para almacenar el importe total
                if len(transaccion)>0: #si la lista ventas es mayor a 0, quiere decir que hay ventas por lo tanto se puede procesar la venta
                    for i in transaccion: #recorremos cada venta 
                        importe_total = importe_total + i[3]#extraemos su precio 
                    print(f"Total : ${importe_total}")

                    finalizar= input("1 Cobrar y Finalizar - 2 Cancelar venta\n") 
                    if finalizar == "1": #finalizamos la venta cobrandola                        
                        for i in transaccion:
                            insertar_detalle(i[0],i[1],i[2],i[3])

                        for i in transaccion:
                            print(i)
                        finalizar_venta(n_venta,importe_total)
                        del transaccion
                        fecha = ""
                        print("Venta Finalizada.")
                        break
                    elif finalizar == "2": #cancelamos venta
                        print("Venta cancelada")
                        eliminar_venta(n_venta)
                        
                        break #terminamos con el ciclo del menú de ventas
                    else:
                        print("Opcion no existe.")
                else:
                    print("Ningun artículo añadido.") 
                    eliminar_venta(n_venta)
                    print("Venta cancelada.")
                    break
            else:
                print("Opcion no existe.")
    #bloque para obtener un reporte
    elif respuesta=="2":
        print(f"{SEPARADOR}Consultar Ventas{SEPARADOR}")
        ventas=select_ventas()
        #print(ventas)
        if ventas==None:
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
                        resultados = select_fecha(fecha)
                        if len(resultados)>1:

                            print(f"{SEPARADOR}Reporte de Ventas del día {fecha} {SEPARADOR}")
                            #print(resultados)
                            print("Venta\tArticulo\tCantidad\tSubTotal")
                            for i in resultados:
                                #print(i)
                                _resultados = select_detalle(i[0])
                                for y in _resultados:
                                    print(f'{y[0]}\t{y[1]}\t\t{y[2]}\t\t{y[3]}')
                            total_venta_reporte=0
                            for folio,total in resultados:
                                total_venta_reporte+=total
                            print(f"Total vendido del día es:\t{total_venta_reporte}")
                        
                            fecha = ""
                        else:
                            print("No hay ventas registradas para la fecha ingresada.")
                            fecha = ""

                elif respuesta==2:
                    break
                else:
                    print("Opcion no valida") 
    #bloque para salir del programa
    elif respuesta=="3":
        print("Saliendo del programa...")
        time.sleep(2)
        sys.exit()
    #bloque -opcion no valida
    else:
        print("Opcion no válida")

