import pulp

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

# Disciplinas fixas no primeiro semestre
first_semester_courses = ['ENGF56', 'MATA01', 'MATA02']

semesters = list(range(1, 13))  # até 12 semestres disponíveis
max_courses_per_semester = 6

model = pulp.LpProblem('GradeCurricular', pulp.LpMinimize)

x = pulp.LpVariable.dicts('x', (courses, semesters), cat='Binary')

# Cada curso deve ser alocado em exatamente um semestre
for c in courses:
    model += pulp.lpSum(x[c][s] for s in semesters) == 1

# Fixar disciplinas do primeiro semestre
for c in first_semester_courses:
    model += x[c][1] == 1

# Garantir que APENAS essas disciplinas estejam no primeiro semestre
model += pulp.lpSum(x[c][1] for c in courses) == len(first_semester_courses)

# Cada semestre (exceto o primeiro que já está fixo) deve ter um numero max de cursos
for s in semesters:
    if s > 1:
        model += pulp.lpSum(x[c][s] for c in courses) <= max_courses_per_semester

# Restrições de pré-requisitos
for course, prereq_list in prereqs.items():
    for prereq in prereq_list:
        for s in semesters:
            model += x[course][s] <= pulp.lpSum(x[prereq][t] for t in semesters if t < s)

# Função objetivo: minimizar o último semestre usado
ultimo_semestre = pulp.LpVariable('ultimo_semestre', lowBound=1, upBound=max(semesters), cat='Integer')

for c in courses:
    for s in semesters:
        model += ultimo_semestre >= s * x[c][s]

model += ultimo_semestre

# Resolver
model.solve()

print("Status:", pulp.LpStatus[model.status])
print(f"\nCurso concluído em {int(ultimo_semestre.value())} semestres\n")
print("Grade Curricular Ótima:\n")

for s in semesters:
    courses_in_semester = [c for c in courses if x[c][s].value() == 1]
    if courses_in_semester:
        print(f"\n{s}º Semestre ({len(courses_in_semester)} matérias):")
        for c in courses_in_semester:
            print(f"  - {c}: {course_names[c]}")

model.writeLP("grade_curricular.lp")
