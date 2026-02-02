import pulp

def is_even(number):
    return number % 2 == 0

# ===============================================================
# DEFINIÇÃO DOS DADOS
# ===============================================================

courses = [
    'ENGF56', 'MATA01', 'MATA02', 'ENGD01', 'FIS121', 'MATA03', 'ENG041', 
    'ENGD02', 'MATA07', 'QUIB50', 'ECO151', 'FIS122', 'MATA04', 'ENG207', 
    'ENG269', 'ENGF81', 'ENGF90', 'ENGF77', 'ENGF78', 'ENGF80', 'ENGF82', 
    'FCC024', 'DIR175', 'ENG308', 'ENGF79', 'ENGF86', 'OP1', 'ENG037', 
    'ENG040', 'ENG179', 'ENG430', 'ENGA62', 'ENG039', 'ENGF83', 'ENGF84', 
    'ENGF85', 'OP2', 'ENG432', 'ENGF88', 'FIS123', 'OP3', 'ENG003', 
    'ENGF89', 'OP4', 'OP5', 'ENGF87'
]

prereqs = {
    'MATA03': ['MATA01', 'MATA02'],
    'FIS121': ['MATA02'],
    'ENGD01': ['MATA02'],
    'ENG041': ['FIS121'],
    'ENGD02': ['ENGD01', 'MATA03'],
    'MATA07': ['MATA01'],
    'FIS122': ['FIS121', 'MATA01', 'MATA02'],
    'MATA04': ['MATA03'],
    'ENG207': ['FIS121'],
    'ENG269': ['QUIB50'],
    'ENGF81': ['ENGD01', 'ENGD02', 'MATA02', 'MATA03', 'MATA07'],
    'ENGF90': ['FIS121', 'MATA02'],
    'ENGF77': ['ENGF56'],
    'ENGF78': ['FIS122', 'MATA03'],
    'ENGF80': ['ENG041', 'ENGF90'],
    'ENGF82': ['ENGF81'],
    'FCC024': ['ECO151'],
    'DIR175': ['ENGF77'],
    'ENG308': ['ECO151', 'ENGD02', 'ENGF77'],
    'ENGF79': ['MATA02', 'QUIB50'],
    'ENGF86': ['ECO151'],
    'ENG037': ['ENGF82'],
    'ENG040': ['ECO151', 'ENGF77'],
    'ENG179': ['ENGD02', 'ENGF80', 'ENGF86'],
    'ENG430': ['ENGF80'],
    'ENGA62': ['ENGF82'],
    'ENG039': ['ECO151', 'ENGD02', 'ENGF77'],
    'ENGF83': ['ENG179', 'ENGD02', 'ENGF82'],
    'ENGF84': ['ENG037', 'ENG179', 'ENGA62', 'ENGF79', 'ENGF80', 'ENGF82'],
    'ENGF85': ['ENG430', 'ENGA62'],
    'ENG432': ['ENG037', 'ENG179', 'ENGF79', 'ENGF80'],
    'ENGF88': ['ENG037', 'ENG430', 'ENGF77', 'ENGF86'],
    'FIS123': ['FIS122', 'MATA03'],
    'ENG003': ['FIS123'],
    'ENGF89': ['ENGF88']
}

course_names = {
    'ENGF56': 'INTRODUÇÃO À ENGENHARIA DE PRODUÇÃO',
    'MATA01': 'GEOMETRIA ANALÍTICA',
    'MATA02': 'CÁLCULO A',
    'ENGD01': 'MÉTODOS COMPUTACIONAIS NA ENGENHARIA',
    'FIS121': 'FÍSICA GERAL E EXPERIMENTAL I-E',
    'MATA03': 'CÁLCULO B',
    'ENG041': 'MATERIAIS DE CONSTRUÇÃO MECÂNICA I',
    'ENGD02': 'ESTATÍSTICA NA ENGENHARIA',
    'MATA07': 'ÁLGEBRA LINEAR A',
    'QUIB50': 'FUNDAMENTOS DE QUÍMICA',
    'ECO151': 'ECONOMIA E FINANÇAS',
    'FIS122': 'FÍSICA GERAL E EXPERIMENTAL II-E',
    'MATA04': 'CÁLCULO C',
    'ENG207': 'METROLOGIA INDUSTRIAL',
    'ENG269': 'CIÊNCIAS DO AMBIENTE',
    'ENGF81': 'PESQUISA OPERACIONAL I',
    'ENGF90': 'FUNDAMENTOS DE MECÂNICA DOS SÓLIDOS',
    'ENGF77': 'ADMINISTRAÇÃO NA ENGENHARIA',
    'ENGF78': 'MECÂNICA DOS FLUÍDOS',
    'ENGF80': 'SISTEMAS DE PRODUÇÃO DISCRETA',
    'ENGF82': 'PESQUISA OPERACIONAL II',
    'FCC024': 'CONTABILIDADE DE CUSTOS',
    'DIR175': 'LEGISLAÇÃO SOCIAL',
    'ENG308': 'SISTEMAS DE GARANTIA DA QUALIDADE',
    'ENGF79': 'PRINCÍPIOS DOS PROCESSOS CONTÍNUOS',
    'ENGF86': 'ENGENHARIA ECONÔMICA',
    'OP1': 'OPTATIVA 1',
    'ENG037': 'PLANEJAMENTO E CONTROLE DA PRODUÇÃO',
    'ENG040': 'GESTÃO EMPREENDEDORA DA ENGENHARIA',
    'ENG179': 'PROJETO E PLANEJAMENTO INDUSTRIAL',
    'ENG430': 'ENGENHARIA DE PRODUTO',
    'ENGA62': 'LOGÍSTICA DE TRANSPORTES',
    'ENG039': 'GESTÃO DA QUALIDADE NA ENGENHARIA',
    'ENGF83': 'SISTEMAS DE APOIO À DECISÃO',
    'ENGF84': 'MODELAGEM E OTIMIZAÇÃO DE SISTEMAS DE PRODUÇÃO',
    'ENGF85': 'ENGENHARIA DO TRABALHO',
    'OP2': 'OPTATIVA 2',
    'ENG432': 'MANUFATURA ASSISTIDA POR COMPUTADOR',
    'ENGF88': 'PLANEJAMENTO DO TRABALHO DE CONCLUSÃO',
    'FIS123': 'FÍSICA GERAL E EXPERIMENTAL III-E',
    'OP3': 'OPTATIVA 3',
    'ENG003': 'ELETRICIDADE',
    'ENGF89': 'TRABALHO DE CONCLUSÃO DE CURSO',
    'OP4': 'OPTATIVA 4',
    'OP5': 'OPTATIVA 5',
    'ENGF87': 'ESTÁGIO EM ENGENHARIA DE PRODUÇÃO'
}


