import os
import sys
from flask import Flask, render_template, jsonify, abort, request, redirect, url_for

# Ajuste para importar dos módulos irmãos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'acompanhamento_visitantes', '02_cartao_boas_vindas')))
from integrar_cartoes import generate_cards_from_spreadsheet, gerar_cartao_individual
from models import db, Visitor
from database import init_db

app = Flask(__name__)
app.instance_path = os.path.join(os.getcwd(), 'instance')
init_db(app)

from datetime import datetime, timedelta
from collections import Counter

@app.route('/relatorios')
def relatorios():
    visitors = Visitor.query.all()

    # Contagem por mês (últimos 12 meses a partir de hoje)
    hoje = datetime.now()
    month_counts = Counter()
    for v in visitors:
        try:
            data = datetime.strptime(v.data_chegada, '%Y-%m-%d')
            # Agrupa no mês de chegada; pode refinar para meses correntes
            month_key = f"{data.year}-{data.month:02d}"
            month_counts[month_key] += 1
        except (ValueError, TypeError):
            continue

    # Distribuição de status geral
    status_counts = dict(Counter([v.status_geral for v in visitors if v.status_geral]))

    return render_template('relatorios.html',
                           month_data=dict(sorted(month_counts.items())),
                           status_data=status_counts)

@app.route('/')
def index():
    hoje = datetime.now().date()
    semana_passada = hoje - timedelta(days=7)

    visitors = Visitor.query.all()

    # KPIs (Últimos 7 dias)
    v_semana = [v for v in visitors if datetime.strptime(v.data_chegada, '%Y-%m-%d').date() >= semana_passada]

    kpis = {
        "total_semana": len(v_semana),
        "permissao": len([v for v in v_semana if v.autorizou_contato]),
        "retorno": len([v for v in v_semana if v.status_geral == 'Positivo']), # Assumindo 'Positivo'
        "hoje": len([v for v in visitors if v.data_chegada == str(hoje)])
    }

    return render_template('index.html', visitors=visitors, kpis=kpis)

@app.route('/visitor/<int:visitor_id>')
def visitor_detail(visitor_id):
    visitor = Visitor.query.filter_by(id=visitor_id, autorizou_contato=True).first()
    if not visitor:
        abort(404)
    return render_template('visitor_detail.html', visitor=visitor)

@app.route('/api/generate_card/<int:visitor_id>', methods=['POST'])
def generate_card(visitor_id):
    visitor = Visitor.query.filter_by(id=visitor_id, autorizou_contato=True).first()
    if not visitor:
        abort(404)

    # Gerar cartão individual
    caminho_arquivo = gerar_cartao_individual(visitor.nome)

    return jsonify({"status": "Cartão gerado com sucesso", "file_path": caminho_arquivo})

@app.route('/api/get_message/<int:visitor_id>')
def get_message(visitor_id):
    # Lógica simples de retorno de template
    return jsonify({"message": "Olá! Seja bem-vindo à nossa igreja."})

@app.route('/visitantes', methods=['GET', 'POST'])
def novo_visitante():
    if request.method == 'POST':
        nome = request.form['nome']
        whatsapp = request.form['whatsapp']
        bairro = request.form['bairro']

        # Criando o novo visitante com dados padrão iniciais
        novo = Visitor(
            nome=nome,
            whatsapp=whatsapp,
            bairro=bairro,
            culto='Não informado',
            data_chegada=str(datetime.now().date()),
            fase_atual='Dia 0',
            status_geral='Ativo',
            autorizou_contato=True
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('novo_visitante.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
