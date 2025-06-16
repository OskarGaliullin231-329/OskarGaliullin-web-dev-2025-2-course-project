from flask import Flask, render_template, request
import markdown

app = Flask(__name__)

notes = []
# for i in range(40):
#     notes.append({
#         "note_id": i,
#         "user_id": 1,
#         "text": f'Some text for note {i} ну и немного русского',
#         "name": f'Имя of note {i}'
#     })

# notes[1]["text"] = '''
# text with [**markdown**](https://www.markdownguide.org/extended-syntax/) *marking*


# ``` 
# char* lets_add_some_code(int here) {
#     return here;
# }
# ```
# '''


@app.route('/')
def index():
    return render_template('note_view/index.html', notes_arr=notes)

# , text=markdown.markdown(notes[1]["text"])

# @app.route('')
# def note():
#     return render_template
