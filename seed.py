'''Seed file to make sample data for users db'''

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add users
jane = User(first_name='Jane', last_name='Doe', image_url='https://i.pinimg.com/originals/5c/09/c4/5c09c4dc82dc441dfb26975fe8dc1634.jpg')
john = User(first_name='John', last_name='Doe', image_url='https://images.squarespace-cdn.com/content/v1/587a9b3fbf629abac08b3ce9/1564863231701-WUQL63XUZB9GIXADMY1B/Portraits_byAndreaDomjanPhotography_013.jpg?format=1500w')
charlie = User(first_name='Charlie', last_name='Dough', image_url='https://cms-assets.tutsplus.com/cdn-cgi/image/width=850/uploads/users/80/posts/26761/image/22-MalePortraits.jpg')

# Add new objects to session, so they'll persist
db.session.add(jane)
db.session.add(john)
db.session.add(charlie)

# Commit to db
db.session.commit()
