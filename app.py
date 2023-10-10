import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


st.set_page_config(page_title="Pizzaria") #Troca o título da página

#extraindo os dados e convertendo em um df
df_pizza = pd.read_csv('pizzas.csv',delimiter=",")
df_pizza_type = pd.read_csv('pizza_types.csv',delimiter=",")
df_orders = pd.read_csv('orders.csv',delimiter=",")
df_details = pd.read_csv('order_details.csv',delimiter=",")

#criação de novos df
df_orders['date'] = pd.to_datetime(df_orders['date'], format='%Y-%m-%d').dt.date
df_orders['month'] = pd.to_datetime(df_orders['date']).dt.month_name()
df_orders['day of the week'] = pd.to_datetime(df_orders['date'],format='%Y-%m-%d').dt.day_name()
df_orders['day'] = pd.to_datetime(df_orders['date'],format='%Y-%m-%d').dt.day 
df_orders['hour'] = pd.to_datetime(df_orders['time'], format='%H:%M:%S').dt.hour
aux = pd.merge(df_details, df_orders, on='order_id', how='left') #concatena dois df baseado na abordagem left
aux2 = pd.merge(aux, df_pizza, on='pizza_id', how='left')
data_final = pd.merge(aux2, df_pizza_type, on='pizza_type_id', how='left')

def calcularTotal(x,y):
	lista = []
	filtrar = set(x)
	filtrar = list(filtrar)
	for i in range(len(filtrar)):
		contad = 0
		for k in range(len(x)):
			if filtrar[i] == x[k]:
				contad += y[k]
		lista.append(contad)
	return filtrar, lista

def calcularValorTotal(x,y,z):
	lista = []
	filtrar = set(x)
	filtrar = list(filtrar)
	for i in range(len(filtrar)):
		contad = 0
		for k in range(len(x)):
			if filtrar[i] == x[k]:
				contad += y[k]*z[k]
		lista.append(contad)
	return filtrar, lista


def diaPicoSemana(lista,nome_df,df_dia,nome_order,nome_data):
    lista_soma = []
    for i in range(len(lista)):
        dia_semana = nome_df[df_dia==lista[i]]
        soma_pedidos = dia_semana[nome_order].nunique()
        soma_dias = dia_semana[nome_data].nunique()
        soma_pedidos = soma_pedidos/soma_dias
        lista_soma.append(soma_pedidos)
    dic = {'Dia': lista,'Pedidos': lista_soma}
    dic = pd.DataFrame(dic)
    return dic

def InfoPedidosporHora(data_selecionada,df_data,df_idpedido,df_hora):
    lista1 = []
    lista2 = []
    for i in range(len(df_data)):
        if df_data[i] == data_selecionada and df_idpedido[i] not in lista1:
            lista1.append(df_idpedido[i])
            lista2.append(df_hora[i])
    dic = {'Hora': lista2, 'ID': lista1}
    df = pd.DataFrame(dic)
    lista2 = set(lista2)
    lista2 = list(lista2)
    return df, lista2

def PedidosporHora(df_IPH,lista_IPH):
    lista3 = []
    for i in range(len(lista_IPH)):
        acumulador = 0
        for j in range(len(df_IPH['Hora'])):
            if lista_IPH[i] == df_IPH['Hora'][j]:
                acumulador+= 1
        lista3.append(acumulador)
    dic = {'Horas':lista_IPH, 'Nº Pedidos': lista3}
    dic = pd.DataFrame(dic)
    return dic

def PizzaFav(meses,nome_df,nome_mes,pizza_name):
    lista1 = []
    lista2 = []
    for i in range(len(meses)):
        fg = nome_df.loc[nome_df[nome_mes] == meses[i]]
        df = fg[pizza_name].value_counts()
        lista1.append(df.index[0])
        lista2.append(df.iloc[0])
    return lista1, lista2

st.title('DADOS PIZZARIA')

colunas = ['Categorias Mais Consumidas','Pizzas Mais Consumidas no Total','Tamanhos Mais Pedidos','Dinheiro Adquirido no Total por Categoria','Média de Consumo em Cada Dia da Semana','Dinheiro Obtido a partir de Cada Mês','Horário de pico','Pizza Favorita de Cada Mês','Quantidade de pizzas solicitadas']
column = st.sidebar.selectbox('Qual tipo de informação?', colunas)

if column == 'Categorias Mais Consumidas':
    st.write('Porcentagem da Categoria por Quantidade Total Consumida.')
    lista,total = calcularTotal(data_final['category'],data_final['quantity'])
    df = {'Categorias':lista,'Quantidade':total}
    df = pd.DataFrame(df)
    df = df.sort_values(by='Quantidade', ascending=True)
    plt.figure(figsize=(3, 3))
    plt.pie(df['Quantidade'], labels=df['Categorias'], autopct='%1.1f%%', startangle=140)
    st.pyplot(plt)

elif column == 'Pizzas Mais Consumidas no Total':
    st.write('Quantidade Total de Cada Tipo de Pizza Consumida.')
    cores = ['red', 'green', 'blue', 'purple']
    lista,total = calcularTotal(data_final['name'],data_final['quantity'])
    df = {'Tipos de Pizza':lista,'Quantidade':total}
    df = pd.DataFrame(df)
    df = df.sort_values(by='Quantidade', ascending=True)
    plt.figure(figsize=(30,40))
    plt.barh(df['Tipos de Pizza'], df['Quantidade'],color=cores)
    plt.xlabel('Quantidade', fontsize=60)
    plt.xticks(rotation=90)
    plt.xticks(fontsize=70)
    plt.ylabel('Tipos de Pizza', fontsize=60)
    plt.yticks(fontsize=70)
    st.pyplot(plt)

