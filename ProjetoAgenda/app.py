from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def ligar_banco():
    banco = psycopg2.connect(
        host = "localhost",
        dbname = "BancoAgenda",
        user = "postgres",
        password = "senai",
        port = "5432"
    )
    return banco




@app.route('/')
def index():
    return render_template("index.html")
@app.route('/compromisso')
def compromisso():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""SELECT id_compromisso, titulo, local, duracao, data FROM compromisso ORDER BY id_compromisso DESC
                   """)
    lista = cursor.fetchall()
    banco.close()
    return render_template("compromisso.html", compromisso = lista)



@app.route('/compromisso/enviar', methods=['POST'])
def enviar():
    titulo = request.form.get('titulo')
    local = request.form.get('local')
    duracao = request.form.get('duracao')
    data = request.form.get('data')
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO compromisso(titulo, local, duracao, data)
                   VALUES (%s, %s, %s, %s)""", (titulo, local, duracao, data))
    banco.commit()
    banco.close()
    return redirect('/')



@app.route('/compromisso/editar/<int:id>')
def editar_compromisso(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_compromisso, titulo, local, duracao, data FROM compromisso WHERE id_compromisso = %s", (id,))
    compromisso = cursor.fetchone()
    banco.close()

    if compromisso is None:
        return redirect('/')
    return render_template('editar_compromisso.html', compromisso=compromisso)


@app.route('/compromisso/atualizar/<int:id_compromisso>', methods=['POST'])
def atualizar_compromisso(id_compromisso):
    titulo = request.form.get('titulo')
    local = request.form.get('local')
    duracao = request.form.get('duracao')
    data = request.form.get('data')
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE compromisso SET titulo = %s, local = %s, duracao = %s, data =%s
                   WHERE id_compromisso = %s""", (titulo, local, duracao, data, id_compromisso))
    banco.commit()
    banco.close()
    return redirect('/')


@app.route('/compromisso/excluir/<int:id_compromisso>', methods=['POST'])
def excluir_compromisso(id_compromisso):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""DELETE FROM compromisso WHERE id_compromisso = %s""", (id_compromisso,))
    banco.commit()
    banco.close()
    return redirect('/')
@app.route('/contato')
def listar_contatos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""SELECT id_contato, nome, telefone, idade, data_aniversario FROM contato ORDER BY id_contato
    """)
    contatos = cursor.fetchall()
    banco.close()
    return render_template("contato.html", contatos=contatos)

@app.route('/contato/enviar', methods=['POST'])
def enviar_contato():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    idade = request.form.get("idade")
    data_aniversario = request.form.get("data_aniversario")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO contato (nome, telefone, idade, data_aniversario)
                   VALUES (%s, %s, %s, %s)""", (nome, telefone, idade, data_aniversario))
    banco.commit()
    banco.close()
    return redirect("/contato")

@app.route('/contato/editar/<int:id_contato>')
def editar_contato(id_contato):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id_contato, nome, telefone, idade, data_aniversario FROM contato WHERE id_contato = %s', (id_contato,))
    contato = cursor.fetchone()
    banco.close()

    if contato is None:
        return redirect("/")
    return render_template("editar_contato.html", contato=contato)

@app.route("/contato/atualizar/<int:id_contato>", methods=['POST'])
def atualizar_contato(id_contato):
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    idade = request.form.get("idade")
    data_aniversario = request.form.get("data_aniversario")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE contato SET nome = %s, telefone = %s, idade = %s, data_aniversario = %s 
                      WHERE id_contato = %s""", (nome, telefone, idade, data_aniversario, id_contato))
    banco.commit()
    banco.close()
    return redirect("/contato")

@app.route("/contato/excluir/<int:id_contato>", methods=['POST'])
def excluir_contato(id_contato):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM contato WHERE id_contato = %s", (id_contato,))
    banco.commit()
    banco.close()
    return redirect("/contato")


if __name__ == '_main_':
    app.run()