import pandas as pd
import pulp
import json
from decimal import Decimal

def is_even(number):
    return number % 2 == 0

def resolve_model(
    courses,
    prereqs,
    course_names,
    even_semesters_courses,
    odd_semesters_courses,
    max_courses_per_semester,
    completed_courses,
    first_semester_courses,
    course_levels,
    max_level
):
    # Carrega os horários
    with open("horarios_impar.json", "r", encoding="utf-8") as f:
        horarios_impar_raw = json.load(f)

    with open("horarios_par.json", "r", encoding="utf-8") as f:
        horarios_par_raw = json.load(f)

    # Normaliza horários
    def norm_h(h):
        return Decimal(str(h)).quantize(Decimal("0.1"))

    horarios_impar = {c: [norm_h(h) for h in hs] for c, hs in horarios_impar_raw.items()}
    horarios_par   = {c: [norm_h(h) for h in hs] for c, hs in horarios_par_raw.items()}
    
    semesters = list(range(1, 13))  

    remaining_courses = [c for c in courses if c not in completed_courses]
    prereqs = {c: [p for p in prereqs.get(c, []) if p in remaining_courses] for c in remaining_courses}

    model = pulp.LpProblem('GradeCurricular', pulp.LpMinimize)
    x = pulp.LpVariable.dicts('x', (remaining_courses, semesters), cat='Binary')

    # ===============================================================
    # RESTRIÇÕES
    # ===============================================================

    # 1. Cada disciplina deve ir para exatamente um semestre
    for c in remaining_courses:
        model += pulp.lpSum(x[c][s] for s in semesters) == 1

    if len(completed_courses) == 0:
        # 2. Fixar disciplinas obrigatórias do 1º semestre
        # (essas matérias são pré-definidas na matriz curricular)
        for c in first_semester_courses:
            model += x[c][1] == 1

        # 3. Garantir que apenas essas disciplinas estejam no 1º semestre
        # (impede o solver de colocar outras matérias junto delas)
        model += pulp.lpSum(x[c][1] for c in courses) == len(first_semester_courses)

    # 4. Máximo de matérias por semestre
    for s in semesters:
        model += pulp.lpSum(x[c][s] for c in remaining_courses) <= max_courses_per_semester

    # 5. Pré-requisitos
    for course, prereq_list in prereqs.items():
        for prereq in prereq_list:
            for s in semesters:
                model += x[course][s] <= pulp.lpSum(x[prereq][t] for t in semesters if t < s)

    # 6. Paridade
    for c in remaining_courses:
        if c in even_semesters_courses:
            allowed = [s for s in semesters if is_even(s)]
            model += pulp.lpSum(x[c][s] for s in allowed) == 1
        elif c in odd_semesters_courses:
            allowed = [s for s in semesters if not is_even(s)]
            model += pulp.lpSum(x[c][s] for s in allowed) == 1

    # 7. Limite de nível total por semestre
    for s in semesters:
         model += pulp.lpSum(course_levels[c] * x[c][s] for c in remaining_courses) <= max_level

    # 8. Choque de horário, não permitir matérias com horário coincidente no mesmo semestre
    for s in semesters:
        horarios_semestre = horarios_par if is_even(s) else horarios_impar

        # horários de todas as disciplinas relevantes para esse semestre
        horarios_usados = set()
        for c in remaining_courses:
            if c in horarios_semestre:
                horarios_usados.update(horarios_semestre[c])

        # para cada horário, no máximo 1 disciplina no semestre s
        for h in horarios_usados:
            model += (
                pulp.lpSum(
                    x[c][s]
                    for c in remaining_courses
                    if c in horarios_semestre and h in horarios_semestre[c]
                ) <= 1
            )

    # Variáveis indicando uso real de cada semestre (se contém matéria da paridade)
    y_odd  = pulp.LpVariable.dicts('y_odd',  [s for s in semesters if s % 2 == 1], cat='Binary')
    y_even = pulp.LpVariable.dicts('y_even', [s for s in semesters if s % 2 == 0], cat='Binary')

    # Liga semestre ímpar ao uso real
    for s in y_odd:
        model += y_odd[s] >= pulp.lpSum(x[c][s] for c in remaining_courses if c in odd_semesters_courses) / max_courses_per_semester

    # Liga semestre par ao uso real
    for s in y_even:
        model += y_even[s] >= pulp.lpSum(x[c][s] for c in remaining_courses if c in even_semesters_courses) / max_courses_per_semester

    # Impede buracos na sequência de semestres ímpares
    odd_list = sorted([s for s in semesters if s % 2 == 1])
    for i in range(1, len(odd_list)):
        model += y_odd[odd_list[i]] <= y_odd[odd_list[i-1]]

    # Impede buracos na sequência de semestres pares
    even_list = sorted([s for s in semesters if s % 2 == 0])
    for i in range(1, len(even_list)):
        model += y_even[even_list[i]] <= y_even[even_list[i-1]]

    # ===============================================================
    # FUNÇÃO OBJETIVO
    # ===============================================================

    # Puxa cada matéria para o menor semestre possível
    model += pulp.lpSum(s * x[c][s] for c in remaining_courses for s in semesters)

    # ===============================================================
    # SOLUÇÃO
    # ===============================================================

    model.solve()

    rows = []

    for s in semesters:
        courses_in_semester = [c for c in remaining_courses if x[c][s].value() == 1]

        if courses_in_semester:
            tipo = "Ímpar" if s % 2 != 0 else "Par"

            for c in courses_in_semester:
                rows.append({
                    "semester": s,
                    "type": tipo,
                    "course": c,
                    "course_name": course_names.get(c, c)
                })

    return pd.DataFrame(rows)

def norm_h(h):
    return Decimal(str(h)).quantize(Decimal("0.1"))

def parse_timecode(h_dec: Decimal):
    # Ex: 4.2 -> dia=4, slot=2
    dia = int(h_dec)
    slot = int((h_dec - Decimal(dia)) * Decimal(10))
    return dia, slot

def build_schedule_df(courses_in_semester, horarios_semestre, course_names):
    
    DIAS = {
        1: "segunda",
        2: "terça",
        3: "quarta",
        4: "quinta",
        5: "sexta",
    }
    
    # filtra só as disciplinas com horário fixo (presentes no json)
    fixed_courses = [c for c in courses_in_semester if c in horarios_semestre]

    if not fixed_courses:
        return None

    # coleta slots usados
    slots = set()
    for c in fixed_courses:
        for h in horarios_semestre[c]:
            h_dec = norm_h(h)
            dia, slot = parse_timecode(h_dec)
            if dia in DIAS:
                slots.add(slot)

    if not slots:
        return None

    slots = sorted(slots)

    # monta a grade vazia
    df_cal = pd.DataFrame("", index=slots, columns=[DIAS[i] for i in range(1, 6)])

    # preenche
    for c in fixed_courses:
        nome = course_names.get(c, c)
        texto = f"{c} - {nome}" if nome != c else c

        for h in horarios_semestre[c]:
            h_dec = norm_h(h)
            dia, slot = parse_timecode(h_dec)

            if dia not in DIAS:
                continue

            col = DIAS[dia]

            # se já tiver algo, concatena (só por segurança, mesmo que o solver impeça conflito)
            if df_cal.loc[slot, col]:
                df_cal.loc[slot, col] = df_cal.loc[slot, col] + "\n" + texto
            else:
                df_cal.loc[slot, col] = texto

    # opcional: deixar o índice mais bonito
    df_cal.index = [f"horário {s}" for s in df_cal.index]
    return df_cal