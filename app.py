#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form 
from forms import *
from flask_migrate import Migrate
from datetime import datetime
import sys
import re
from operator import itemgetter
from sqlalchemy import distinct
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#connect to local postgres :
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://azzouzhamza:@localhost:5432/test_2'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# connect to a local postgresql database (done above)

#azzouz_hamza (hdado)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
  
    #implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(250))
    seeking_description = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    genres = db.Column(db.String(), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True) #declare shows on PARENT table 
    
    def __repr__(self):
      return  f'<Venue : {self.id}, name :{self.name}, city : {self.state}, address : {self.address} >'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))  #could be a separate table to construct a relationship (later testing)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120)) 
    #  implement any missing fields, as a database migration using Flask-Migrate
    seeking_description= db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), default=False)
    website_link = db.Column(db.String(120))
    show = db.relationship("Show", backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist : {self.id} {self.name}>'

class Show(db.Model):
  _tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False) #adding foreign key on child table (show)
  venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False) #foreign key linked to Venue table

  def __repr__(self):
        return f'<Show : {self.id} start time : {self.start_time}>'
# Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
# i have had error : TypeError: Parser must be a string or character stream, not datetime
def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
    if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
      format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Done: replace with real venues data.
  #   num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    #i had to find a way and simplify my code as dummy data: because i was 
    # city
    # state
    # venues{} 
     #=============================== ! my mistake,my first submited code : 
  
  venues = Venue.query.all()

  data = []   # declare an empty list for later append (final data input)
  cities_states = set()

  for venue in venues:
    #print("venue ======", venue) #just to visualise the output
    cities_states.add((venue.city, venue.state)) 
    
     # Add data from venue model to the tuple | set()deduplicate will filter the data based on city/state
    #print(cities_states)
   
    #print("=======")
    #print(type(cities_states_list)) #goog result
    cities_states_list = list(cities_states)
    #print(type(cities_states_list))
    cities_states_list.sort(key=itemgetter(1,0))     # Sorts on second column first (state), then by city usinf sort() with itemgetter key
    # itemgetter() can be used to sort the list based on the value of the given key.
    now = datetime.now()    
  
  for c_s in cities_states_list: # boucle for pour passer sur toutes les localisations
        # For this location, see if there are any venues there, and add if so
          venues_list = []
          for venue in venues: 
            if (venue.city == c_s[0]) and (venue.state == c_s[1]):
                print(c_s[0] , " ", c_s[1])
                venue_shows = Show.query.filter_by(venue_id=venue.id).all()
                num_upcoming = 0
                for show in venue_shows:
                    if show.start_time > now:
                        num_upcoming += 1
                # fill the data into venues
                venues_list.append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": num_upcoming
                })
         # adding the data to cITY STATE VENUE so the structure is like the dummy data presented
          data.append({
            "city": c_s[0],
            "state": c_s[1],
            "venues": venues_list #tree - nested list
        })
      
  return render_template("pages/venues.html", areas=data)
    
    
    # declare an empty list for later append (final data input)
 
    # Add data from venue model to the tuple | tuple will filter the data based on city/state
   

    # print("***********")
    # print(cities_states_list)

    #sort a list of tuple
    #cities_states_list.sort(key=itemgetter(1,0)) 
    #sort a list of tuples by second  element "state" in List of tuple
    # print("=============")
    # print(cities_states_list.sort(key=lambda i: i[1])) # Sorts on second column first (state), then by city usinf sort() with itemgetter key
    # itemgetter() can be used to sort the list based on the value of the given key.
    
              
    # adding the data to cITY STATE VENUE so the structure is like the dummy data presented
  

 
   
    # return render_template('pages/venues.html', areas=data)
   
         
         
        
         

#==============================
 
  #return render_template('pages/venues.html', areas=data);  #rendering the view
