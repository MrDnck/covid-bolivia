import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cargar datos
file_path = 'bolivia_covid19_cases_daily.csv'
df = pd.read_csv(file_path)



st.markdown("""
### Código Fuente
Puedes ver y modificar el código en el siguiente repositorio de GitHub: [Repositorio de GitHub](https://github.com/MrDnck/covid-bolivia)

### Autor
Cristian Catari
            
Celular: +591 70562921  
Correo electrónico: cristian.catari.ma@gmail.com
""")

# Configuración de Streamlit
st.title('COVID-19 en Bolivia')


# Transformar la columna 'date' a datetime
df['date'] = pd.to_datetime(df['date'])

# Agregar el año
df['year'] = df['date'].dt.year

# Ejemplo de coordenadas para cada región (puedes ajustarlas según tus datos reales)
region_coords = {
    'Santa Cruz': (-17.7833, -63.1822),
    'La Paz': (-16.5000, -68.1500),
    'Cochabamba': (-17.3833, -66.1500),
    'Beni': (-14.8333, -64.9000),
    'Tarija': (-21.5333, -64.7333),
    'Oruro': (-17.9667, -67.1167),
    'Chuquisaca': (-19.0333, -65.2627),
    'Pando': (-11.0333, -68.7667),
    'Potosí': (-19.5833, -65.7500)
}

# Crear un DataFrame con las coordenadas
coords_df = pd.DataFrame(region_coords).T.reset_index()
coords_df.columns = ['region', 'lat', 'lon']

# Combinar con el DataFrame original
df = df.merge(coords_df, on='region', how='left')

# Gráfico de mapa interactivo con Mapbox
fig_map = px.scatter_mapbox(df, lat='lat', lon='lon', color='region', size='cases',
                            hover_name='region', hover_data=['cases'],
                            title='Casos Confirmados de COVID-19 por Región',
                            mapbox_style='carto-positron', zoom=4, height=500,
                            size_max=70)  # Ajustar el tamaño máximo de los puntos
st.plotly_chart(fig_map)

# Gráfico de casos confirmados por fecha
total_confirmed = df[['date', 'cases']].groupby('date').sum().reset_index()
fig1 = go.Figure(data=go.Scatter(x=total_confirmed['date'],
                                 y=total_confirmed['cases'],
                                 mode='lines+markers'))
fig1.update_layout(title='Casos Confirmados de COVID-19 por Año en Bolivia', 
                   xaxis_title="Fecha",
                   yaxis_title="Numero de casos")
st.plotly_chart(fig1)

# Gráfico de casos confirmados por región
fig2 = px.line(df, x='date', y='cases', color='region', title='Casos Confirmados de COVID-19 por Región')
st.plotly_chart(fig2)

# Gráfico de barras de casos confirmados por región en un año específico (ej. 2020)
cases_2020 = df[df['year'] == 2020].groupby('region')['cases'].sum().reset_index()
fig3 = px.bar(cases_2020, x='region', y='cases', title='Casos Confirmados de COVID-19 por Región en 2020')
st.plotly_chart(fig3)

# Gráfico de pastel de casos confirmados por departamento
Data_per_department = df.groupby('region')['cases'].sum().reset_index()
fig7 = px.pie(Data_per_department, values='cases', names='region',
              title='Casos Confirmados de COVID-19 en Bolivia', hole=0.2)
fig7.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig7)

# Gráfico de Treemap de casos confirmados por departamento
fig8 = px.treemap(Data_per_department, path=['region'], values='cases', 
                  title='Casos Confirmados de COVID-19 en Bolivia', 
                  color_discrete_sequence=px.colors.qualitative.Dark2, height=700)
fig8.data[0].textinfo = 'label+text+value'
st.plotly_chart(fig8)

# Gráfico de casos activos por región a lo largo del tiempo
fig4 = px.line(df, x='date', y='active', color='region', title='Casos Activos de COVID-19 por Región')
st.plotly_chart(fig4)

# Gráfico de casos recuperados por región a lo largo del tiempo
fig5 = px.line(df, x='date', y='recovered', color='region', title='Casos Recuperados de COVID-19 por Región')
st.plotly_chart(fig5)

# Gráfico de casos fallecidos por región a lo largo del tiempo
fig6 = px.line(df, x='date', y='deceased', color='region', title='Casos Fallecidos de COVID-19 por Región')
st.plotly_chart(fig6)
