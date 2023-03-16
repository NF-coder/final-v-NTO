import streamlit as st
import pandas as pd
import numpy as np
import modules.db_middelware as DB
import modules.calc_portf as CP

state_auth = False
authed = False

with open("modules/state","r",encoding="utf-8-sig") as f:
    if f.read() == "1": authed = True
def toggle_on():
    with open("modules/state", "w", encoding="utf-8-sig") as f: f.write("1")


df = pd.DataFrame(
            np.random.randn(3, 3),
            columns=['a', 'b', 'c'])
tab1, tab2 = st.tabs(["Регистрация", "Авторизация"])

with tab1:
    name = st.text_input('Введите логин:', key="logreg")
    password1 = st.text_input('Введите пароль:', key="passreg")
    password2 = st.text_input('Повторите пароль:')
    if st.button('Отправить', key="sendreg") :
        if password1 != password2:
            st.subheader('Пароли не совпадают')
            state_auth=False

        if name == '':
            st.subheader('Введите логин')
            state_auth=False

        if password1 == '' or password2 == '':
            st.subheader('Введите пароль/Повторите пароль')
            state_auth = False

        if name!="" and password1 != "" and password2 != "": state_auth = True


    if state_auth: #auth checker
        if DB.register(name,password1):
            authed = True
            toggle_on()
            st.caption("Пользователь успешно зарегестрирован!")
        else: st.caption("Ошибка регистрации")

with tab2:
    login = st.text_input('Введите логин:', key="logauth")
    pw = st.text_input('Введите пароль:', key="passauth")
    if st.button('Отправить', key="sendauth") :
        if login == '':
            st.subheader('Введите логин')
            state_auth = False

        if pw == '':
            st.subheader('Введите пароль/Повторите пароль')
            state_auth = False

        if login != '' and pw != '': state_auth = True

    if state_auth: #auth checker
        if DB.check_login(login, pw):
            authed = True
            toggle_on()
            st.caption("Вы вошли в систему!")
        else: st.caption("Ошибка входа")


if authed:
    CP.get_data()
    akc = st.text_input('Введите акции через пробел:').split()
    var = st.radio('Выберите ориентир для поиска:', ('Риск', 'Доходность'))
    if var=='Риск':
        risk = st.slider('Выберите желаемый процент риска:', 0.00, 100.00, 0.01)
    if var == 'Доходность':
        dohod = st.slider('Выберите желаемый процент дохода:', 0.00, 100.00, 0.01)
    opt = st.multiselect('Выберите необходимые параметры для просмотра:',
                         ['Облако портфелей', 'Плавающее среднее', 'Текущий курс'])
    start = st.button('Поиск')
    if start:
        if 'Облако портфелей' in opt:
            st.header('Облако портфелей:')
            st.image("https://cdnn21.img.ria.ru/images/07e5/06/18/1738448523_0:89:864:575_1920x0_80_0_0_7541a4a6d36edb667d2de032b8aefc66.jpg")
        if 'Плавающее среднее' in opt:
            st.header('Плавающее среднее:')
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['a', 'b', 'c'])

            st.line_chart(chart_data)
        if 'Текущий курс' in opt:
            st.header('Текущий курс:')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Доллар", value="75.81", delta="-0.13")
            with col2:
                st.metric(label="Евро:", value="72.23", delta="-0.21")
            with col3:
                st.metric(label="Рубль", value="124.12", delta="55.23")
    with st.sidebar:
        st.header('Ваши портфели:')
        option = st.selectbox('Выберите параметры портфеля:', ('Выберите портфель','Риск: 11.23%  Доход: 23.12%', 'Риск: 15.75% Доход: 43.54%'))
        if option == 'Риск: 11.23%  Доход: 23.12%':
            st.metric(label="Риск:", value="11.23%")
            st.metric(label="Доход", value="23.12%")
            st.dataframe(df.style.highlight_max(axis=0))
        if option == 'Риск: 15.75% Доход: 43.54%':
            st.metric(label="Риск:", value="15.75%")
            st.metric(label="Доход", value="43.54%")
            st.dataframe(df.style.highlight_max(axis=0))