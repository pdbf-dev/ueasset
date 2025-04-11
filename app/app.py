from flask import Flask, render_template, request, redirect, url_for
from db import Session, File, Tag

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    session = Session()
    tags = session.query(Tag).order_by(Tag.name).all()
    selected_tag = request.args.get('tag')

    if selected_tag:
        files = session.query(File).join(File.tags).filter(Tag.name == selected_tag).all()
    else:
        files = session.query(File).all()

    session.close()
    return render_template('index.html', files=files, tags=tags, selected_tag=selected_tag)

@app.route('/file/<int:file_id>', methods=['GET', 'POST'])
def file_detail(file_id):
    session = Session()
    file = session.query(File).get(file_id)

    if request.method == 'POST':
        tag_name = request.form['tag_name'].strip()
        if tag_name:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
            if tag not in file.tags:
                file.tags.append(tag)
                session.commit()
        return redirect(url_for('file_detail', file_id=file_id))

    session.close()
    return render_template('file_detail.html', file=file)

if __name__ == '__main__':
    app.run(debug=True)
