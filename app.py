
'''
export FLASK_APP=example
export FLASK_DEBUG=1
flask run
'''
import re
import dependencies
from flask import Flask, render_template, request,  redirect, url_for, session,flash
from DB_Operations import get_data_menu, get_data_categoria, get_login, get_registro, post_registro, get_tables, get_fields, get_columns, get_menu_item, get_busca, update_row, get_row_data, get_table_data, insert_row, delete_row


#app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app = Flask(__name__)
app.secret_key = '1a2b3c4d5e'

@app.route('/', methods=['GET', 'POST'])
def home():
    all_text = get_data_menu()
    all_categoria = get_data_categoria()
    return render_template('index.html', all_text = all_text, categorias = all_categoria)



# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
       
        usuario = get_login(username,password)
        print(len(usuario))
                # If usuario exists in usuarios table in out database
        if len(usuario)> 1:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = usuario['id']
            session['username'] = usuario['nome']
            # Redirect to home page
            return redirect(url_for('homelog'))
        else:
            # Usuario doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")



# http://localhost:5000/pythinlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
               
        usuario = get_registro(username)

        # If usuario exists show error and validation checks
        if usuario:
            flash("Usuario already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
        # Usuario doesnt exists and the form data is valid, now insert new usuario into usuarios table
            post_registro(username,password)
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html',title="Register")

# http://localhost:5000/pythinlogin/home 
# This will be the home page, only accessible for loggedin users

@app.route('/pythonlogin/homelog')
def homelog():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('adm/home.html', username=session['username'],title="Home")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))    


@app.route('/pythonlogin/profile')
def profile():
    print(session)
    # Check if user is loggedin
    if session['loggedin']:
        # User is loggedin show them the home page
        return render_template('auth/profile.html', username=session['username'],title="Profile")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  


@app.route('/pythonlogin/logout')
def logout():
    print(session)
    session.pop('username')
    print(session)
    return render_template('auth/login.html',title="Login")


'''END LOGIN'''

'''CRUD'''
global TABLES
TABLES = get_tables()

@app.route('/pythonlogin/siteAdm')
def siteAdm():
    # Check if user is loggedin
    if 'loggedin' in session:
        print(TABLES)
        # User is loggedin show them the home page
        return render_template('adm/site_crud.html', username=session['username'],title="Site ADM",tables=TABLES)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/siteAdm/<string:table_name>')
def tableCrud(table_name,methods=['GET', 'POST']):
    # Check if user is loggedin
    if 'loggedin' in session:
        print("Aquiiii ->>> " + table_name)
        campos=get_fields(table_name)
        colunas=get_columns(table_name)
       
        # User is loggedin show them the home page
        return render_template('adm/table_crud.html',username=session['username'],title="Site ADM",colunas=colunas, fields=campos, table_name=table_name)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/table/<table_name>')
def table_view(table_name):
    data = get_table_data(table_name)
    return render_template('adm/table_crud_view.html', table_name=table_name, data=data)

@app.route('/pythonlogin/siteAdm/<string:table_name>/edit/<int:id>', methods=['GET', 'POST'])
def crud_update(table_name, id):
    if 'loggedin' in session:
        row_data = get_row_data(table_name, id)
        print(row_data)
        campos=get_fields(table_name)
        colunas=get_columns(table_name)
       
        # verifica se o formulário foi submetido
        if request.method == 'POST':
            # obtém os dados do formulário
            form_data = request.form
           
            # atualiza os dados da linha no banco de dados
            update_row(table_name, id, form_data)
            print("Atualizooouuu ")
            # redireciona para a página de visualização da tabela
            return redirect(url_for('tableCrud',username=session['username'],title="Site ADM",colunas=colunas, fields=campos, table_name=table_name))
        

        return render_template('adm/crud_update.html', table_name=table_name, row_data=row_data)
        #return render_template('adm/crud_update.html',username=session['username'],title="Site ADM",id=id, table_name=table_name, resultado=get_busca(table_name, id), colunas=colunas)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/siteAdm/insert/<string:table_name>', methods=['GET', 'POST'])
def crud_insert(table_name):
    if 'loggedin' in session:
        campos=get_columns(table_name)
        # verifica se o formulário foi submetido
        if request.method == 'POST':
            # obtém os dados do formulário
            form_data = request.form          
    
            # atualiza os dados da linha no banco de dados
            insert_row(table_name,  form_data)
            print("entrouuuuuuuuuuu ")
            # redireciona para a página de visualização da tabela
            return redirect(url_for('tableCrud',table_name=table_name))
        

        return render_template('adm/crud_insert.html', table_name=table_name,campos=campos, title="Site ADM - Insert")
        #return render_template('adm/crud_update.html',username=session['username'],title="Site ADM",id=id, table_name=table_name, resultado=get_busca(table_name, id), colunas=colunas)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/siteAdm/<string:table_name>/delete/<int:id>', methods=['GET', 'POST'] )
def crud_delete(table_name,id):
    if 'loggedin' in session:
        print("DELETEEEEEEEE")
        delete_row(table_name,id)
        return redirect(url_for('tableCrud',table_name=table_name))
        
    return redirect(url_for('login'))





if __name__ == '__main__':
    app.run()


