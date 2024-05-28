import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from django.shortcuts import render
from transbank.webpay.webpay_plus.transaction import Transaction

CommerceCode = '597055555532'
ApiKeySecret = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'

#C
@app.route('/create/<name>/<email>/<int:phone>/<address>', methods=['POST'])
def create_emp(name,email,phone,address):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO emp(name, email, phone, address) VALUES(%s, %s, %s, %s)"
        bindData = (name,email,phone,address)            
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        respone = jsonify('Employee added successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()          
 #L   
@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM emp")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  
#R
@app.route('/emp/<int:emp_id>')
def emp_details(emp_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM emp WHERE id =%s", emp_id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
#U
@app.route('/update/<name>/<email>/<phone>/<address>/<int:id>', methods=['PUT'])
def update_emp(name, email, phone, address, id):
    try:
        if name and email and phone and address and id:
            sqlQuery = "UPDATE emp SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
            bindData = (name, email, phone, address, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Employee updated successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
#D
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_emp(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM emp WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Employee deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

#PRODUCTO

#C

@app.route('/create_pro/<nombreprod>/<int:precioprod>/<descripprod>', methods=['POST'])
def create_producto(nombreprod, precioprod, descripprod):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO producto(nombreprod ,precioprod , descripprod) VALUES(%s, %s, %s)"
        bindData = (nombreprod, precioprod, descripprod)            
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify('Producto agregado exitosamente!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        response = jsonify({'error': 'Error al agregar el producto'})
        response.status_code = 500
        return response
    finally:
        cursor.close() 
        conn.close()  
 #L   
@app.route('/producto')
def producto():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT idproducto,nombreprod,precioprod, descripprod FROM producto")
        proRows = cursor.fetchall()
        respone = jsonify(proRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  
#R
@app.route('/producto/<int:producto_id>')
def producto_details(producto_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT idproducto,nombreprod,precioprod, descripprod FROM producto WHERE idproducto =%s", producto_id)
        proRow = cursor.fetchone()
        respone = jsonify(proRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
#U
@app.route('/update_pro/<idproducto>/<nombreprod>/<int:precioprod>/<descripprod>', methods=['PUT'])
def update_producto(idproducto,nombreprod,precioprod, descripprod):
    try:
        if nombreprod and precioprod and descripprod and idproducto:
            sqlQuery = "UPDATE producto SET nombreprod=%s, precioprod=%s, descripprod=%s WHERE idproducto=%s"
            bindData = (nombreprod,precioprod, descripprod, idproducto)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Producto updated successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
#D
@app.route('/delete_pro/<int:idproducto>', methods=['DELETE'])
def delete_producto(idproducto):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM producto WHERE idproducto =%s", (idproducto,))
		conn.commit()
		respone = jsonify('Producto deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

#cliente
#C
@app.route('/create_cli/<nombrecli>/<usuariocli>/<correocli>/<direccioncli>', methods=['POST'])
def create_cli(nombrecli,usuariocli,correocli,direccioncli):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO cliente(nombrecli,usuariocli,correocli,direccioncli) VALUES(%s, %s, %s, %s)"
        bindData = (nombrecli,usuariocli,correocli,direccioncli)            
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        respone = jsonify('Cliente added successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()          
 #L   
@app.route('/cliente')
def cliente():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT idcliente,nombrecli,usuariocli,correocli,direccioncli FROM cliente")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  
#R
@app.route('/cliente/<int:cliente_id>')
def cliente_details(cliente_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT idcliente,nombrecli,usuariocli,correocli,direccioncli FROM cliente WHERE idcliente =%s", cliente_id)
        cliRow = cursor.fetchone()
        respone = jsonify(cliRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
#U
@app.route('/update_cli/<nombrecli>/<usuariocli>/<correocli>/<direccioncli>/<int:idcliente>', methods=['PUT'])
def update_cli(nombrecli,usuariocli,correocli,direccioncli, idcliente):
    try:
        if nombrecli and usuariocli and correocli and direccioncli and idcliente:
            sqlQuery = "UPDATE cliente SET nombrecli=%s, usuariocli=%s, correocli=%s, direccioncli=%s WHERE idcliente=%s"
            bindData = (nombrecli,usuariocli,correocli,direccioncli, idcliente)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Cliente updated successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
#D
@app.route('/delete_cli/<int:idcliente>', methods=['DELETE'])
def delete_cliente(idcliente):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM cliente WHERE idcliente =%s", (idcliente,))
		conn.commit()
		respone = jsonify('Cliente deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

#CATEGORIA
#C
@app.route('/create_cat')
def create_cat():
    if request.method == "GET":
        return render(request, "add_cat.html")
    elif request.method == "POST":
        try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery = "INSERT INTO categoria(desc_cat) VALUES(%s)"
                desc_cat = request.POST.get("desc_cat")
                bindData = (desc_cat)            
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                respone = jsonify('Categoria añadida exitosamente!')
                respone.status_code = 200
                return respone
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()
    else:
         print('f')

        
if __name__ == "__main__":
    app.run()


    
