                                #archivo inicial del servidor
#---------------------------------------------------------------------------------------------#
#inportamos el modulo y requerimos render_template e inportamos request inportamos redirect
from flask import Flask, render_template, request,redirect,url_for,flash
from Crypto.Cipher import AES
#conectamos al DB
from flask_mysqldb import MySQL
#---------------------------------------------------------------------------------------------#
#poder tener una conexion un objeto
app = Flask(__name__)
#Mysql Conneccion
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='pweb_python'
mysql = MySQL(app)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'PWEB_PYTHON'
# mysql = MySQL(app)
#iniciamos session
app.secret_key= 'mysecretkey'
#---------------------------------------------------------------------------------------------#
#funcion y retorno index.html #cada vez que alguien entre a la pag web vamos a responder algo
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM login')
    data = cur.fetchall()
    return render_template('index.html',contacts = data)#retornamos o renderisamos plantilla

#creamos ruta(registramos al usuario)#-----------------------------------------------------------------------------------------#
@app.route('/add_contact',methods=['POST'])
def add_contact():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        #cursor es para manejar nuestra coneccion
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO login(usuario,password) VALUES(%s,aes_encrypt(%s,"toto"));',(usuario,password))
        #cur.execute('INSERT INTO user(usuario,email,contraseña) VALUES(%s,%s,%s);',(usuario,email,password))
        mysql.connection.commit()
        flash('contacto added succesfull')
        return redirect(url_for('Index'))#volvemos a la vista de inicio con redirect
#-------------------------------------------------------------------------------------------------------------------------------#
#otra ruta(llamamos con /edit -> para editar contactos)
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM login WHERE id_l = {0};'.format(id))
    data = cur.fetchall()
    return render_template('edit.html',contact = data[0])

@app.route('/update/<id>',methods=['POST'])
def update_contact(id):
     if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE login
            SET usuario = %s,
                password = %s
            WHERE id_l = %s
                """,(usuario,password,id))
        mysql.connection.commit()
        flash('Contact Update Successfully')
        return redirect(url_for('Index'))
#ruta de eliminar
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM login where id_l= {0};'.format(id))
    mysql.connection.commit()
    flash('delete with succesfull')
    return redirect(url_for('Index'))
data = 'jabon'

#@app.route('/encript')
# def encryptar(key, data):
#     cipher = AES.new(key, AES.MODE_EAX)
#     ciphertext, tag = cipher.encrypt_and_digest(data)
#     print(data)
#     return cipher.nonce + tag + ciphertext
#codigo para iniciar el servidor #debug reinicia cada ves que entramos a la pag web    
if __name__ == '__main__':
    app.run(port = 3000, debug = True)