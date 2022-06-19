from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Thought:
    db = 'users_and_thoughts'
    def __init__(self, data):
        self.id = data['id']
        self.thought = data['thought']
        self.likes=data['likes']
        self.user_id= data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_who_liked=[]
        self.creator=""

    @classmethod
    def get_all(cls):
        query = "SELECT * from thoughts LEFT JOIN users on thoughts.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        thoughts = []
        for row in results:
            print(row)
            thoughts.append(row)
        return thoughts

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM thoughts WHERE id = %(thought_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO thoughts (thought, user_id ) VALUES ( %(thought)s , %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = 'UPDATE thoughts SET likes = %(likes)s WHERE id=%(thought_id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO thoughts_was_like_from_users (thoughts_id,users_id) VALUES (%(thought_id)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM thoughts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def getUsersWhoLiked(cls, data):
        query = "SELECT * FROM thoughts_was_like_from_users LEFT JOIN thoughts ON thoughts_was_like_from_users.thoughts_id = thoughts.id LEFT JOIN users ON thoughts_was_like_from_users.users_id = users.id WHERE thoughts.id = %(thought_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        myThought = Thought.get_one(data)
        for row in results:
            myThought.users_who_liked.append(row['email'])
        myThought.likes=len(myThought.users_who_liked)
        print(myThought.users_who_liked)
        return myThought


    

    @staticmethod
    def validate_thought(thought):
        is_valid = True
        if len(thought['thought']) < 5:
            flash("Thought must be at least 5 characters","addThought")
            is_valid= False
        if len(thought['thought']) < 1:
            flash("Thought is required","addThought")
            is_valid= False
        return is_valid


    @classmethod
    def get_userThoughts(cls, data):
        query = "SELECT * FROM thoughts LEFT JOIN users on thoughts.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        thoughts = []
        for row in results:
            print(row)
            thoughts.append(row)
        return thoughts