import modules.bd.db as DB

def check_login(login, password):
    bd = DB.BD().login_infos()
    for elem in bd:
        if elem.user == login and elem.password == password: return True
    return False
def register(login, password):
    bd = DB.BD().create_user(login, password)
    return check_login(login, password)

def portf_add(act, weights, USER):
    bd = DB.BD().portf_add(act, weights, USER)
def portf_get(USER):
    bd = DB.BD().portf_add()
    arr = []
    for elem in bd:
        if elem.user == USER: arr.append(elem)
    return arr

def act_get(ticker):
    bd = DB.BD().all_act_get()
    for elem in bd:
        if elem.ticker == ticker: return elem
    return False
def act_upd(ticker, cost):
    bd = DB.BD().all_act_get()
    for elem in bd:
        if elem.ticker == ticker: DB.BD().act_upd(cost, ticker)
        else: bd = DB.BD().act_add(cost, ticker)