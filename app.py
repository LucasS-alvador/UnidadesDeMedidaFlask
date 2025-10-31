# Seção 1: Importações
# ---------------------
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

# Seção 2: Configuração Inicial
# ------------------------------
app = Flask(__name__)
app.secret_key = '17f5fe9813722ae4f396dc93f56b3125c7797b18e2af49a5c912de405956a009'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'unidadesdemedida'
}

# Seção 3: Rotas da Aplicação
# ---------------------------

# Rota principal - lista todas as unidades
@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM unidade_medida ORDER BY cod_unidade")
    unidades = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', unidades=unidades)


# Rota de cadastro
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome_unidade']
        sigla = request.form['sigla_unidade']

        if not nome or not sigla:
            flash("Preencha todos os campos!", "erro")
            return redirect(url_for('adicionar'))

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO unidade_medida (nome_unidade, sigla_unidade)
            VALUES (%s, %s)
        """, (nome, sigla))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Unidade cadastrada com sucesso!", "sucesso")
        return redirect(url_for('index'))

    return render_template('adicionar.html')


# Rota de edição
@app.route('/editar/<int:cod_unidade>', methods=['GET', 'POST'])
def editar(cod_unidade):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nome = request.form['nome_unidade']
        sigla = request.form['sigla_unidade']

        cursor.execute("""
            UPDATE unidade_medida
            SET nome_unidade = %s, sigla_unidade = %s
            WHERE cod_unidade = %s
        """, (nome, sigla, cod_unidade))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Unidade atualizada com sucesso!", "sucesso")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM unidade_medida WHERE cod_unidade = %s", (cod_unidade,))
    unidade = cursor.fetchone()
    cursor.close()
    conn.close()

    if not unidade:
        flash("Unidade não encontrada.", "erro")
        return redirect(url_for('index'))

    return render_template('editar.html', unidade=unidade)


# Rota de exclusão
@app.route('/excluir/<int:cod_unidade>', methods=['POST'])
def excluir(cod_unidade):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM unidade_medida WHERE cod_unidade = %s", (cod_unidade,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Unidade excluída com sucesso!", "sucesso")
    return redirect(url_for('index'))


# Seção 4: Execução
# -----------------
if __name__ == '__main__':
    app.run(debug=True)