#=======--------------- dummy data
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  # return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
   # pages/search_venue : search_term 
  search_term = request.form.get('search_term', '') #input from the utilisateur  (jinja)

  #what sould we do after getting the data from the front - is to query the model database to extract  the same keyword  (Venue.name) 
  # search term =should be like = venue.name  | session.query(TableName).filter(TableName.colName.ilike(f'%{search_text}%')).all()
  #use sql alchemy ilike to match the search term from the user in our venue db.model
  search_match = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []

  for match in search_match:
    data.append({ #fill the data list with id,name, num_upcoming_shows as in response
      "id": match.id,
      "name": match.name,
      "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id == match.id).filter(Show.start_time > datetime.now()).all()), #using two filter
      #lenght represent the number of upcoming event after query the show table that match the venue and filter by future date only
    })
  response = {
    "count" : len(search_match) ,# lenght of a list | could use a count also: search_match.count()
    "data" : data
  }
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # Done : replace with real venue data from the venues table, using venue_id
  #we should display every Venue data as structured in dummy data in every route by id, first let's connect the controller to the view :

  venue = Venue.query.get(venue_id) #query the venue model
  #we would query also the show table that has relationship with both artist and venue, to accomplish the objectif of filling data same as demo data:

  join_query = db.session.query(Show).join(Artist) #Join query the show with artist, artist is a foreign key, so we could display artist data as well by calling their col name in the show query !!
  
  query_upcoming_shows = join_query.filter(Show.venue_id==venue_id).filter(Show.start_time> datetime.now()).all() 
  print("==============")
  print(len(query_upcoming_shows))
  upcoming_shows = [] 
  # updating code :
  query_past_shows = join_query.filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all() 
  past_shows = [] 
  #Now i should fill the past shows and upcoming shows as presented in demo data: then i make the main structure data that contains the 
  #upcoming shows and past shows, 
  for show in query_past_shows:
    past_shows.append({
      "artist_id" : show.artist_id, # artist id is foreign key in show table, we query from it directly
      "artist_name": show.artist.name, # call the artist {backref} name from show ,make use of the relationship on artist model
      "artist_image_link" : show.artist.image_link,
      "start_time" : show.start_time.strftime("%Y-%m-%d %H:%M:%S") # display the time like "2019-05-21T21:30:00.000Z" , date time to string
    })
  # let's print the main data on screen for this route, we are in Venue route, so let's query from Venue model :
  data = {
    "id" : venue.id, #venue is declared above that query from model
    "name" : venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(query_past_shows),
    "upcoming_shows_count": len(query_upcoming_shows),

  }
  return render_template('pages/show_venue.html', venue=data)

  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  # return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # done: insert form data as a new Venue record in the db, instead
  # done: modify data to be the data object returned from db insertion

  form = VenueForm(request.form)

  if form.validate() :
        try:
          
          new_venue = Venue(
            name = form.name.data,
            city = form.city.data,
            state = form.state.data ,
            address = form.address.data ,
              #using regular expression to clean phone data. 
            phone = re.sub('\D', '', form.phone.data), 
            genres = form.genres.data  ,                
            seeking_talent = True if form.seeking_talent.data == 'Yes' else False ,
            image_link = form.image_link.data,
            website_link = form.website_link.data,
            facebook_link = form.facebook_link.data,
            seeking_description = form.seeking_description.data
          )  
    
          db.session.add(new_venue)
          db.session.commit()
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
        except Exception:
          db.session.rollback()
          print("=======================") #i had some issue, this print helped me to view errror in my termminal logs
          print(sys.exc_info())
          print("=======================")
        
          flash('An error occurred. Venue' + ' could not be listed.' )

        finally:
          db.session.close()
  else:
        print("\n\n", form.errors)
        flash('An error occurred. Venue' + ' could not be listed.')

  return redirect(url_for("index"))       

  #return render_template('pages/home.html')

#@app.route('/venues/<venue_id>', methods=['DELETE'])
#def delete_venue():
  # Testing -didn't complete front-: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists') #done 
