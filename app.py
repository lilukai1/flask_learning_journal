from flask import (Flask, g, render_template, flash, redirect, 
                    url_for, make_response, abort)

import models
import forms

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'sdkghaawoienvoweavnwoainvweoaghwesoisudaygnaewagaieuahgv;lanwefoai;o'

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/', methods=('GET', 'POST'))
def index():
    stream = models.Entry.select().limit(100)
    return render_template('index.html', stream=stream)


@app.route("/new", methods=('GET', 'POST'))
def new_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        print('validated')
        models.Entry.create(
            content=form.content.data.strip(),
            title = form.title.data.strip(),
            timestamp = form.timestamp.data, 
            time_spent = form.time_spent.data,
            resources = form.resources.data.strip()
            )
        flash("Entry Saved", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    try:
        entry = models.Entry.get(entry_id)
    except:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/entry/<int:entry_id>/edit', methods=('GET', 'POST'))
def edit_entry(entry_id):
    try:
        entry = models.Entry.get(entry_id)
    except:
        abort(404)

    entry_dict = {'content':entry.content, 
                    'title': entry.title, 
                    'timestamp': entry.timestamp, 
                    'time_spent':entry.time_spent, 
                    'resources': entry.resources
                    }
    form = forms.EntryForm(data=entry_dict)

    if form.validate_on_submit():
        q = models.Entry.update(
            content=form.content.data.strip(),
            title = form.title.data.strip(),
            timestamp = form.timestamp.data, 
            time_spent = form.time_spent.data,
            resources = form.resources.data.strip()
            ).where(models.Entry.id==entry_id)
        q.execute()
        flash("Entry Updated!", "success")
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry, form=form)


@app.route('/entry/<int:entry_id>/delete', methods=('GET', 'POST'))
def delete_entry(entry_id):
    try:
        entry = models.Entry.get(entry_id)
        entry.delete_instance()
        flash("Entry Deleted.", "success")
        return redirect(url_for('index'))
    except:
        abort(404)
    return render_template('index.html', entry=entry)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    # try:
    #     models.User.create_user(
    #         username='anniewiley',
    #         email='annienwiley@gmail.com',
    #         password='password',
    #         admin=True

    #     )
    # except ValueError:
    #     pass
    app.run(debug=DEBUG, port=PORT, host=HOST)