elif column == 'Tamanhos Mais Pedidos':
    st.write('Quantidade de Pizzas Consumidas por Tamanho.')
    lista,total = calcularTotal(data_final['size'],data_final['quantity'])
    df = {'Tamanhos':lista,'Quantidade':total}
    df = pd.DataFrame(df)
    df = df.sort_values(by='Quantidade', ascending=True)
    plt.figure(figsize=(10,6))
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.bar(df['Tamanhos'], df['Quantidade'], color='purple')
    plt.xlabel('Tamanhos',fontsize=20)
    plt.ylabel('Quantidade',fontsize=20)
    st.pyplot(plt)

elif column == 'Dinheiro Adquirido no Total por Categoria':
    st.write('Dinheiro Adquirido no Total por Categoria.')
    lista,total = calcularValorTotal(data_final['category'],data_final['price'],data_final['quantity'])
    df = {'Categorias':lista,'Dinheiro Adquirido em Dólar':total}
    df = pd.DataFrame(df)
    df = df.sort_values(by='Categorias', ascending=True)
    plt.figure(figsize=(10,6))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.stem(df['Categorias'], df['Dinheiro Adquirido em Dólar'])
    plt.xlabel('Categorias',fontsize=10)
    plt.ylabel('Dinheiro Adquirido em Dólar',fontsize=10)
    st.pyplot(plt)

elif column == 'Média de Consumo em Cada Dia da Semana':
    st.write('Média de Consumo em Cada Dia da Semana.')
    dias = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    df = diaPicoSemana(dias,data_final,data_final['day of the week'],'order_id','date')
    plt.figure(figsize=(10,6))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.plot(df['Dia'], df['Pedidos'],linestyle = 'dashed')
    plt.xlabel('Dias')
    plt.ylabel('Pedidos')
    st.pyplot(plt)

elif column == 'Dinheiro Obtido a partir de Cada Mês':
    st.write('Dinheiro Obtido a partir de Cada Mês')
    mes = ['January','February','March','April','May','June','July','August','September','October','November','December']
    lista, total = calcularValorTotal(data_final['month'],data_final['price'],data_final['quantity'])
    df = {'Data':lista,'Valor':total}
    df = pd.DataFrame(df)
    df['coluna_de_ordenacao'] = pd.Categorical(df['Data'], categories=mes, ordered=True)
    df = df.sort_values(by='coluna_de_ordenacao')
    plt.figure(figsize=(10, 6))
    plt.plot(df['Data'], df['Valor'], marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('Data')
    plt.ylabel('Valor')
    st.pyplot(plt)

elif column == 'Horário de pico':
    data_minima = date(2015, 1, 1)
    data_maxima = date(2015, 12, 31)
    data_padrao = data_minima
    data_selecionada = data_padrao
    data_selecionada = st.sidebar.date_input("Selecione uma data:", min_value=data_minima, max_value=data_maxima, value=data_padrao)
    if data_selecionada in data_final['date'].values:
        st.write(f'Horário de pico do dia {data_selecionada}')
        dic_auxiliar, lista_auxiliar = InfoPedidosporHora(data_selecionada, data_final['date'], data_final['order_id'], data_final['hour'])
        df = PedidosporHora(dic_auxiliar,lista_auxiliar)
        plt.figure(figsize=(10, 6))
        plt.plot(df['Horas'], df['Nº Pedidos'], marker='o', linestyle='-', color='b', label='Dados')
        plt.xticks(df['Horas'],df['Horas'])
        plt.xlabel('Horas',fontsize=15)
        plt.ylabel('Quantidade de Pedidos',fontsize=15)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.legend()
        st.pyplot(plt)
    else:
        st.write('A Pizzaria não abriu neste dia.')

elif column == 'Pizza Favorita de Cada Mês':
    st.write('Pizza Favorita de Cada Mês.')
    meses = ['January','February','March','April','May','June','July','August','September','October','November','December']
    nome_pizza, quantidade = PizzaFav(meses,data_final,'month','name')
    dic = {'Mês':meses,'Quantidade':quantidade,'Pizza':nome_pizza}
    df = pd.DataFrame(dic)
    plt.figure(figsize=(10, 6))
    for pizza in df['Pizza'].unique():
        subset = df[df['Pizza'] == pizza]
        plt.bar(subset['Mês'], subset['Quantidade'], label=pizza)
    plt.xlabel('Mês')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)

elif column == 'Quantidade de pizzas solicitadas':
    st.write('Número de Pizzas Solicitadas por Cada Pessoa.')
    contagem = data_final.groupby('order_id')['quantity'].sum()
    pessoas_quantidade = contagem.value_counts().sort_index()
    dic = {'Quantidades de Pizzas':pessoas_quantidade.index,'Contagem de Pedidos':pessoas_quantidade.values}
    df = pd.DataFrame(dic)
    plt.scatter(df['Quantidades de Pizzas'], df['Contagem de Pedidos'], marker='o', color='b', label='Dados')
    for i, row in df.iterrows():
        x = row['Quantidades de Pizzas']
        y = row['Contagem de Pedidos']
        plt.text(x, y, f'({x}, {y})', fontsize=10, ha='left', va='bottom',rotation=60)
    plt.xlabel('Quantidade de Pizzas Por Pedido')
    plt.ylabel('Quantidade de Pedidos')
    st.pyplot(plt)
st.caption('Os dados foram obtidos a partir do site: https://github.com/khorneflakes-dev/maven-pizza-challenge/tree/main/pizza_sales')