def artists(): #Get request from model database/ 
  data = db.session.query(Artist).all()
  return render_template('pages/artists.html', artists=data)
  # # DONE: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  # return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists(): #done
  # Done : implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  search_result = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in search_result:
    data.append({
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(db.session.query(Show).filter(Show.artist_id == result.id).filter(Show.start_time > datetime.now()).all()),
    })
  response={
    "count": len(search_result),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id): #done
  # shows the artist page with the given artist_id
  # Done: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()

  for show in shows:
    data = {
      'venue_id': show.venue.id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': format_datetime(str(show.start_time))
    }
    if show.start_time > current_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)
  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genres,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website_link' : artist.website_link,
    'facebook_link': artist.facebook_link,
    'image_link': artist.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows)
  }  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    
    artist = Artist.query.get(artist_id)

    if artist: 
      form.name.data = artist.name
      form.city.data = artist.city
      form.state.data = artist.state
      form.phone.data = artist.phone
      form.genres.data = artist.genres
      form.facebook_link.data = artist.facebook_link
      form.image_link.data = artist.image_link
      form.website_link.data = artist.website_link
      form.seeking_venue.data = artist.seeking_venue
      form.seeking_description.data = artist.seeking_description
     

    return render_template('forms/edit_artist.html', form=form, artist=artist)

  # form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # !!!done : populate form with fields from artist with ID <artist_id>
    #return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    
  
    artist.name = request.form.get("name")
    artist.phone = request.form.get("phone")
    artist.state = request.form.get("state")
    artist.city = request.form.get("city")
    artist.genres = request.form.getlist("genres")
    artist.image_link = request.form.get("image_link")
    artist.website_link = request.form.get("website_link")
    artist.facebook_link = request.form.get("facebook_link")
    artist.seeking_venue = request.form.get("seeking_venue") #

    
    db.session.commit()
    
    flash('The Artist ' + request.form.get("name") + ' has been successfully updated!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An Error has occured and the update unsucessful')
  finally:
    db.session.close()
  #return render_template("pages/show_artist.html" , artist=artist_id )
  return redirect(url_for('show_artist', artist_id=artist_id))

  #return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  form = VenueForm()
  venue = Venue.query.get(venue_id) #getting the data that match venue_id opened in link <route> 
  # populating form by default when opening route url in browser :
  if venue: 
    form.name.data = venue.name  #name in form (user input) == name in db model ! 
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # done: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # done: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  try: 
    venue.name = request.form.get("name")
    venue.city = request.form.get("city")
    venue.state = request.form.get("state")
    venue.phone = request.form.get("phone")
    venue.genres = request.form.getlist("genres"),
    venue.facebook_link = request.form.get("facebook_link")
    venue.image_link = request.form.get("image_link")
    venue.website_link = request.form.get("website_link")
    venue.seeking_venue = True if "seeking_venue" in request.form else False
    venue.seeking_description = request.form.get("seeking_description")
    #Controller to model communication :
   
    #no need to match venue, already query the database ; venue = Venue(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_talent=seeking_venue, seeking_description=seeking_description)
    #db.session.add(venue) #we don't add in edit ! just commit; pour ecraser les donnees 
    db.session.commit()
    flash('Venue' + request.form.get("name") + '  was successfully listed!')
  
  except Exception(): 
    
    db.session.rollback()
    print("===================")
    print(sys.exc_info())
    flash('An error occurred.  The Venue ' + request.form.get("name")+ ' could not be listed.')
  finally: 
    db.session.close()

  #return render_template('pages/home.html')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # : insert form data as a new Venue record in the db, instead
  # : modify data to be the data object returned from db insertion
    form = ArtistForm()  #declaring form from forms.py !!
  # 1 :
    
    try:  # assign  input data form from the view to a python object artist,  
      artist = Artist(
        name = request.form.get('name') ,
        city = request.form.get('city'),
        state = request.form.get('state'),
        phone = request.form.get('phone'),
        image_link = request.form.get('image_link'),
        genres = request.form.getlist('genres'),
        website_link = request.form.get('website_link'),
        facebook_link = request.form.get('facebook_link'),
        # seeking_venue = request.form['seeking_venue'], #bool : let's try :
        seeking_venue = True if form.seeking_venue.data == 'Yes' else False,
        seeking_description = request.form.get('seeking_description')
      )
      #posting to the database
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception:
      db.session.rollback()
      #print("=================")
      #print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form.get("name") + ' could not be listed.')
    finally:
      # closing session 
      db.session.close()
    # whatever the result of the operation; return home page ;
    return render_template('pages/home.html')  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # done: replace with real venues data.
  shows = Show.query.order_by('start_time').all()
  #print("========") 
  #print(shows) #view repr on logs 

  data=[]
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time})
  shows = Show.query.all()
  data = [] #declare empty data list, append data once ready 
  for show in shows:
      show = {
          "venue_id": show.venue_id,
          "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
          "artist_id": show.artist_id,
          "artist_name": db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0],
          "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
          "start_time": show.start_time
      }
      print("=============")
      print(show['start_time'])	  
      data.append(show)
  	  
  return render_template('pages/shows.html', shows=data)


  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  # return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission(): 
  # called to create new shows in the db, upon submitting new show listing form
  # Done: insert form data as a new Show record in the db, instead
    # declaring errors as global
    error_artist = False
    error_venue = False
    try:
      # request artist data from forms. 
        artist_id = request.form.get("artist_id")
        venue_id = request.form.get("venue_id")
        start_time = request.form.get("start_time")

        #  Testing artist_id availlability in database model :
        query_artist = Artist.query.get(artist_id)
        if query_artist is None:
            error_artist = True


        #  
        query_venue = Venue.query.get(venue_id)
        if query_venue is None:
           error_venue = True
          

        #  If the above tests pass, add the record to the DB as usual. Else, set the errors above.
        if query_venue is not None and query_artist is not None:
            new_show = Show(
                artist_id=query_artist.id,
                venue_id=query_venue.id,
                start_time=start_time,
            )
            db.session.add(new_show) #adding to show table
            db.session.commit()
            flash("show by"
                + query_artist.name + " has been successfully scheduled at the following venue: "
                + query_venue.name
            )

        
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash("Something went wrong and the show was not created. Please try again.")
        

    finally:
        db.session.close()
    if error_artist == True:
      flash("Artist id not found")
    elif error_venue==True:
      flash("Venue not found")      

    
    
    
    return render_template("pages/home.html")
    flash("Show was successfully listed!")

    
  
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
