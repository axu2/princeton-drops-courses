import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from models import Course
from datetime import datetime

app = dash.Dash()
server = app.server

options = []
for c in Course.objects():
    name = c.dept + " " + c.num + ": " + c.title
    options.append({'label': name, 'value': c.course_id})

app.layout = html.Div([
    html.H1('Course Enrollments'),
    dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value=40038
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(course_id):
    course = Course.objects(course_id=int(course_id)).first()

    return {
        'data': [{
            'x': course.dates,
            'y': course.enroll
        }]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
    