from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


# Creating the forms
class PlayerForm(FlaskForm):
    player_name = SelectField(u'Select Your Person:',
                              validators=[DataRequired()])
    submit_person_choice = SubmitField('Choose Person')


class QuestionForm(FlaskForm):
    question = SelectField(u'Select The Question:',
                           validators=[DataRequired()])
    submit_question_choice = SubmitField('Choose Question')


class AnswerForm(FlaskForm):
    answer_ques = SelectField(u'Choose the Answer:',
                              validators=[DataRequired()])
    submit_answer = SubmitField("Submit Answer")
