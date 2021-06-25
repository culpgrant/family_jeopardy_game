from flask import Flask, render_template, redirect, url_for, flash
from form import PlayerForm, QuestionForm, AnswerForm
import Data_Pull

app = Flask(__name__)

app.config['SECRET_KEY'] = '79g9626d80785cf145dd05db66bf2f83'

full_dataset = Data_Pull.get_data()


class CurrentScore:
    def __init__(self, my_score):
        self.score = my_score

    def get_current_score(self):
        return self.score

    def increment_score(self, prize):
        self.score += prize
        return self.score

    def reset_score(self):
        self.score = 0
        return self.score


class QuestionDataset:
    def __init__(self, my_dataset):
        self.dataset = my_dataset

    def get_unique_players(self):
        unique = set()
        for index, data in self.dataset.items():
            unique.add(data['Player'])
        return unique

    def get_question_name(self, q_id):
        for index, data in self.dataset.items():
            if data['Internal_ID'] == int(q_id):
                return data['Question']

    def filter_questions_player(self, player):
        filtered_data = []
        for index, data in self.dataset.items():
            if data['Player'] == player and data['Used'] == 'N':
                filtered_data.append(data)
        return filtered_data

    def update_question_used(self, q_id):
        for index, data in self.dataset.items():
            if data['Internal_ID'] == int(q_id):
                data['Used'] = "Y"

    def get_ques_choices(self, q_id):
        for index, data in self.dataset.items():
            if data['Internal_ID'] == int(q_id):
                question_choices = data['Choices_Comma_Seperated'].split(",")
                return question_choices

    def get_question_answer(self, q_id):
        for index, data in self.dataset.items():
            if data['Internal_ID'] == int(q_id):
                return str(data['Answers'])

    def get_question_prize(self, q_id):
        for index, data in self.dataset.items():
            if data['Internal_ID'] == int(q_id):
                return int(data['Prize'])

    def reset_dataset(self):
        for index, data in self.dataset.items():
            data['Used'] = "N"


# Initializing the Dataset
jeapordy_dataset = QuestionDataset(full_dataset)
unique_players = jeapordy_dataset.get_unique_players()

# Initializing the score
score_class = CurrentScore(0)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    global question_player_form
    question_player_form = PlayerForm()
    # Set the Choices
    question_player_form.player_name.choices = list(unique_players)
    if question_player_form.validate_on_submit():
        return redirect(url_for('question'))
    return render_template('home.html', title='Home', question_player_form=question_player_form,
                           score=score_class.score)


@app.route("/question", methods=["GET", "POST"])
def question():
    global question_form
    question_form = QuestionForm()
    # Getting who the player selected was
    player_selected = question_player_form.player_name.data
    # Filtering the Dataset
    filtered_data = jeapordy_dataset.filter_questions_player(player_selected)
    # Pass the questions as to Flask Form as a list
    filtered_questions = []
    for row in filtered_data:
        filtered_questions.append((row['Internal_ID'], f"{row['Prize']} - {row['Question']}"))
    # Setting the choice to the questions above
    question_form.question.choices = filtered_questions
    if question_form.validate_on_submit():
        # Mark the question as being used
        id_ques_selected = question_form.question.data
        jeapordy_dataset.update_question_used(id_ques_selected)
        return redirect(url_for('answer'))
    return render_template('question.html', title='Question', question_form=question_form, score=score_class.score)


@app.route("/answer", methods=["GET", "POST"])
def answer():
    answer_form = AnswerForm()

    # Getting the Question that was selected
    ques_id = question_form.question.data

    # Getting the Question name that was selected
    ques_name = jeapordy_dataset.get_question_name(ques_id)

    # Getting the Prize for that question
    ques_prize = jeapordy_dataset.get_question_prize(ques_id)

    # Getting the Choices for that Question
    ques_choices = jeapordy_dataset.get_ques_choices(ques_id)

    # Getting the Correct Answer
    cor_answer = jeapordy_dataset.get_question_answer(ques_id)

    # Setting the choice to the choices above
    answer_form.answer_ques.choices = ques_choices
    if answer_form.validate_on_submit():
        # Check if the answer is correct
        if str(cor_answer).strip() == str(answer_form.answer_ques.data).strip():
            flash(f"Correct Answer! Question was worth {ques_prize} points!", "success")
            score_class.score += ques_prize
        else:
            flash(f"Incorrect Answer. The correct answer is {cor_answer}", "danger")
        # Redirect them to the home screen
        return redirect('home')
    return render_template('answer.html', title='Answer', answer_form=answer_form, ques_name=ques_name,
                           score=score_class.score)


@app.route("/reset", methods=["GET", "POST"])
def reset():
    # Reset the Score
    score_class.reset_score()
    # Reset the Dataset
    jeapordy_dataset.reset_dataset()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
