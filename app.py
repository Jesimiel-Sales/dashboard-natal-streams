# app.py - Dashboard de Streams Natalinos
# Funciona em qualquer Linux com Python 3.8+
# Apenas para verificação de alteração com commit e push

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ================== 1. CRIANDO OS DADOS ==================
# Lista de anos de 2016 a 2026
anos = list(range(2016, 2027))  # [2016, 2017, ..., 2026]

# Streams da Mariah Carey (em milhões)
# Dados simulados baseados em tendências reais
mariah_streams = [
    28, 32, 38, 45, 52,          # 2016-2020
    68, 85, 110, 142, 178, 210    # 2021-2026
]

# Streams do George Michael (mais estável)
george_streams = [
    42, 45, 48, 51, 54,           # 2016-2020
    58, 61, 64, 67, 70, 73        # 2021-2026
]

# Criar DataFrame (tabela no pandas)
dados = pd.DataFrame({
    'ano': anos,
    'Mariah Carey': mariah_streams,
    'George Michael': george_streams
})

# Transformar para formato "longo" (ideal para gráficos do plotly)
# melt = derrete a tabela larga em longa
dados_long = dados.melt(id_vars=['ano'], 
                        var_name='artista', 
                        value_name='streams_milhoes')

# ================== 2. DASHBOARD ==================
# Inicializar o app Dash
app = Dash(__name__)

# Layout visual - tudo que aparece na tela
app.layout = html.Div([
    # Título principal
    html.H1("🎄 Guerra do Natal nos Streamings (2016–2026)", 
            style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Subtítulo
    html.H3(f"Comparação: Mariah Carey vs George Michael - Dezembro de cada ano",
            style={'textAlign': 'center', 'color': '#7f8c8d'}),
    
    # Linha separadora
    html.Hr(),
    
    # Dropdown para escolher visualização
    html.Label("Escolha o tipo de gráfico:", style={'fontSize': '18px', 'fontWeight': 'bold'}),
    dcc.Dropdown(
        id='tipo_grafico',
        options=[
            {'label': '📊 Barras agrupadas', 'value': 'bar'},
            {'label': '📈 Linhas', 'value': 'line'},
            {'label': '🔵 Área empilhada', 'value': 'area'}
        ],
        value='bar',  # valor padrão
        clearable=False,
        style={'width': '60%', 'marginBottom': '20px', 'marginTop': '10px'}
    ),
    
    # Gráfico interativo
    dcc.Graph(id='grafico_streams'),
    
    # Linha separadora
    html.Hr(),
    
    # Tabela resumo (estilo simples em HTML)
    html.H4("📋 Tabela completa (streams em milhões)", 
            style={'textAlign': 'center'}),
    html.Table([
        html.Thead(html.Tr([html.Th("Ano", style={'padding': '10px'}), 
                           html.Th("Mariah Carey", style={'padding': '10px'}), 
                           html.Th("George Michael", style={'padding': '10px'})]))
    ] + [
        html.Tr([html.Td(ano, style={'padding': '8px', 'textAlign': 'center'}), 
                html.Td(m, style={'padding': '8px', 'textAlign': 'center'}), 
                html.Td(g, style={'padding': '8px', 'textAlign': 'center'})]) 
        for ano, m, g in zip(anos, mariah_streams, george_streams)
    ], style={'border': '1px solid #ddd', 'margin': 'auto', 'width': '80%', 
              'borderCollapse': 'collapse'})
])

# ================== 3. INTERATIVIDADE (CALLBACK) ==================
# Decorate a função com callback do Dash
@app.callback(
    Output('grafico_streams', 'figure'),  # O que será atualizado
    Input('tipo_grafico', 'value')        # O que dispara a atualização
)
def atualizar_grafico(tipo):
    """Função que atualiza o gráfico baseado no dropdown"""
    
    if tipo == 'bar':
        fig = px.bar(dados_long, x='ano', y='streams_milhoes', color='artista',
                     barmode='group',
                     title='Streams em dezembro (milhões)',
                     labels={'streams_milhoes': 'Streams (milhões)', 'ano': 'Ano'})
    elif tipo == 'line':
        fig = px.line(dados_long, x='ano', y='streams_milhoes', color='artista',
                      markers=True,
                      title='Evolução dos streams em dezembro',
                      labels={'streams_milhoes': 'Streams (milhões)', 'ano': 'Ano'})
    else:  # area
        fig = px.area(dados_long, x='ano', y='streams_milhoes', color='artista',
                      title='Streams acumulados em dezembro',
                      labels={'streams_milhoes': 'Streams (milhões)', 'ano': 'Ano'})
    
    # Melhorar aparência do gráfico
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        title_x=0.5,  # centralizar título
        font=dict(size=12)
    )
    
    return fig

# ================== 4. RODAR O SERVIDOR ==================
if __name__ == '__main__':
    # debug=True permite hot-reload e mostra erros no navegador
    # host='0.0.0.0' permite acessar de outros dispositivos na rede
    app.run(debug=True, host='127.0.0.1', port=8050)
