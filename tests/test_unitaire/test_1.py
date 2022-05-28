import conftest


def test_index(clients):
    response = clients.get("/")
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_mail_know(clients):
    know_email = "john@simplylift.co"
    response = clients.post("/", data={'email': know_email})
    assert response.status_code == 200
    assert b'Points available:' in response.data

def test_mail_unknow(clients):
    unknown_email = "yassine@yassine.com"
    response = clients.post("/", data={'email': unknown_email})
    assert response.status_code == 200
    assert b'Adresse email non autoris' in response.data

def test_logout(clients):
    test_mail_know(clients)
    response = clients.get('/showSummary')
    assert response.status_code == 200
    response = clients.get('/logout')
    assert response.status_code == 302
    response = clients.get('/showSummary')
    assert response.status_code == 302

