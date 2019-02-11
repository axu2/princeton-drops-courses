import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from models import Course
from datetime import datetime

app = dash.Dash()
app.title = 'When To Drop Princeton Courses!'
server = app.server
COS126 = 40038

options = []
for c in Course.objects().order_by('dept', 'num'):
    name = c.dept + " " + c.num + ": " + c.title
    options.append({'label': name, 'value': c.course_id})

app.layout = html.Div([
    html.Div(
        [
            dcc.Markdown(
                '''
                ### Course Enrollment at Princeton University
                A visualization of Princeton course enrollment over time during Spring 2019. All data was obtained by scraping the Registrar website daily.
                '''.replace('  ', ''),
                className='eight columns offset-by-two'
            )
        ],
        className='row',
        style={'text-align': 'center', 'margin-bottom': '15px'}
    ),
    dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value=COS126
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(course_id):
    course = Course.objects(course_id=int(course_id)).first()
    name = course.dept + " " + course.num + ": " + course.title
    return {
        'data': [{
            'x': course.dates,
            'y': course.enroll
        }],
        'layout': {
            'xaxis':{
                'title':'Time'
            },
            'yaxis':{
                'title':'Number of Students'
            },
            'title': '{}'.format(name)
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
    
