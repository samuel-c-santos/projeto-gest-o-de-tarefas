import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from PIL import Image

# Caminhos dos arquivos
task_file_path = 'C:\\Users\\usuario\\Documents\\DASHBOARD TERRARE\\NOVAS BASES\\GESTÃO DE TAREFAS.xlsx'
tech_file_path = 'C:\\Users\\usuario\\Documents\\DASHBOARD TERRARE\\NOVAS BASES\\corpo_tecnico_geomap.xlsx'
logo_path = 'C:\\Users\\usuario\\Documents\\DASHBOARD TERRARE\\LOGOMARCA-20240327T194240Z-001\\LOGOMARCA\\GEOMAP - Consultoria Ambiental e Fundiária_Prancheta 1 cópia 35.png'

# Verificação se o arquivo da logomarca existe
if not os.path.exists(logo_path):
    st.error(f"Logomarca não encontrada no caminho: {logo_path}")
else:
    try:
        logo = Image.open(logo_path)
        # Reduzir a resolução da imagem se necessário
        logo.thumbnail((300, 300))  # Reduzir para um máximo de 300x300 pixels
        st.sidebar.image(logo, use_column_width=True)
    except Exception as e:
        st.error(f"Erro ao carregar a logomarca: {e}")

# Estilos customizados
st.markdown(f"""
    <style>
    .reportview-container .main .block-container {{
        padding: 1rem; /* Reduzir o padding para diminuir os espaços laterais */
        max-width: 1200px;
        margin: auto;
    }}
    .css-6qob1r {{
        background-color: #4d7055 !important;
        color: white !important;
    }}
    .css-6qob1r a {{
        color: white !important;
    }}
    .css-6qob1r .block-container {{
        color: white !important;
    }}
    .css-6qob1r .block-container div {{
        color: white !important;
    }}
    .css-6qob1r .block-container div a {{
        color: white !important;
    }}
    .css-6qob1r img {{
        max-width: 100%;
        height: auto;
    }}
    .css-16idsys eqr7zpz4 p {{
        color: white !important;
    }}
    .css-1nm2qww {{
        color: white !important;
    }}
    .css-1nm2qww div {{
        color: white !important;
    }}
    .st-bf {{
        color: white !important;
    }}
    .css-18e3th9 {{
        background-color: #4d7055;
        color: white;
    }}
    .css-18e3th9 a {{
        color: white;
    }}
    .css-18e3th9 .block-container {{
        color: white;
    }}
    .css-18e3th9 .block-container div {{
        color: white;
    }}
    .css-18e3th9 .block-container div a {{
        color: white;
    }}
    .css-18e3th9 img {{
        max-width: 100%;
        height: auto;
    }}
    input, select, textarea {{
        color: #333333 !important; /* Cinza escuro */
    }}
    .css-1cpxqw2 {{
        color: #333333 !important; /* Cinza escuro para texto de input */
    }}
    .css-2b097c-container {{
        color: #333333 !important; /* Cinza escuro para selects */
    }}
    .main .block-container {{
        max-width: 100% !important; /* Tornar o layout mais largo */
        padding-left: 5rem; /* Ajustar padding para centralizar */
        padding-right: 5rem; /* Ajustar padding para centralizar */
    }}
    h1 {{
        font-size: 2rem !important;
    }}
    h2 {{
        font-size: 1.5rem !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Interface Streamlit
st.title('Gestão de Tarefas')

# Carregar os dados
task_data = pd.read_excel(task_file_path)
tech_data = pd.read_excel(tech_file_path)

# Função para definir a cor da prioridade
def get_priority_color(priority):
    if priority == "Baixa":
        return "#40c5af"  # Verde
    elif priority == "Importante":
        return "#ffc83d"  # Amarelo
    elif priority == "Urgente":
        return "#ef6950"  # Vermelho
    else:
        return "#FFFFFF"  # Branco como padrão

# Função para exibir tarefas
def display_tasks(tasks, status, search_text, filter_overdue, code_search_text):
    filtered_tasks = tasks[(tasks['Status'] == status) & (tasks['Nome da Tarefa'].str.contains(search_text, case=False, na=False))]
    if filter_overdue:
        today = date.today()
        filtered_tasks = filtered_tasks[filtered_tasks['Prazo'].apply(lambda x: pd.notna(x) and x.date() < today and status != 'Concluído')]
    if code_search_text:
        filtered_tasks = filtered_tasks[filtered_tasks['Código da Tarefa'].str.contains(code_search_text, case=False, na=False)]
        
    for index, task in filtered_tasks.iterrows():
        color = get_priority_color(task['Prioridade'])
        if pd.isna(task['Prazo']):
            task_due_date = "Sem prazo definido"
            overdue_text = ""
        else:
            task_due_date = task['Prazo'].strftime('%d/%m/%Y')
            today = date.today()
            if task['Prazo'].date() < today and task['Status'] != 'Concluído':
                overdue_text = ' <span style="color:red;">*prazo vencido</span>'
            elif task['Prazo'].date() == today:
                overdue_text = ' <span style="color:orange;">*vence hoje</span>'
            else:
                overdue_text = ''
        st.markdown(f"""
            <div style="border: 1px solid {color}; border-left: 8px solid {color}; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: white; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                <strong>{task['Nome da Tarefa']}</strong><br>
                <hr>
                <strong>Responsável:</strong> {task['Responsável']}<br>
                <strong>Setor:</strong> {task['Setor']}<br>
                <strong>Descrição da tarefa:</strong> {task['Descrição da tarefa']}<br>
                <strong>Código da Tarefa:</strong> {task['Código da Tarefa']}<br>
                <strong>Prazo:</strong> {task_due_date}{overdue_text}
            </div>
        """, unsafe_allow_html=True)

# Função para gerar o código da tarefa
def generate_task_code(data, setor, responsavel):
    date_str = data.strftime("%d%m%y")
    setor_str = setor[:3].upper()
    responsavel_str = responsavel.split(",")[0][:4].upper()
    count = len(task_data[task_data['Código da Tarefa'].str.contains(f"{date_str}{setor_str}{responsavel_str}")])
    code = f"{date_str}{setor_str}{responsavel_str}-{count:03d}"
    return code

# Navegação por abas
selected_tab = st.sidebar.radio("Ir para", ["Tarefas", "Cadastrar tarefa", "Editar tarefa"])

# Tarefas
if selected_tab == "Tarefas":
    # Tratar valores nulos na coluna 'Responsável'
    task_data['Responsável'] = task_data['Responsável'].fillna('')

    # Filtros
    funcionarios = st.selectbox('Funcionário', options=['Todos'] + list(set([resp.strip() for sublist in task_data['Responsável'].str.split(',') for resp in sublist if resp])))
    prioridade = st.selectbox('Prioridade', options=['Todos'] + list(task_data['Prioridade'].unique()))
    search_text = st.text_input('Buscar tarefa por nome', '')
    filter_overdue = st.checkbox('Mostrar apenas tarefas com prazo vencido')
    code_search_text = st.text_input('Buscar por Código da Tarefa', '')

    # Filtrando dados
    filtered_data = task_data
    if funcionarios != 'Todos':
        filtered_data = filtered_data[filtered_data['Responsável'].str.contains(funcionarios)]
    if prioridade != 'Todos':
        filtered_data = filtered_data[filtered_data['Prioridade'] == prioridade]

    # Exibir tarefas com barra de rolagem
    st.markdown("""
        <style>
        .scrollable-container {
            max-height: 400px;
            overflow-y: auto;
        }
        </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Não iniciadas')
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            display_tasks(filtered_data, 'Não iniciado', search_text, filter_overdue, code_search_text)
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.header('Em andamento')
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            display_tasks(filtered_data, 'Em andamento', search_text, filter_overdue, code_search_text)
            st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.header('Concluídas')
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            display_tasks(filtered_data, 'Concluído', search_text, filter_overdue, code_search_text)
            st.markdown('</div>', unsafe_allow_html=True)

# Cadastrar tarefa
elif selected_tab == "Cadastrar tarefa":
    st.header('Adicionar Nova Tarefa')
    new_task = {}
    new_task['Setor'] = st.selectbox('Setor', ['Ambiental', 'Fundiário'])
    new_task['Nome da Tarefa'] = st.text_input('Nome da Tarefa')
    new_task['Responsável'] = st.multiselect('Responsável (separar múltiplos nomes por vírgula)', options=tech_data['Responsável'].dropna().unique().tolist())
    new_task['Prazo'] = st.date_input('Prazo')
    new_task['Prioridade'] = st.selectbox('Prioridade', ['Baixa', 'Importante', 'Urgente'])
    new_task['Status'] = st.selectbox('Status', ['Não iniciado', 'Em andamento', 'Concluído'])
    new_task['Descrição da tarefa'] = st.text_area('Descrição da tarefa')
    new_task['Observações'] = st.text_area('Observações')
    new_task['Data da Conclusão'] = st.date_input('Data da Conclusão', key='data_conclusao')
    
    if st.button('Adicionar Tarefa'):
        new_task['Responsável'] = ', '.join(new_task['Responsável'])
        new_task['Código da Tarefa'] = generate_task_code(new_task['Prazo'], new_task['Setor'], new_task['Responsável'])
        task_data = pd.concat([task_data, pd.DataFrame([new_task])], ignore_index=True)
        task_data.to_excel(task_file_path, index=False)  # Salvar mudanças na base de dados
        st.success('Tarefa adicionada com sucesso!')
        # Limpar campos de entrada
        st.experimental_rerun()

# Editar tarefas
elif selected_tab == "Editar tarefa":
    st.header('Editar Tarefa')
    codigo_tarefa = st.text_input('Código da Tarefa para editar')
    if codigo_tarefa:
        task_to_edit = task_data[task_data['Código da Tarefa'] == codigo_tarefa]
        if not task_to_edit.empty:
            task_to_edit = task_to_edit.iloc[0]
            new_setor = st.selectbox('Setor', ['Ambiental', 'Fundiário'], index=['Ambiental', 'Fundiário'].index(task_to_edit['Setor']))
            new_nome = st.text_input('Nome da Tarefa', task_to_edit['Nome da Tarefa'])
            new_responsavel = st.multiselect('Responsável', options=tech_data['Responsável'].dropna().unique().tolist(), default=task_to_edit['Responsável'].split(', '))
            prazo = task_to_edit['Prazo']
            new_prazo = st.date_input('Prazo', value=pd.to_datetime(prazo) if pd.notnull(prazo) else datetime.today())
            new_prioridade = st.selectbox('Prioridade', ['Baixa', 'Importante', 'Urgente'], index=['Baixa', 'Importante', 'Urgente'].index(task_to_edit['Prioridade']))
            new_status = st.selectbox('Status', ['Não iniciado', 'Em andamento', 'Concluído'], index=['Não iniciado', 'Em andamento', 'Concluído'].index(task_to_edit['Status']))
            new_descricao = st.text_area('Descrição da tarefa', task_to_edit['Descrição da tarefa'])
            new_observacoes = st.text_area('Observações', task_to_edit['Observações'])
            data_conclusao = task_to_edit['Data da Conclusão']
            new_data_conclusao = st.date_input('Data da Conclusão', value=pd.to_datetime(data_conclusao) if pd.notnull(data_conclusao) else datetime.today(), key='data_conclusao_edit')

            if st.button('Salvar Alterações'):
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Setor'] = new_setor
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Nome da Tarefa'] = new_nome
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Responsável'] = ', '.join(new_responsavel)
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Prazo'] = new_prazo
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Prioridade'] = new_prioridade
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Status'] = new_status
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Descrição da tarefa'] = new_descricao
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Observações'] = new_observacoes
                task_data.loc[task_data['Código da Tarefa'] == codigo_tarefa, 'Data da Conclusão'] = new_data_conclusao
                task_data.to_excel(task_file_path, index=False)  # Salvar mudanças na base de dados
                st.success('Tarefa editada com sucesso!')
        else:
            st.error('Código da Tarefa não encontrado.')
