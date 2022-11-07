from backend import test, movies, user


class TestMovies(test.TestCase):

    def test_create(self):
        obj = movies.Movie_list.create(Title='test', imdbID='23435', Year='2022', Type='Fantasy', Poster='xxyy')
        self.assertEqual(obj, movies.Movie_list.get(obj.Title))


    def test_delete(self):
        obj = user.User.create(email="test@gmail.com", password="test")
        self.assertRaises(user.CredentialsInvalid, lambda: user.User.login("test@gmail.com", "wrong_password"))
        self.assertEqual(obj, user.User.login("test@gmail.com", "test"))
        self.assertEqual(obj, user.User.login("test@gmail.com", u"test"))
        obj = movies.Movie_list.create(Title='test', imdbID='23435', Year='2022', Type='Fantasy', Poster='xxyy')
        self.assertEqual(obj, movies.Movie_list.delete_movie('23435'))
        

    def test_movie_get(self):
        movies.Movie_list.create(Title='test', imdbID='23435', Year='2022', Type='Fantasy', Poster='xxyy')
        self.assertEqual(1, len(movies.Movie_list.get("test")))

    def test_all_movies(self):
        movies.Movie_list.create(Title='test', imdbID='23435', Year='2022', Type='Fantasy', Poster='xxyy')
        self.assertEqual(1, len(movies.Movie_list.get("test")))

class TestMoviesApi(test.TestCase):
    def test_login(self):
        resp = self.api_client.post("user.create", dict(email="test@gmail.com", password="test"))
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post("user.me", headers=dict(authorization=access_token))
        self.assertEqual(resp.get("email"), "test@gmail.com")

    def test_movie_create(self):
        resp = self.api_client.post("movies.create", dict(Title='test', imdbID='23435', Year='2022', Type='Fantasy', Poster='xxyy'))
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
        

    def test_movie_search(self):
        resp = self.api_client.post("movies.create", dict(Title='test'))
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post("movies.get", dict(title="test"), headers=dict(authorization=access_token))
        self.assertEqual(len(resp.get("movies")), 1) 

    def test_movie_add(self):
        resp = self.api_client.post("movies.create", dict(Title='test1',imdbID='234335', Year='2021', Type='Comedy', Poster='xrxyy'))
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
    

    def test_logout(self):
        resp = self.api_client.post("user.create", dict(email="test@gmail.com", password="test"))
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post("user.me", headers=dict(authorization=access_token))
        self.assertEqual(resp.get("email"), "test@gmail.com")
        resp = self.api_client.post("user.logout", headers=dict(authorization=access_token))
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post("user.me")
        self.assertTrue(resp.get("error"))

  