from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request, send_from_directory, current_app, jsonify
from flask_login import current_user, login_required

from app import db
from app.main.forms import ApplyForm
from app.models import Question, Submission, PersonalitySchema
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
def index():
    if current_app.config["BETA_MODE_ON"]:
        flash("Welcome to our Beta. If you run into any trouble or find any bugs, please leave me a message using the button in the bottom right corner.")
    return render_template('home.html')

@bp.route('/robots.txt')
@bp.route('/sitemap.xml')
def static_from_root():
    return send_from_directory('static', request.path[1:])

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@bp.route('/impressum')
def impressum():
    return render_template('impressum.html')

@bp.route('/interview', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplyForm(obj=current_user, meta={'csrf': False})
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.linkedin_url = form.linkedin_url.data

        s = Submission(applicant=current_user._get_current_object())

        db.session.add(s)
        db.session.commit()

        session['submission'] = s.to_dict()

        msg = 'Thanks, submission requested for user {}, mail={}'.format(
            form.name.data, current_user.email)
        flash(msg)
        return redirect(url_for('main.find_question'))

    questions = Question.query.order_by("order_pos asc").all()
    return render_template('apply.html', questions=questions, form=form)


@bp.route('/questions')
def find_question():
    current_submission = session.get('submission')
    if current_submission is not None:
        video_settings = {
            'controls': True,
            'fluid': True,
            'plugins': {
                'record': {
                    'audio': True,
                    'video': True,
                    'debug': False
                }
            }
        }
        questions = Question.query.order_by("order_pos asc").all()
        return render_template('video.html', questions=questions, video_settings=video_settings, submission=current_submission)
    return redirect(url_for('main.apply'))

@bp.route('/personality', methods=['GET', 'POST'])
def get_personality():
    if request.method == 'POST':
        answers_json = request.get_json()['personality']
        big_five = get_big_five(answers_json)
        current_app.logger.info(big_five)

        sub = Submission.from_dict(session['submission'])
        sub.personality = PersonalitySchema().dump(big_five).data
        db.session.commit()
        return jsonify(big_five)
        
    return render_template('survey.html')


def get_big_five(answers):
    scoring_instructions = {
        "extraversion": ["1", "6R", "11", "16", "21R", "26", "31R", "36"],
        "agreeableness": ["2R", "7", "12R", "17", "22", "27R", "32", "37R", "42"],
        "conscientiousness": ["3", "8R", "13", "18R", "23R", "28", "33", "38", "43R"],
        "neuroticism": ["4", "9R", "14", "19", "24R", "29", "34R", "39"],
        "openness": ["5", "10", "15", "20", "25", "30", "35R", "40", "41R", "44"],
    }

    def f(instructions):
        total = 0
        for i in instructions:
            if i.strip('R') in answers:
                if i.endswith('R'):
                    total += (6 - int(answers[i.strip('R')]))
                else:
                    total += int(answers[i])
        return round(total / len(instructions), 2)

    return {k: f(v) for k, v in scoring_instructions.items()}