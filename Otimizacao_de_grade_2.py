import pulp

def is_even(number):
    return number % 2 == 0
# ===============================================================
# DEFINIÇÃO DOS DADOS DO PROBLEMA
# ===============================================================

# Lista completa de disciplinas do curso
# Cada código representa uma matéria da matriz curricular.
courses = [
    'ENGF56', 'MATA01', 'MATA02', 'ENGD01', 'FIS121', 'MATA03', 'ENG041', 
    'ENGD02', 'MATA07', 'QUIB50', 'ECO151', 'FIS122', 'MATA04', 'ENG207', 
    'ENG269', 'ENGF81', 'ENGF90', 'ENGF77', 'ENGF78', 'ENGF80', 'ENGF82', 
    'FCC024', 'DIR175', 'ENG308', 'ENGF79', 'ENGF86', 'OP1', 'ENG037', 
    'ENG040', 'ENG179', 'ENG430', 'ENGA62', 'ENG039', 'ENGF83', 'ENGF84', 
    'ENGF85', 'OP2', 'ENG432', 'ENGF88', 'FIS123', 'OP3', 'ENG003', 
    'ENGF89', 'OP4', 'OP5', 'ENGF87'
]

# Dicionário de pré-requisitos
# Exemplo: 'MATA03': ['MATA01', 'MATA02'] significa que MATA03 só pode ser cursada
# depois que MATA01 e MATA02 já tiverem sido alocadas em semestres anteriores.
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

# Dicionário apenas para exibir os nomes completos das disciplinas ao final
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

# Lista como cursos que são ofertados apenas em semestres pares
even_semesters_courses = ['ENGF77','ENGF78','ENGF80','ENG037','ENG040','ENG430','ENG432']

# Lista como cursos que são ofertados apenas em semestres impares
odd_semesters_courses = ['ENGF56','ENG207','ENGF90','ENG308','ENGF86','ENGF83','ENGF84','ENGF85']

# Disciplinas obrigatórias no primeiro semestre (definidas manualmente)
first_semester_courses = ['ENGF56', 'MATA01', 'MATA02']

# Disciplinas cursadas
coursed_courses = ['ENGF56', 'MATA01', 'MATA02', 'ENGD01', 'FIS121', 'MATA03', 'MATA07']

# Disciplinas remanecentes
courses = list(set(courses) - set(coursed_courses))



# Definição dos semestres disponíveis (1º ao 12º)
semesters = list(range(1, 13))

# Número máximo de disciplinas permitidas em um mesmo semestre
max_courses_per_semester = 6


# ===============================================================
# CRIAÇÃO DO MODELO DE OTIMIZAÇÃO
# ===============================================================

# O modelo será de Minimização (pois queremos reduzir o número de semestres)
model = pulp.LpProblem('GradeCurricular', pulp.LpMinimize)

# Variáveis binárias de decisão
# x[c][s] = 1 se o curso c for alocado no semestre s, e 0 caso contrário
x = pulp.LpVariable.dicts('x', (courses, semesters), cat='Binary')


# ===============================================================
# RESTRIÇÕES DO MODELO
# ===============================================================

# 1. Cada disciplina deve ser alocada em exatamente UM semestre
# (garante que o curso não apareça duplicado ou seja ignorado)
for c in courses:
    model += pulp.lpSum(x[c][s] for s in semesters) == 1


# 2. Fixar disciplinas obrigatórias do 1º semestre
# (essas matérias são pré-definidas na matriz curricular)
for c in first_semester_courses:
    model += x[c][1] == 1


# 3. Garantir que apenas essas disciplinas estejam no 1º semestre
# (impede o solver de colocar outras matérias junto delas)
model += pulp.lpSum(x[c][1] for c in courses) == len(first_semester_courses)


# 4. Limitar a quantidade máxima de disciplinas por semestre
# (controla a carga de cada período, exceto o 1º que é fixo)
for s in semesters:
    if s > 1:
        model += pulp.lpSum(x[c][s] for c in courses) <= max_courses_per_semester


# 5. Restrições de pré-requisitos
# Para cada disciplina com dependências, o modelo garante que ela só poderá
# ser alocada em um semestre posterior ao de seus pré-requisitos.
# Formalmente: x[curso][s] <= soma(x[prereq][t] para t < s)
for course, prereq_list in prereqs.items():
    for prereq in prereq_list:
        for s in semesters:
            model += x[course][s] <= pulp.lpSum(x[prereq][t] for t in semesters if t < s)

# 6. Restrições de materias que são ofertadas apenas em semestres pares ou impares
for c in courses:
    if c in even_semesters_courses:
        model += pulp.lpSum(x[c][s] for s in semesters if is_even(s)) == 1
    elif c in odd_semesters_courses:
        model += pulp.lpSum(x[c][s] for s in semesters if not is_even(s)) == 1
    else:
        pass


# ===============================================================
# FUNÇÃO OBJETIVO
# ===============================================================

# Variável auxiliar que representa o último semestre em que alguma disciplina foi alocada.
last_semester = pulp.LpVariable('ultimo_semestre', lowBound=1, upBound=max(semesters), cat='Integer')

# Essa relação força o "último semestre" a ser maior ou igual
# ao semestre de qualquer disciplina que foi alocada.
for c in courses:
    for s in semesters:
        model += last_semester >= s * x[c][s]

# O objetivo é minimizar o número total de semestres necessários
model += last_semester


# ===============================================================
# RESOLUÇÃO DO MODELO
# ===============================================================

model.solve()

# ===============================================================
# RESULTADOS
# ===============================================================

print("Status:", pulp.LpStatus[model.status])
print(f"\nCurso concluído em {int(last_semester.value())} semestres\n")
print("Grade Curricular Ótima:\n")

# Exibe as disciplinas alocadas em cada semestre
for s in semesters:
    courses_in_semester = [c for c in courses if x[c][s].value() == 1]
    if courses_in_semester:
        print(f"\n{s}º Semestre ({len(courses_in_semester)} matérias):")
        for c in courses_in_semester:
            print(f"  - {c}: {course_names[c]}")
