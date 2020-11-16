# Jupyter Dash in Jupyter Lab for MacOS

Sources:
[Charming Data](https://drive.google.com/file/d/1ZRtQUie0y2k3dXz_MM8s29WQaSrM9bDn/view)
[Xing Han Lu](https://medium.com/plotly/introducing-jupyterdash-811f1f57c02e)
[Plotly](https://plotly.com/python/getting-started/#jupyterlab-support-python-35)
[Real Python](https://realpython.com/intro-to-pyenv/#virtual-environments-and-pyenv)

## Python Virtual Environment:

1. Open the terminal and ```cd``` into the project main directory, or create a folder where you would like to start developing your project/app.
2. Create virtual environment: 
   ```pyenv virtualenv <python_version> <environment_name>```
3. Activate your new environment:
   ```pyenv local <environment_name>```
4. Install Node using homebrew (NPV included):
   ~~```brew install node```~~ <-- **Cant get that one to work, please advice if able.**
   [Download Node](https://nodejs.org/dist/v14.15.0/node-v14.15.0.pkg)
5. Install required libraries:
   1. ```python3 -m pip install numpy```
   2. ```python3 -m pip install pandas```
   3. ```python3 -m pip install plotly```
   4. ```python3 -m pip install dash```
   5. ```python3 -m pip install Jupyterlab```
6. To run Dash inside Jupyter lab:
   ```python3 -m pip install jupyter-dash```
7. To run Plotly figures inside jupyter lab:
   ```python3 -m pip install ipywidgets```
8. Add JupyterLab extension for renderer support:
   1. Required: ```jupyter labextension install jupyterlab-plotly```
   Example: ```fig.show()```
   1. Optional widget extension: ```jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget```
   Example: ```fig```
9.  Rebuild:
   ```jupyter lab build```
10. Start Jupyterlab
   ```jupyter lab```
11. Save dependencies for later:
    ```python3 -m pip freeze > requirements.txt```
12. Install dependencies:
    ```python3 -m pip install -r requirements.txt```

## Test code

### Inline:

```python
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Load Data
df = px.data.tips()
# Build App
app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("JupyterDash Demo"),
    dcc.Graph(id='graph'),
    html.Label([
        "colorscale",
        dcc.Dropdown(
            id='colorscale-dropdown', clearable=False,
            value='plasma', options=[
                {'label': c, 'value': c}
                for c in px.colors.named_colorscales()
            ])
    ]),
])
# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("colorscale-dropdown", "value")]
)
def update_figure(colorscale):
    return px.scatter(
        df, x="total_bill", y="tip", color="size",
        color_continuous_scale=colorscale,
        render_mode="webgl", title="Tips"
    )
# Run app and display result inline in the notebook
app.run_server(mode='inline')
```

### External:

```python
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Load Data
df = px.data.tips()
# Build App
app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("JupyterDash Demo"),
    dcc.Graph(id='graph'),
    html.Label([
        "colorscale",
        dcc.Dropdown(
            id='colorscale-dropdown', clearable=False,
            value='plasma', options=[
                {'label': c, 'value': c}
                for c in px.colors.named_colorscales()
            ])
    ]),
])
# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("colorscale-dropdown", "value")]
)
def update_figure(colorscale):
    return px.scatter(
        df, x="total_bill", y="tip", color="size",
        color_continuous_scale=colorscale,
        render_mode="webgl", title="Tips"
    )
# Run app and display result inline in the notebook
app.run_server(mode='external')
```

### JupyterLab:

```python
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Load Data
df = px.data.tips()
# Build App
app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("JupyterDash Demo"),
    dcc.Graph(id='graph'),
    html.Label([
        "colorscale",
        dcc.Dropdown(
            id='colorscale-dropdown', clearable=False,
            value='plasma', options=[
                {'label': c, 'value': c}
                for c in px.colors.named_colorscales()
            ])
    ]),
])
# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("colorscale-dropdown", "value")]
)
def update_figure(colorscale):
    return px.scatter(
        df, x="total_bill", y="tip", color="size",
        color_continuous_scale=colorscale,
        render_mode="webgl", title="Tips"
    )
# Run app and display result inline in the notebook
app.run_server(mode='jupyterlab')
```

