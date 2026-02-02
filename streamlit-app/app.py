import streamlit as st
import pandas as pd
import pulp
import re
from datetime import datetime
import json
from decimal import Decimal

from functions import *

ss = st.session_state

st.set_page_config(page_title="Otimizador de Grade", initial_sidebar_state="collapsed", layout="wide", page_icon="📑")

if "page" not in ss:
    ss.page = "inicio"

if "grade" not in ss:
    ss.grade = []

ss.first_semester = ['ENGF56', 'MATA01', 'MATA02']

if "courses" not in ss:
    ss.courses = [
        'ENGF56', 'MATA01', 'MATA02', 'ENGD01', 'FIS121', 'MATA03', 'ENG041', 
        'ENGD02', 'MATA07', 'QUIB50', 'ECO151', 'FIS122', 'MATA04', 'ENG207', 
        'ENG269', 'ENGF81', 'ENGF90', 'ENGF77', 'ENGF78', 'ENGF80', 'ENGF82', 
        'FCC024', 'DIR175', 'ENG308', 'ENGF79', 'ENGF86', 'OP1', 'ENG037', 
        'ENG040', 'ENG179', 'ENG430', 'ENGA62', 'ENG039', 'ENGF83', 'ENGF84', 
        'ENGF85', 'OP2', 'ENG432', 'ENGF88', 'FIS123', 'OP3', 'ENG003', 
        'ENGF89', 'OP4', 'OP5', 'ENGF87'
    ]