even_semesters_courses = ['ENGF77','ENGF78','ENGF80','ENG040','ENG430','ENG432']
odd_semesters_courses = ['ENGF56','ENG207','ENGF90','ENG308','ENGF86','ENGF83','ENGF84','ENGF85']

first_semester_courses = ['ENGF56', 'MATA01', 'MATA02']
semesters = list(range(1, 13))
max_courses_per_semester = 5

# ===============================================================
# ENTRADA DO USUÁRIO
# ===============================================================

# Disciplinas já cursadas
completed_courses = ['ENGF56','MATA01',"MATA02","ENGD01","FIS121","MATA03","ENGD02","MATA07","QUIB50","ECO151",
                     "FIS122","MATA04","ENG207","ENG269","ENGF81","ENGF90","ENGF77","ENGF82","FCC024","ENG308",
                     "ENGF86","OP1",'ENG003', 'FIS123', 'OP2','ENG040', 'ENGF78', 'ENGA62']

# Define se o semestre atual é ímpar ou par
current_semester_is_even = False  # altere para True se estiver em semestre par

# ===============================================================
# AJUSTE DOS DADOS
# ===============================================================

# Filtra apenas as disciplinas que ainda faltam
remaining_courses = [c for c in courses if c not in completed_courses]

# Ajusta os pré-requisitos considerando apenas disciplinas ainda existentes
prereqs = {c: [p for p in prereqs.get(c, []) if p in remaining_courses] for c in remaining_courses}

# ===============================================================
# MODELO DE OTIMIZAÇÃO
# ===============================================================

model = pulp.LpProblem('GradeCurricular', pulp.LpMinimize)
x = pulp.LpVariable.dicts('x', (remaining_courses, semesters), cat='Binary')

# ===============================================================
# RESTRIÇÕES
# ===============================================================

# 1. Cada disciplina restante deve ser alocada em exatamente um semestre
for c in remaining_courses:
    model += pulp.lpSum(x[c][s] for s in semesters) == 1

# 2. Limite máximo de disciplinas por semestre
for s in semesters:
    model += pulp.lpSum(x[c][s] for c in remaining_courses) <= max_courses_per_semester

# 3. Restrições de pré-requisitos
for course, prereq_list in prereqs.items():
    for prereq in prereq_list:
        for s in semesters:
            model += x[course][s] <= pulp.lpSum(x[prereq][t] for t in semesters if t < s)

# 4. Restrições de paridade
for c in remaining_courses:
    if c in even_semesters_courses:
        allowed = [s for s in semesters if is_even(s)]  # apenas semestres pares
        model += pulp.lpSum(x[c][s] for s in allowed) == 1
    elif c in odd_semesters_courses:
        allowed = [s for s in semesters if not is_even(s)]  # apenas semestres ímpares
        model += pulp.lpSum(x[c][s] for s in allowed) == 1

# ===============================================================
# FUNÇÃO OBJETIVO
# ===============================================================

last_semester = pulp.LpVariable('ultimo_semestre', lowBound=1, upBound=max(semesters), cat='Integer')

for c in remaining_courses:
    for s in semesters:
        model += last_semester >= s * x[c][s]

model += last_semester

# ===============================================================
# SOLUÇÃO
# ===============================================================

model.solve()

print("Status:", pulp.LpStatus[model.status])
print(f"\nDisciplinas restantes concluídas em {last_semester.value()} semestres\n")

for s in semesters:
    courses_in_semester = [c for c in remaining_courses if x[c][s].value() == 1]
    if courses_in_semester:
        tipo = "Ímpar" if s % 2 != 0 else "Par"
        nomes = [course_names.get(c, c) for c in courses_in_semester]
        print(f"\nSemestre {tipo} ({len(nomes)} matérias):")
        for nome in nomes:
            print(" -", nome)




