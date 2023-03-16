import streamlit as st
import pandas as pd
import numpy as np
import modules.db_middelware as DB
import modules.calc_portf as CP

state_auth = False
authed = False
login = ""

with open("modules/state","r",encoding="utf-8-sig") as f:
    if f.read() == "1":
        authed = True
        with open ("modules/login","r", encoding="utf-8-sig") as f2:
            login = f2.read()
def toggle_on():
    with open("modules/state", "w", encoding="utf-8-sig") as f: f.write("1")


df = pd.DataFrame(
            np.random.randn(3, 3),
            columns=['a', 'b', 'c'])
if not authed:
    tab1, tab2 = st.tabs(["Регистрация", "Авторизация"])

    with tab1:
        login = st.text_input('Введите логин:', key="logreg")
        password1 = st.text_input('Введите пароль:', key="passreg")
        password2 = st.text_input('Повторите пароль:')
        if st.button('Отправить', key="sendreg") :
            if password1 != password2:
                st.error('Пароли не совпадают', icon=None)
                state_auth=False

            if login == '':
                st.error('Введите логин', icon=None)
                state_auth=False

            if password1 == '' or password2 == '':
                st.error('Введите пароль/Повторите пароль', icon=None)
                state_auth = False

            if login!="" and password1 != "" and password2 != "" and password2==password1: state_auth = True


        if state_auth: #auth checker
            if DB.register(login,password1):
                authed = True
                toggle_on()
                with open ("modules/login","w", encoding="utf-8-sig") as f2:

                    f2.write(login)
                st.success("Пользователь успешно зарегестрирован!", icon=None)
                st.experimental_rerun()
            else: st.error("Ошибка регистрации", icon=None)

    with tab2:
        login = st.text_input('Введите логин:', key="logauth")
        pw = st.text_input('Введите пароль:', key="passauth")
        if st.button('Отправить', key="sendauth") :
            if login == '':
                st.error('Введите логин', icon=None)
                state_auth = False

            if pw == '':
                st.error('Введите пароль/Повторите пароль', icon=None)
                state_auth = False

            if login != '' and pw != '': state_auth = True

        if state_auth: #auth checker
            if DB.check_login(login, pw):
                authed = True
                toggle_on()
                with open ("modules/login","w", encoding="utf-8-sig") as f2:

                    f2.write(login)
                st.success("Вы вошли в систему!", icon=None)
                st.experimental_rerun()
            else: st.error("Ошибка входа", icon=None)


if authed:
    akc = st.text_input('Введите акции через пробел:').split()
    var = st.radio('Выберите ориентир для поиска:', ('Риск', 'Доходность'))
    if var=='Риск':
        risk = st.slider('Выберите желаемый процент риска:', 0.00, 100.00, 0.01)
    if var == 'Доходность':
        dohod = st.slider('Выберите желаемый процент дохода:', 0.00, 100.00, 0.01)
    opt = st.multiselect('Выберите необходимые параметры для просмотра:',
                         ['Облако портфелей', 'Текущий курс', 'Средний портфель' ,'Портфель с максимальным коэффициентом Шарпа', 'Портфель с минимальным риском', 'Портфель с максимальным риском'])
    start = st.button('Поиск')
    if start:

        if var == "Риск": data = CP.get_data(outers=opt, target_risk=risk/100, tickers = akc)
        if var == "Доходность": data = CP.get_data(outers=opt, target_doh=dohod/100, tickers = akc)

        if 'Целевой риск' in list(data.keys()):
            st.header('Целевой портфель')
            _ = data["Целевой риск"]
            st.subheader(f"Риск: {_['риск']}")
            st.subheader(f"Доходность: {_['доходность']}")
            st.subheader('Доли')
            st.dataframe(_['доли'].style.highlight_max(axis=0))

            DB.portf_add(act=list(_['доли'].index), weights = _['доли']["доли, %"].values, USER=login, risk = _['риск'], doh=_['доходность'])


        if 'Целевой доход' in list(data.keys()):
            st.header('Целевой портфель')
            _ = data["Целевой доход"]
            st.subheader(f"Риск: {_['риск']}")
            st.subheader(f"Доходность: {_['доходность']}")
            st.subheader('Доли')
            st.dataframe(_['доли'].style.highlight_max(axis=0))

            DB.portf_add(act=list(_['доли'].index), weights = _['доли']["доли, %"].values, USER=login, risk = _['риск'], doh=_['доходность'])

        if 'Облако портфелей' in opt:
            st.title('Облако портфелей:')
            st.image(data['Облако портфелей'])

        if 'Плавающее среднее' in opt: #deactivated
            for elem in list(data["Плавающее среднее"].keys()):
                st.subheader(f'Плавающее среднее для {elem}')
                st.line_chart(data["Плавающее среднее"][elem])

        if 'Средний портфель' in opt:
            st.title('Средний портфель')
            _ = data["Средний портфель"]
            st.subheader(f"Риск: {_['риск']}")
            st.subheader(f"Доходность: {_['доходность']}")
            st.subheader('Доли')
            st.dataframe(_['доли'].style.highlight_max(axis=0))

        if 'Портфель с максимальным коэффициентом Шарпа' in opt:
            st.title('Портфель с максимальным коэффициентом Шарпа')
            _ = data["Портфель с максимальным коэффициентом Шарпа"]
            st.subheader(f"Риск: {_['риск']}")
            st.subheader(f"Доходность: {_['доходность']}")
            st.subheader('Доли')
            st.dataframe(_['доли'].style.highlight_max(axis=0))

        if 'Портфель с минимальным риском' in opt:
            st.title('Портфель с минимальным риском')
            _ = data["Портфель с минимальным риском"]
            st.subheader(f"Риск: {_['риск']}")
            st.subheader(f"Доходность: {_['доходность']}")
            st.subheader('Доли')
            st.dataframe(_['доли'].style.highlight_max(axis=0))

        if 'Портфель с максимальным риском' in opt:
            st.title('Портфель с максимальным риском')
            _ = data["Портфель с максимальным риском"]
            st.subheader(f"Риск: {_['риск']}")
            st.subheader(f"Доходность: {_['доходность']}")
            st.subheader('Доли')
            st.dataframe(_['доли'].style.highlight_max(axis=0))
                
        if 'Текущий курс' in opt:
            st.title('Текущий курс:')
            _ = data["Текущий курс"]
            l = list(_.keys())
            for i,j in zip(st.columns(len(_)),l):
                with i:
                    st.metric(label=j, value=_[j][0], delta=_[j][1])
    with st.sidebar:
        st.header('Ваши портфели:')
        
        arr = DB.portf_get(USER=login)
        names = []
        data_names_l = []
        for elem in arr:
            names.append(f"{elem.portfs} Риск: {elem.risk} Доход: {elem.doh}" )
            data_names_l = [elem.risk,elem.doh,elem.weights,elem.portfs]
        names = tuple(names)

        option = st.selectbox('Выберите параметры портфеля:', names)
        names = list(names)
        for i in range(len(names)):
            elem = names[i]
            data_names = data_names_l
            if option == elem:
                st.metric(label="Риск:", value=data_names[0])
                st.metric(label="Доход", value=data_names[1])
                weights = [i for i in list(map(float,data_names[2].split()))]
                df = pd.DataFrame({"тикеры": data_names[3].split(),"доли, %":weights}).set_index(["тикеры"])

                st.dataframe(df.style.highlight_max(axis=0))
                break
        logout = st.button('Выход')
        if logout:
            with open("modules/state", "w", encoding="utf-8-sig") as f:
                f.write("0")
                st.experimental_rerun()
