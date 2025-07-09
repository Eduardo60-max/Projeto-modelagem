from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

prioridades_semanais = [
    {"id": 1, "texto": "Finalizar tarefas", "concluida": False},
    {"id": 2, "texto": "Visitar a tia Mae", "concluida": False},
]

habitos = [
    {"id": 1, "texto": "Dormir", "dias": {"S": False, "T": False, "Q": False, "Qi": False, "Se": False, "Sa": False, "D": False}, "horas": {"S": 0, "T": 0, "Q": 0, "Qi": 0, "Se": 0, "Sa": 0, "D": 0}},
]

tarefas_diarias = {
    "Segunda": [],
    "Terça": [],
    "Quarta": [],
    "Quinta": [],
    "Sexta": [],
    "Sábado": [],
    "Domingo": [],
}

proximo_id_prioridade = 3
proximo_id_habito = 2

ORDEM_PRIORIDADE = {'alta': 1, 'media': 2, 'baixa': 3}

@app.route('/')
def inicio():
    data_atual_obj = datetime.now()

    mapa_dias_semana = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    mapa_meses = {
        "January": "Janeiro",
        "February": "Fevereiro",
        "March": "Março",
        "April": "Abril",
        "May": "Maio",
        "June": "Junho",
        "July": "Julho",
        "August": "Agosto",
        "September": "Setembro",
        "October": "Outubro",
        "November": "Novembro",
        "December": "Dezembro"
    }

    data_formatada_ingles = data_atual_obj.strftime("%A, %d de %B de %Y")

    data_atual_portugues = data_formatada_ingles
    for en, pt in mapa_dias_semana.items():
        data_atual_portugues = data_atual_portugues.replace(en, pt)
    for en, pt in mapa_meses.items():
        data_atual_portugues = data_atual_portugues.replace(en, pt)

    tarefas_diarias_ordenadas = {}
    for dia, tarefas_do_dia in tarefas_diarias.items():
        tarefas_concluidas = [t for t in tarefas_do_dia if t['concluida']]
        tarefas_pendentes = [t for t in tarefas_do_dia if not t['concluida']]

        tarefas_pendentes.sort(key=lambda x: ORDEM_PRIORIDADE.get(x.get('prioridade', 'baixa'), 99))
        
        tarefas_diarias_ordenadas[dia] = tarefas_pendentes + tarefas_concluidas

    return render_template('index.html',
                            prioridades_semanais=prioridades_semanais,
                            habitos=habitos,
                            tarefas_diarias=tarefas_diarias_ordenadas,
                            data_atual=data_atual_portugues)

@app.route('/adicionar_prioridade', methods=['POST'])
def adicionar_prioridade():
    global proximo_id_prioridade
    novo_texto_prioridade = request.form.get('nova_prioridade')
    if novo_texto_prioridade:
        prioridades_semanais.append({"id": proximo_id_prioridade, "texto": novo_texto_prioridade, "concluida": False})
        proximo_id_prioridade += 1
    return redirect(url_for('inicio'))

@app.route('/remover_prioridade/<int:prioridade_id>')
def remover_prioridade(prioridade_id):
    global prioridades_semanais
    prioridades_semanais = [p for p in prioridades_semanais if p['id'] != prioridade_id]
    return redirect(url_for('inicio'))

@app.route('/alternar_prioridade/<int:prioridade_id>')
def alternar_prioridade(prioridade_id):
    for prioridade in prioridades_semanais:
        if prioridade['id'] == prioridade_id:
            prioridade['concluida'] = not prioridade['concluida']
            break
    return redirect(url_for('inicio'))

@app.route('/adicionar_habito', methods=['POST'])
def adicionar_habito():
    global proximo_id_habito
    novo_texto_habito = request.form.get('novo_habito')
    if novo_texto_habito:
        habitos.append({
            "id": proximo_id_habito,
            "texto": novo_texto_habito,
            "dias": {"S": False, "T": False, "Q": False, "Qi": False, "Se": False, "Sa": False, "D": False},
            "horas": {"S": 0, "T": 0, "Q": 0, "Qi": 0, "Se": 0, "Sa": 0, "D": 0}
        })
        proximo_id_habito += 1
    return redirect(url_for('inicio'))

@app.route('/atualizar_habito/<int:habito_id>', methods=['POST'])
def atualizar_habito(habito_id):
    for habito in habitos:
        if habito["id"] == habito_id:
            for dia_curto in ['S', 'T', 'Q', 'Qi', 'Se', 'Sa', 'D']:
                habito["dias"][dia_curto] = (f'dia_habito_{habito_id}_{dia_curto}' in request.form)
                habito["horas"][dia_curto] = int(request.form.get(f'hora_{habito_id}_{dia_curto}', 0))
            break
    return redirect(url_for('inicio'))


@app.route('/adicionar_tarefa/<dia>')
def adicionar_tarefa(dia):
    return redirect(url_for('inicio'))

@app.route('/adicionar_tarefa/<dia>', methods=['POST'])
def adicionar_tarefa_post(dia):
    novo_texto_tarefa = request.form.get(f'nova_tarefa_{dia}')
    prioridade_tarefa = request.form.get(f'prioridade_{dia}', 'baixa')
    if novo_texto_tarefa and dia in tarefas_diarias:
        tarefas_diarias[dia].append({"texto": novo_texto_tarefa, "concluida": False, "prioridade": prioridade_tarefa})
    return redirect(url_for('inicio'))


@app.route('/alternar_tarefa/<dia>/<int:indice_tarefa>')
def alternar_tarefa(dia, indice_tarefa):
    if dia in tarefas_diarias and 0 <= indice_tarefa < len(tarefas_diarias[dia]):
        tarefas_diarias[dia][indice_tarefa]['concluida'] = not tarefas_diarias[dia][indice_tarefa]['concluida']
    return redirect(url_for('inicio'))

@app.route('/remover_tarefa/<dia>/<int:indice_tarefa>')
def remover_tarefa(dia, indice_tarefa):
    if dia in tarefas_diarias and 0 <= indice_tarefa < len(tarefas_diarias[dia]):
        del tarefas_diarias[dia][indice_tarefa]
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)