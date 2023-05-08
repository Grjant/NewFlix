#!/usr/bin/env python3

# ---------------------------
# projects/IDB3/main.py
# Professor: Fares Fraij
# ---------------------------

# -------
# imports
# -------

from models import app, db, Theater, Movie, StreamingService
import unittest

# -----------
# DBTestCases
# -----------


class DBTestCases(unittest.TestCase):
    # ---------
    # insertion
    # ---------

    def test_movie_insert(self):  # unit test for inserting movie
        m = Movie(title='example title', id='123sad', duration='120m', genre='Horror',
                  rotten_tomatoes_rating='94%', imdb_rating='10/10', director='Bone Ale', plot='A plot', poster='postersource')
        db.session.add(m)
        db.session.commit()

        r = db.session.query(Movie).filter_by(id='123sad').one()
        self.assertEqual(str(r.id), '123sad')

        r = db.session.query(Movie).filter_by(id='123sad').first()
        db.session.delete(r)
        db.session.commit()

    def test_movie_delete(self):  # unit test for deleting movie
        m = Movie(title='example title', id='123sad', duration='120m', genre='Horror',
                  rotten_tomatoes_rating='94%', imdb_rating='10/10', director='Bone Ale', plot='A plot', poster='postersource')
        db.session.add(m)
        db.session.commit()
        r = db.session.query(Movie).filter_by(id='123sad').one()
        self.assertEqual(str(r.id), '123sad')
        r = db.session.query(Movie).filter_by(id='123sad').first()
        db.session.delete(r)
        db.session.commit()
        r = db.session.query(Movie).filter_by(id='123sad').first()
        self.assertEqual(r, None)

    def test_movie_edit(self):  # unit test for editing movie
        m = Movie(title='example title', id='123sad', duration='120m', genre='Horror',
                  rotten_tomatoes_rating='94%', imdb_rating='10/10', director='Bone Ale', plot='A plot', poster='postersource')
        db.session.add(m)
        db.session.commit()
        r = db.session.query(Movie).filter_by(id='123sad').one()
        r.genre = 'Fantasy'
        r = db.session.query(Movie).filter_by(id='123sad').one()
        self.assertEqual(r.genre, 'Fantasy')

        r = db.session.query(Movie).filter_by(id='123sad').first()
        db.session.delete(r)
        db.session.commit()

    def test_theater_insert(self):  # unit test for inserting theater
        t = Theater(name='Cool Theater', id=1000000, location='Austin, Texas',
                    google_maps='maps.com', img='imgexample')
        db.session.add(t)
        db.session.commit()
        r = db.session.query(Theater).filter_by(id=1000000).one()
        self.assertEqual(str(r.id), '1000000')

        r = db.session.query(Theater).filter_by(id='1000000').first()
        db.session.delete(r)
        db.session.commit()

    def test_theater_edit(self):  # unit test for editing theater
        t = Theater(name='Cool Theater', id=1000000, location='Austin, Texas',
                    google_maps='maps.com', img='imgexample')
        db.session.add(t)
        db.session.commit()
        r = db.session.query(Theater).filter_by(id=1000000).one()
        r.location = 'Round Rock, Texas'
        r = db.session.query(Theater).filter_by(id=1000000).one()
        self.assertEqual(str(r.location), 'Round Rock, Texas')

        r = db.session.query(Theater).filter_by(id='1000000').first()
        db.session.delete(r)
        db.session.commit()

    def test_theater_delete(self):  # unit test for deleting theater
        t = Theater(name='Cool Theater', id=1000000, location='Austin, Texas',
                    google_maps='maps.com', img='imgexample')
        db.session.add(t)
        db.session.commit()
        r = db.session.query(Theater).filter_by(id=1000000).one()
        db.session.delete(r)
        db.session.commit()
        r = db.session.query(Theater).filter_by(id=1000000).first()
        self.assertEqual(r, None)

    def test_services_insert(self):  # unit test for inserting services
        s = StreamingService(name='newflix', id='9999999', website='example.com', logo='img.src',
                             country_origin='US', base_price=10.42, ad_free_available='No',
                             user_base=21, revenue2022=31)
        db.session.add(s)
        db.session.commit()
        r = db.session.query(StreamingService).filter_by(id='9999999').one()
        self.assertEqual(str(r.id), '9999999')
        r = db.session.query(StreamingService).filter_by(id='9999999').first()
        db.session.delete(r)
        db.session.commit()

    def test_services_update(self):  # unit test for updating a streaming service
        s = StreamingService(name='newflix', id='9999999', website='example.com', logo='img.src',
                             country_origin='US', base_price=10.42, ad_free_available='No',
                             user_base=21, revenue2022=31)
        db.session.add(s)
        db.session.commit()
        r = db.session.query(StreamingService).filter_by(id='9999999').one()
        r.country_origin = 'UK'
        r = db.session.query(StreamingService).filter_by(id='9999999').one()
        self.assertEqual(str(r.country_origin), 'UK')

        r = db.session.query(StreamingService).filter_by(id='9999999').first()
        db.session.delete(r)
        db.session.commit()

    def test_services_delete(self):  # unit test for deleting a streaming service
        s = StreamingService(name='newflix', id='9999999', website='example.com', logo='img.src',
                             country_origin='US', base_price=10.42, ad_free_available='No',
                             user_base=21, revenue2022=31)
        db.session.add(s)
        db.session.commit()
        r = db.session.query(StreamingService).filter_by(
            id='9999999').one()
        db.session.delete(r)
        db.session.commit()
        r = db.session.query(StreamingService).filter_by(id='9999999').first()
        self.assertEqual(r, None)


if __name__ == '__main__':
    with app.app_context():
        unittest.main()
# end of code
