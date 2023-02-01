import sys
sys.path.append("/Users/carolinasosa/opt/anaconda3/lib/python3.9/site-packages")

import streamlit as st

import streamlit.components.v1 as components

import numpy as np

import sklearn

import pickle

from pypdf import PdfReader

st.set_page_config(layout='wide')

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image : url("https://www.pexels.com/photo/blue-and-purple-cosmic-sky-956999/");
background-size : cover;
}
</style>
"""

st.markdown(page_bg_img,unsafe_allow_html=True)

st.title("Data World")
st.header("Herramienta para recruiters")

tab1, tab2 = st.tabs(["Insights", "Match"]) 

with tab1:
    cols = st.columns([1, 1, 1, 1, 1, 1])

    with cols[1]:
        components.html("""<iframe title="Pagina 1 - Estado mercado" width="900" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiNDhkYzYxZTgtMmZjNy00OTcyLWEyYWQtMzQ5NzlkOTA0NDk4IiwidCI6IjNhNDIzMDA3LTk3MDktNGU0NS1iNGFmLTJmOTliZDM3ZDE4ZSJ9" frameborder="0" allowFullScreen="true"></iframe>""",900,600)
    with st.expander("Ver explicación"):
        st.write(""""Sueldos y Ofertas laborales" muestra el promedio del salario anual por cada carrera: Data analyst, Data engineer y Data science. Además de elegir el año,puede filtrar por trimestre y por sub región del mundo. Se muestra en el mapa las regiones según el salario promedio a nivel global o si selecciona una sub región se mostrará solo de ese lugar. En la parte superior derecha se encuentran los salarios promedios por año por carrera y su variación porcentual con el año anterior, y debajo el cambio en el tiempo de los salarios promedios por carrera.""")

    cols = st.columns([1, 1, 1, 1, 1, 1])

    with cols[1]:
        components.html("""<iframe title="Pagina 1 - Empresas" width="900" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiMTZmYjFmZTctOWVkMy00ZWRhLWJkMTEtMmI0NDc0ZjVjZWZiIiwidCI6IjNhNDIzMDA3LTk3MDktNGU0NS1iNGFmLTJmOTliZDM3ZDE4ZSJ9" frameborder="0" allowFullScreen="true"></iframe>""",900,600)
    with st.expander("Ver explicación"):
        st.write(""""Ofertas laborales por empresa" muestra las empresas que publicaron las ofertas de trabajo extraídas de las plataformas Glassdoor,Linkedin y GetOnBoard. Del lado izquierdo puede ver la cantidad de publicaciones de ofertas de empleo de cada empresa en orden descendente y del lado derecho las ofertas de empleo de la empresa seleccionada por carrera y sub región.""")
    
    cols = st.columns([1, 1, 1, 1, 1, 1])

    with cols[1]:
        components.html("""<iframe title="Pagina 1 - Herramientas" width="900" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiOTY2NzliZjYtYTNjYS00Nzg5LWE4ODUtNjc0N2EzMzM0NTYyIiwidCI6IjNhNDIzMDA3LTk3MDktNGU0NS1iNGFmLTJmOTliZDM3ZDE4ZSJ9" frameborder="0" allowFullScreen="true"></iframe>""",900,600)
    with st.expander("Ver explicación"):
        st.write(""""Herramientas por perfil" muestra las herramientas tecnológicas más utilizadas por carrera. Sobre cada nombre de las herramientas puede ver el porcentaje que representan dentro del stack tecnológico y arriba puede ver el porcentaje de ellas que representan el 80% de la demanda por carrera.""")


def model_prediction(x_in, model):

    x = np.asarray(x_in).reshape(1,-1)
    preds=model.predict(x)

    return preds

def transformar(file):
    pdf = PdfReader(file)
    numeropaginas = len(pdf.pages)
    text = ''
    for i in range(numeropaginas):
        pagina = pdf.pages[i]
        text = text + pagina.extract_text()
    text = text.lower()
    fila = []
    for i in herramienta:
        if i.lower() in text:
            fila.append(1)
        else: fila.append(0)
    return fila 

MODEL_PATH = 'clasificacion_areas_del_data.pkl'
herramienta = ['python','excel','tableau','jupyter','matplotlib','machine learning','engineer','engineering''tensorflow',
 'jupyter notebook','apache''power bi','sql','postgresql','mongodb','airflow','big query','hive','ingeniero software','science',
 'scientists','scientific','scientist','analytics','analysis','analyst','datos','data','cloud','frameworks','numpy','pandas',
 'etl','big data','hadoop','pipeline','dashboards', 'visualization', 'storytelling','deep learning','aws','azure']  

with tab2:

    model=''

    # Se carga el modelo
    if model=='':
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)

    st.write("Ingrese el CV del postulante en formato PDF para determinar a qué perfil pertenece : Analyst, Engineer o Science.")

    upload = st.file_uploader('Elegir Archivo')
    if upload is not None:
        x = transformar(upload)
        predict = model_prediction(x,model)
        if predict[0] == 0:
            st.write('Data Engineer')
        elif predict[0] == 1:
            st.write('Data Analyst')
        else: st.write('Data Science')   

st.markdown('***')