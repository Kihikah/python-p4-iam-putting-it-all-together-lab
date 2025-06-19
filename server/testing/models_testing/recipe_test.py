import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe
from models import db, Recipe, User

class TestRecipe:
    '''User in models.py'''

    def test_has_attributes(self):
        with app.app_context():
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(username="chef123")
            user.password_hash = "secret123"
            db.session.add(user)
            db.session.commit()

            recipe = Recipe(
            title="Delicious Shed Ham",
            instructions="This is a test instruction with more than fifty characters.",
            minutes_to_complete=60,
            user_id=user.id
            )

            
            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter_by(title="Delicious Shed Ham").first()
            assert new_recipe.title == "Delicious Shed Ham"
            assert new_recipe.minutes_to_complete == 60


    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            recipe = Recipe()
            
            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            '''must raise either a sqlalchemy.exc.IntegrityError with constraints or a custom validation ValueError'''
            with pytest.raises( (IntegrityError, ValueError) ):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="idk lol")
                db.session.add(recipe)
                db.session.commit()

