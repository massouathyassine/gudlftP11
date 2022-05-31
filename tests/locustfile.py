from random import randint
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task(6)
    def show_summary(self):
        """ display tournament list """
        self.client.get("/showSummary")

    @task
    def book_get(self):
        """ display booking form """
        with self.client.get("/book/Spring%2520Festival/Iron Temple") as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Request took too long")
            elif response.status_code != 200:
                response.failure("Wrong Status Code")

    @task
    def purchase_post(self):
        """booking place and update point"""
        with self.client.post("/purchasePlaces", data={'club': 'Iron Temple', 'competition': 'Spring Festival', 'places': 1}) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long")

    @task
    def purchase_post_wrong_club(self):
        self.client.post("/purchasePlaces", data={'club': 'Simply Lift',
                                                  'competition': 'Spring Festival',
                                                  'places': 1})

    @task(5)
    def book_get(self):
        competition = ['Fall%20Classic', 'Spring%20Festival', 'Fall%20Classic2', 'Do%20IT%20!']
        clubs = ['She%20Lifts', 'Iron%20Temple', 'Simply%20Lift']
        selected_competition = competition[randint(0, 3)]
        selected_club = clubs[randint(0, 2)]
        self.client.get("/book/{}/{}".format(selected_competition, selected_club))

    @task(11)
    def index_post(self):
        with self.client.get("/", catch_response=True) as response:
            if "Welcome" not in response.text:
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Request took too long")

    @task(10)
    def points_get(self):
        """view clubs status points"""
        with self.client.get("/points", catch_response=True) as response:
            if "Clubs Available points" not in response.text:
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 2:
                response.failure("Request took too long")

    def on_start(self):
        """ login form / Initialize session"""
        self.client.post("/", data={"email": "admin@irontemple.com"})

    def on_quit(self):
        """ logout """
        self.client.get("/logout")
