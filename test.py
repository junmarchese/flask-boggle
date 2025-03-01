from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """To do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Ensure information is in the session and display HTML."""
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Remaining:', response.data)
    
    def test_valid_word(self):
        """Test if word is valid by modifying board in session"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"]
                ]

            response = self.client.get('/check-word?word=cat')
            self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary."""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-a-word')
    