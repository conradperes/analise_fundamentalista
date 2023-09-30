import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import yfinance as yf
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Crie um aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1('Dashboard de Ações'),

    dcc.Input(id='stock-input', type='text', value='BTC-USD', debounce=True),

    dcc.Graph(id='stock-graph', config={'displayModeBar': False})  # Remover barra de modo de exibição
])

# Função para obter dados de ações
def get_stock_data(stock_symbol):
    stock_data = yf.Ticker(stock_symbol)
    df = stock_data.history(period='2y', interval='1d')
    return df

# Callback para atualizar o gráfico com base no símbolo da ação inserido
@app.callback(Output('stock-graph', 'figure'), [Input('stock-input', 'value')])
def update_stock_graph(stock_symbol):
    #df = QueryInflux.get_dataframeByBucketInflux(stock_symbol.upper())
    df = get_stock_data(stock_symbol.upper())
    # Crie um gráfico de linha moderno com grid visível
    figure = {
        'data': [
            go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                marker=dict(color='blue'),  # Cor das linhas
                name=stock_symbol
            )
        ],
        'layout': {
            'title': f'Preço da Ação {stock_symbol}',
            'xaxis': {
                'title': 'Tempo',
                'color': 'black',  # Cor do texto no eixo x
                'showgrid': True,  # Exibir grades no eixo x
                'gridcolor': 'lightgray'  # Cor das grades no eixo x
            },
            'yaxis': {
                'title': 'Preço',
                'color': 'black',  # Cor do texto no eixo y
                'showgrid': True,  # Exibir grades no eixo y
                'gridcolor': 'lightgray'  # Cor das grades no eixo y
            },
            'plot_bgcolor': 'white',  # Fundo branco do gráfico
            'paper_bgcolor': 'white',  # Fundo branco do painel
            'font': {
                'color': 'black'  # Cor do texto
            },
            'template': 'plotly'  # Esquema de cores moderno
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
