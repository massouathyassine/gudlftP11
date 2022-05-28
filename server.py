import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']

        for comp in listOfCompetitions:
            if datetime.datetime.fromisoformat(comp['date']) < datetime.datetime.now():
                comp['closed'] = True
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['email'] = request.form['email']
        club = [club for club in clubs if club['email'] == session['email']]
        if session['email']:
            if club:
                session['name'] = club[0]['name']
                return render_template('welcome.html', club=club[0], competitions=competitions)
            else:
                flash("Adresse email non autorisée ! Merci de contacter l'administrateur : admin@gudlift.org")
        else:
            flash("Veuillez saisir une adresse email !")
    return render_template('index.html')


@app.route('/showSummary')
def showSummary():
    if session.get('email') is not None:
        club = [club for club in clubs if club['email'] == session['email']]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if session.get('email') is not None and len(foundClub) and len(foundCompetition):
        foundClub = foundClub[0]
        foundCompetition = foundCompetition[0]
        if foundClub['name'] != session['name']:
            flash("Something went wrong-please try again")
            return redirect(url_for('showSummary'))
        if datetime.datetime.fromisoformat(foundCompetition['date']) < datetime.datetime.now():
            flash("Sorry booking is closed because Competition is terminated")
            return redirect(url_for('showSummary'))
        else:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired <= 12 and int(competition['numberOfPlaces']) > 0:
        club_capacity = int(club['points']) // 3
        if placesRequired <= club_capacity:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            if competition['numberOfPlaces'] >= 0:
                club['points'] = int(club['points']) - (placesRequired*3)
                flash('Great-booking complete ! You have reserved {} places.'.format(placesRequired))
        else:
            flash('Booking incomplete ! Not enough point in your wallet')
    else:
        if int(competition['numberOfPlaces']) > 0:
            flash('Booking incomplete ! 12 places maximum!')
        else:
            flash('Booking incomplete ! We are sorry, the competition is full !')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/points',methods=['GET'])
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