if "prereqs" not in ss:
    ss.prereqs = {
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
        'ENGF79': ['MATA02', 'QUIB50', "MATA04", "ENGD01", "ENGF78", "FIS123"],
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

if "course_names" not in ss:
    ss.course_names = {
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

if "even_semester_courses" not in ss:
    ss.even_semesters_courses = ['ENGF77','ENGF78','ENGF80','ENG040','ENG430','ENG432']
if "odd_semester_courses" not in ss:
    ss.odd_semesters_courses = ['ENGF56','ENG207','ENGF90','ENG308','ENGF86','ENGF83','ENGF84','ENGF85']

if "completed_courses" not in ss:
    ss.completed_courses = []

if "course_levels" not in ss:
    ss.course_levels = {
        'ENGF56': 1,
        'MATA01': 2,
        'MATA02': 4,

        'ENGD01': 2,
        'FIS121': 3,
        'MATA03': 4,

        'ENG041': 5,
        'ENGD02': 2,
        'MATA07': 4,
        'QUIB50': 3,

        'ECO151': 1,
        'FIS122': 3,
        'MATA04': 3,

        'ENG207': 1,
        'ENG269': 1,
        'ENGF81': 2,
        'ENGF90': 4,

        'ENGF77': 1,
        'ENGF78': 3,
        'ENGF80': 2,
        'ENGF82': 3,
        'FCC024': 1,

        'DIR175': 1,
        'ENG308': 2,
        'ENGF79': 5,
        'ENGF86': 3,
        'OP1': 1,  

        'ENG037': 3,
        'ENG040': 1,
        'ENG179': 4,
        'ENG430': 3,
        'ENGA62': 3,

        'ENG039': 4,
        'ENGF83': 2,
        'ENGF84': 4,
        'ENGF85': 2,
        'OP2': 1,  

        'ENG432': 3,
        'ENGF88': 3,
        'FIS123': 4,
        'OP3': 1,  

        'ENG003': 3,
        'ENGF89': 5,
        'OP4': 1,
        'OP5': 1,

        'ENGF87': 1,
    }

if "max_level" not in ss:
    ss.max_level = 14

if "current_semester_is_even" not in ss:
    ss.current_semester_is_even = False

with open("horarios_impar.json", "r", encoding="utf-8") as f:
    horarios_impar_raw = json.load(f)

with open("horarios_par.json", "r", encoding="utf-8") as f:
    horarios_par_raw = json.load(f)

horarios_impar = {c: [norm_h(h) for h in hs] for c, hs in horarios_impar_raw.items()}
horarios_par   = {c: [norm_h(h) for h in hs] for c, hs in horarios_par_raw.items()}

if ss.page == "inicio":
    st.markdown(f"""
        <h1 style='text-align: left; margin: 0;'>Gerador de Grade Ótima</h1>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.write("**Selcione o semestre atual:**")

        semestre_atual = f"{datetime.now().year}.{2 if datetime.now().month >= 8 else 1}"

        entrada = st.text_input("", max_chars=6, placeholder="Digite o período (ex: 2025.1)", label_visibility="hidden", value=semestre_atual)

        padrao = r"^\d{4}\.(1|2)$"

        if entrada:
            if not re.match(padrao, entrada):
                st.error("Formato inválido, use YYYY.1 ou YYYY.2")
                ss.allow = False
            else:
                ss.current_semester_is_even = entrada.split(".")[1] == "2"
                ss.allow = True

        st.write("**Selcione as matérias já cursadas:**")

        with st.container(border=True):
            s1 = st.segmented_control(
                "Primeiro Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENGF56", "MATA01", "MATA02"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s2 = st.segmented_control(
                "Segundo Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENGD01", "FIS121", "MATA03"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s3 = st.segmented_control(
                "Terceiro Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENG041", "ENGD02", "MATA07", "QUIB50"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s4 = st.segmented_control(
                "Quarto Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ECO151", "FIS122", "MATA04"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s5 = st.segmented_control(
                "Quinto Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENG207", "ENG269", "ENGF81", "ENGF90"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s6 = st.segmented_control(
                "Sexto Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENGF77", "ENGF78", "ENGF80", "ENGF82", "FCC024"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s7 = st.segmented_control(
                "Sétimo Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["DIR175", "ENG308", "ENGF79", "ENGF86"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s8 = st.segmented_control(
                "Oitavo Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENG037", "ENG040", "ENG179", "ENG430", "ENGA62"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s9 = st.segmented_control(
                "Nono Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENG039", "ENGF83", "ENGF84", "ENGF85"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            s10 = st.segmented_control(
                "Décimo Semestre:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENG432", "FIS123", "ENG003"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            opt = st.segmented_control(
                "Optativas:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["OP1", "OP2", "OP3", "OP4", "OP5"]],
                selection_mode="multi"
            )

        with st.container(border=True):
            tcc = st.segmented_control(
                "Estágio e TCC:", 
                [f"{k}: {v}" for k, v in ss.course_names.items() if k in ["ENGF87", "ENGF88", "ENGF89"]],
                selection_mode="multi"
            )

        ss.completed_courses = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + s10 + opt + tcc

        ss.completed_courses = [c.split(":")[0] for c in ss.completed_courses]

        max_materias = st.number_input("Máximo de matérias por semestre:", min_value=1, max_value=10, value=5, placeholder="Selecione o máximo de matérias por semestre")

        ss.max_courses_per_semester = max_materias

        options = ["Fácil", "Normal", "Difícil"]

        dificuldade = st.segmented_control(
            "Dificuldade",
            options,
            selection_mode="single",
            default="Normal"
        )
        if dificuldade == None:
            ss.allow_d = False
        else:
            ss.allow_d = True
            if dificuldade == "Fácil":
                ss.max_level = 10
            elif dificuldade == "Normal":
                ss.max_level = 14
            elif dificuldade == "Difícil":
                ss.max_level = 99

        submitted = st.button("Gerar Grade")
        if submitted:
            if ss.allow == True and ss.allow_d == True:
                ss.grade = resolve_model(
                    ss.courses,
                    ss.prereqs,
                    ss.course_names,
                    ss.even_semesters_courses,
                    ss.odd_semesters_courses,
                    ss.max_courses_per_semester,
                    ss.completed_courses,
                    ss.first_semester,
                    ss.course_levels,
                    ss.max_level
                )
                ss.page = "resolucao"
                st.rerun()
            else:
                st.error("Revise as informações inseridas")

if ss.page == "resolucao":

    col1, col2 = st.columns([6, 1])

    with col1:
        st.markdown(f"""
            <h1 style='text-align: left; margin: 0;'>Gerador de Grade Ótima</h1>
        """, unsafe_allow_html=True)

    with col2:
        voltar = st.button("Gerar nova grade")
        if voltar:
            ss.page = "inicio"
            st.rerun()

    for s in sorted(ss.grade["semester"].unique()):
        st.markdown(f"## 🕓 Semestre {s}")
        df_sem = ss.grade[ss.grade["semester"] == s]
        courses_in_semester = df_sem["course"].tolist()

        col_left, col_right = st.columns([2, 3], gap="large")

        # =========================
        # Coluna esquerda: lista
        # =========================
        with col_left:
            for _, row in df_sem.iterrows():
                st.markdown(f"""
                <div style="
                    border-left: 3px solid #4A90E2;
                    padding-left: 12px;
                    margin-bottom: 12px;
                ">
                    <b>{row['course']}</b> - {row['course_name']}
                </div>
                """, unsafe_allow_html=True)

        # =========================
        # Coluna direita: calendário
        # =========================
        with col_right:
            st.markdown("### Matérias com Horários Fixos")

            horarios_semestre = horarios_par if (s % 2 == 0) else horarios_impar
            df_cal = build_schedule_df(
                courses_in_semester=courses_in_semester,
                horarios_semestre=horarios_semestre,
                course_names=ss.course_names
            )

            if df_cal is None:
                st.caption("Nenhuma disciplina com horário fixo neste semestre.")
            else:
                # st.dataframe fica bem prático e já parece uma “tabela” tipo a imagem
                st.dataframe(df_cal, use_container_width=True)