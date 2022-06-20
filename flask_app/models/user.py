from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login_user_schemas').query_db(query)
        users = []
        for r in results:
            users.append( cls(r) )
        return users
    @classmethod
    def get_all(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s); "
        return  connectToMySQL('login_user_schemas').query_db(query, data)
        
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('login_user_schemas').query_db(query, data)
        return cls(results[0])
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('login_user_schemas').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_vaild = True
        if len(user['first_name']) < 3:
            flash('first name must be at least 3 characters.', 'register')
            is_vaild = False
        if len(user['last_name']) < 3:
            flash('Last Name must be at least 3 characters.','register')
            is_vaild = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invaild email', 'register')
            is_vaild = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.', 'register')
            is_vaild = False
        if user['password'] != user['confirm_password']:
            flash('Passwords dont match', 'register')
        return is_vaild