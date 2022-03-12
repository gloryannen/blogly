from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        test_user = User(first_name="TestUser", last_name="Doe", image_url= 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAMAAAAL34HQAAAAG1BMVEXMzMyWlpbFxcWxsbG3t7ecnJyjo6O+vr6qqqqUhI1cAAABC0lEQVR4nO3U7YrDIBCFYccZP+7/itfRmES6+VfDLrwPlEo54HGSGgIAAAAAAAAAAAAAAAAAAAD+NWkflUZ9kZI9hc7UU+ibqu9Ys6qWEExUJT6EZuop9EXWzt++8nH63GZRfWrBN45i99BMXaFtYrFeq4zT+xAs9WWqbTpLaKZuoY3FfEfJItXXbccydjQxKUvoSN1Du2tpLEnHelRos/Gia62eWkJ7a7n2XJZBqNhnqKVenJYrsr42KeVfarXUa+9Wf6M1H3+y8ew0lWtcvdZM3UJ7a4WUrT+zfiWV8bOFmpbQTF2h3bVKlnFxnxe4V4rnuEatmXrjlgcAAAAAAAAAAAAAAAAAAH/cD4mjA82Or0YGAAAAAElFTkSuQmCC')
        db.session.add(test_user)
        db.session.commit()

        self.test_user_id = test_user.id
        self.test_user = test_user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.test_user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>TestUser Doe Details</h2>', html)
            self.assertIn(self.test_user.first_name, html)


    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "Doug", "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQoAAAC+CAMAAAD6ObEsAAAAP1BMVEXu7u7t7e3x8fGmpqaoqKiqqqq9vb3n5+ejo6Pq6urh4eG6urqurq7k5OS2trbIyMjV1dXX19fCwsLPz8/W1tbWfPimAAACbElEQVR4nO3XW28bIRCGYRhgOS7ssv7/v7WDk8ptWrW9iBrZep+LxNp8OTCZAWwMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgC9j7a+PfpP6l9BzK7O1WcSYODc1d320tX7lHzJSRm/bba19Zbaa9dHH0NOL3bXmetQCeO9cakX25pp3Q34KhebCISYmDbkU76Hgxwt1hlyp76X7S8zh+qGyTFfjEVp8hIbrJU7fRE7Xr+O4sgxf99OF+Ief/WzKVSRvfoiud9gsYqS5m+zdH3mMw5pzjHzVS6vgg12hvEK5avVsd4f8/Vc8DdGNoLXdSPW11pElhnCKLnXI0HEpLQ3NaFBbQzTUtzp0PrqOi60/jdHz0+Xp2o14r/uAn2YP4b1R9L9eN9fv+4GU4C7JXSPJVylNv8dubr5WKcZs/jR26jlytnA8SmH25n3f76kz+GlNHFvRMrjba5ZC2//y63jUVa2Wj49SmOH9uGfO5rd4zxqTNzd0QG6rFK80IHuJRs7Qi4m7ToKWwgR/SlzbotGP965YjbDlteqsoTzdzPe9ouvMfPUCPo3UNLMdvsdT90ijfX+IlsPqi2LMdL37qveKpgGlY9JOU9bBsem87N6Vr17A59Ej0m8zvJ2Mfeg+mdepOfWFyM2F81y75fChLTbXe6hbbaSmoe2FrljGXi2lsG6NpbqUqo6DHSHpxUvWOWrtTOHoSb+Ukst6iOqnunrhWqEXaorFlvL+ViKW98tjLmvfsG/v0+zDx9D//2MBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfPcNls4W+BQokKsAAAAASUVORK5CYII="}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>TestUser2 Doug Details</h2>", html)



    def test_delete_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "Doug", "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQoAAAC+CAMAAAD6ObEsAAAAP1BMVEXu7u7t7e3x8fGmpqaoqKiqqqq9vb3n5+ejo6Pq6urh4eG6urqurq7k5OS2trbIyMjV1dXX19fCwsLPz8/W1tbWfPimAAACbElEQVR4nO3XW28bIRCGYRhgOS7ssv7/v7WDk8ptWrW9iBrZep+LxNp8OTCZAWwMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgC9j7a+PfpP6l9BzK7O1WcSYODc1d320tX7lHzJSRm/bba19Zbaa9dHH0NOL3bXmetQCeO9cakX25pp3Q34KhebCISYmDbkU76Hgxwt1hlyp76X7S8zh+qGyTFfjEVp8hIbrJU7fRE7Xr+O4sgxf99OF+Ief/WzKVSRvfoiud9gsYqS5m+zdH3mMw5pzjHzVS6vgg12hvEK5avVsd4f8/Vc8DdGNoLXdSPW11pElhnCKLnXI0HEpLQ3NaFBbQzTUtzp0PrqOi60/jdHz0+Xp2o14r/uAn2YP4b1R9L9eN9fv+4GU4C7JXSPJVylNv8dubr5WKcZs/jR26jlytnA8SmH25n3f76kz+GlNHFvRMrjba5ZC2//y63jUVa2Wj49SmOH9uGfO5rd4zxqTNzd0QG6rFK80IHuJRs7Qi4m7ToKWwgR/SlzbotGP965YjbDlteqsoTzdzPe9ouvMfPUCPo3UNLMdvsdT90ijfX+IlsPqi2LMdL37qveKpgGlY9JOU9bBsem87N6Vr17A59Ej0m8zvJ2Mfeg+mdepOfWFyM2F81y75fChLTbXe6hbbaSmoe2FrljGXi2lsG6NpbqUqo6DHSHpxUvWOWrtTOHoSb+Ukst6iOqnunrhWqEXaorFlvL+ViKW98tjLmvfsG/v0+zDx9D//2MBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfPcNls4W+BQokKsAAAAASUVORK5CYII="}
            resp = client.post(f"/users/{self.test_user_id}/delete", data=d, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

