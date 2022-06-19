from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.thought import Thought

# @app.route('/ninjas')
# def ninjas():
#    return render_template('ninja.html')

@app.route('/create/thought', methods=['POST'])
def create_thought():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Thought.validate_thought(request.form):
        return redirect('/home')
    data ={ 
        "thought": request.form['thought'],
        "user_id": session['user_id']
    }
    Thought.save(data)
    return redirect('/')

""" @app.route('/thought/<int:id>')
def show_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'thought_id' : id,
        'user_id': session['user_id']
    }
    myThought = Thought.get_one(data)
    return render_template('showOneNinja.html', thought=myThought,  user=User.get_by_id(data),) """

@app.route('/thought/<int:id>/like', methods=['GET','PUT'])
def like_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'thought_id': id,
        'user_id': session['user_id'],
        
    }

    Thought.addLike(data)
    updatedThought = Thought.getUsersWhoLiked(data)
    updatedData = {
        'thought_id': id,
        'likes': updatedThought.likes
    }
    Thought.update(updatedData)
    thoughts = Thought.get_all()
    return  render_template('index.html', thought=updatedThought,  user=User.get_by_id(data), all_thoughts=thoughts)

@app.route('/thought/<int:id>/unlike', methods=['GET','PUT'])
def unlike_thought(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'thought_id': id,
        'user_id': session['user_id'],
    }
    User.unLike(data)
    return redirect(request.referrer)
    #updatedThought = Thought.getUsersWhoLiked(data)
    
    #return render_template('index.html', Thought=updatedThought,  user=User.get_by_id(data))
