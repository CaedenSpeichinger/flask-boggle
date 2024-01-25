from flask import session
from app import app 
from boggle import Boggle
from unittest import TestCase




class test(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        print('Setup')

    def test_start(self):
        """checkin the responce in the sesion and making sure there is no error code"""

        with self.client:
            response = self.client.get('/')
            html = responce.get_data(as_text=true)
            self.assertEqual(responce.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('nplays'))
            self.assertIsNone(session.get('highscore'))
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
            
            
    
            

    def test_check_word(self):
        """Filling in the board to see if each word test case passes"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["C", "A", "S", "E", "T"], 
                                 ["A", "A", "T", "T", "I"], 
                                 ["N", "A", "M", "E", "M"], 
                                 ["L", "A", "T", "T", "E"], 
                                 ["S", "M", "A", "E", "T"]]
        response = self.client.get('/check-word?word=case')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=time')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=name')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=latte')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """make sure it can register words not on the board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=onomatopoeia')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """seeing if it takes made up words that arent on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=honhowchimichanga')
        self.assertEqual(response.json['result'], 'not-word')
