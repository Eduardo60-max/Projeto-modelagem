from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime 

app = Flask(__name__)

weekly_priorities = [
    {"id": 1, "text": "Finalizar tarefas", "completed": False},
    {"id": 2, "text": "Visitar a tia Mae", "completed": False},
]

habits = [
    {"id": 1, "text": "Dormir", "days": {"M": False, "T": False, "W": False, "Th": False, "F": False, "Sa": False, "Su": False}, "hours": {"M": 0, "T": 0, "W": 0, "Th": 0, "F": 0, "Sa": 0, "Su": 0}},
]

tasks = {
    "Segunda": [],
    "Terça": [],
    "Quarta": [],
    "Quinta": [],
    "Sexta": [],
    "Sábado": [],
    "Domingo": [],
}

next_priority_id = 3
next_habit_id = 2

@app.route('/')
def index():
    
    current_date_obj = datetime.now()

    
    dias_semana_map = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    meses_map = {
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

    
    formatted_date_en = current_date_obj.strftime("%A, %d de %B de %Y")

    
    current_date_pt = formatted_date_en
    for en, pt in dias_semana_map.items():
        current_date_pt = current_date_pt.replace(en, pt)
    for en, pt in meses_map.items():
        current_date_pt = current_date_pt.replace(en, pt)

    return render_template('index.html',
                            weekly_priorities=weekly_priorities,
                            habits=habits,
                            tasks=tasks,
                            current_date=current_date_pt) 

@app.route('/add_priority', methods=['POST'])
def add_priority():
    global next_priority_id
    new_priority_text = request.form.get('new_priority')
    if new_priority_text:
        weekly_priorities.append({"id": next_priority_id, "text": new_priority_text, "completed": False})
        next_priority_id += 1
    return redirect(url_for('index'))

@app.route('/remove_priority/<int:priority_id>')
def remove_priority(priority_id):
    global weekly_priorities
    weekly_priorities = [p for p in weekly_priorities if p['id'] != priority_id]
    return redirect(url_for('index'))

@app.route('/toggle_priority/<int:priority_id>')
def toggle_priority(priority_id):
    for priority in weekly_priorities:
        if priority['id'] == priority_id:
            priority['completed'] = not priority['completed']
            break
    return redirect(url_for('index'))

@app.route('/add_habit', methods=['POST'])
def add_habit():
    global next_habit_id
    new_habit_text = request.form.get('new_habit')
    if new_habit_text:
        habits.append({
            "id": next_habit_id,
            "text": new_habit_text,
            "days": {"M": False, "T": False, "W": False, "Th": False, "F": False, "Sa": False, "Su": False},
            "hours": {"M": 0, "T": 0, "W": 0, "Th": 0, "F": 0, "Sa": 0, "Su": 0}
        })
        next_habit_id += 1
    return redirect(url_for('index'))

@app.route('/update_habit/<int:habit_id>', methods=['POST'])
def update_habit(habit_id):
    for habit in habits:
        if habit["id"] == habit_id:
            for day_short in ['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su']:
                habit["days"][day_short] = (f'habit_day_{habit_id}_{day_short}' in request.form)
                habit["hours"][day_short] = int(request.form.get(f'hour_{habit_id}_{day_short}', 0))
            break
    return redirect(url_for('index'))


@app.route('/add_task/<day>', methods=['POST'])
def add_task(day):
    new_task_text = request.form.get(f'new_task_{day}')
    if new_task_text and day in tasks:
        tasks[day].append({"text": new_task_text, "completed": False})
    return redirect(url_for('index'))

@app.route('/toggle_task/<day>/<int:task_index>')
def toggle_task(day, task_index):
    if day in tasks and 0 <= task_index < len(tasks[day]):
        tasks[day][task_index]['completed'] = not tasks[day][task_index]['completed']
    return redirect(url_for('index'))

@app.route('/remove_task/<day>/<int:task_index>')
def remove_task(day, task_index):
    if day in tasks and 0 <= task_index < len(tasks[day]):
        del tasks[day][task_index]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)