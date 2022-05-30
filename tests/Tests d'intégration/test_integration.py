import conftest

club = 'Iron Temple'
placeWant = 3
competition = 'Spring Festival'
email = "admin@irontemple.com"


def test_display_summary(clients):
    response = clients.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': placeWant})
    assert response.status_code == 200
    assert "Welcome, " + email in str(response.data)
    assert b"Points available: " in response.data


def test_booking(clients):
    response = clients.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': placeWant})
    assert response.status_code == 200
    assert b"Great-booking complete"


def test_booking_exceed(clients):
    placeWant = 10
    response = clients.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': placeWant})
    assert response.status_code == 200
    assert b"booking incomplete !"

def test_booking_empty(clients):
    placeWant = 0
    response = clients.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': placeWant})
    assert response.status_code == 200
    assert b"Something went wrong-please try again"
