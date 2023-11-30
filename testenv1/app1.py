### Proyecto Django: Implementar un sistema básico de votaciones.

# - [ ] Modelos para `Poll`, `Choice`, y `Vote` con relaciones adecuadas.
# - [ ] Views para mostrar encuestas, votar, y ver resultados.


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:121224@localhost:5432/test-db'  # Use your own URI
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Poll(db.Model):
    __tablename__ = 'polls'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    choices = db.relationship('Choice', backref='poll', lazy=True)

class Choice(db.Model):
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/polls', methods=['POST'])
def create_poll():
    question = request.json.get('question')
    answers = request.json.get('answers')
    poll = Poll(question=question)
    for answer in answers:
        choice = Choice(answer=answer, poll=poll)
        db.session.add(choice)
    db.session.commit()
    return jsonify({'poll_id': poll.id}), 201

@app.route('/polls/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    return jsonify({
        'question': poll.question,
        'choices': [{'id': choice.id, 'answer': choice.answer, 'votes': choice.votes} for choice in poll.choices]
    })

@app.route('/polls/<int:poll_id>/vote', methods=['POST'])
def vote(poll_id):
    choice_id = request.json.get('choice_id')
    choice = Choice.query.get_or_404(choice_id)
    if choice.poll_id != poll_id:
        return jsonify({'error': 'invalid poll id'}), 400
    vote = Vote(choice_id=choice_id)
    choice.votes += 1
    db.session.add(vote)
    db.session.commit()
    return jsonify({'message': 'votes counted'}), 200
