
# Tools needed to create the Dash app
from dash import Dash, html, dcc, Input, Output

# Dash application
app = Dash(__name__)

# Layout
app.layout = html.Div([

    # Title
    html.H1("BMI Calculator"),

    # Input box for height
    html.P("Enter your height:"),
    dcc.Input(id="height", type="number"),

    # Dropdown menu for height units
    dcc.Dropdown(["Meters", "Feet"], "Meters", id="height_unit"),

    # Input box for weight
    html.P("Enter your weight:"),
    dcc.Input(id="weight", type="number"),

    # Dropdown menu for weight units
    dcc.Dropdown(["Kilograms", "Pounds"], "Kilograms", id="weight_unit"),

    # Display the calculated BMI
    html.H2(id="result")
])

# The calculation updates whenever an input changes
@app.callback(
    Output("result", "children"),
    Input("height", "value"),
    Input("height_unit", "value"),
    Input("weight", "value"),
    Input("weight_unit", "value")
)

# Function that calculates BMI
def calculate(height, height_unit, weight, weight_unit):

    # Check if the user entered both height and weight
    if height is None or weight is None:
        return "Enter your height and weight"

    # Make sure both values are greater than zero
    if height <= 0 or weight <= 0:
        return "Enter values greater than zero"

    # Convert height from feet to meters if needed
    if height_unit == "Feet":
        height = height * 0.3048

    # Convert weight from pounds to kilograms if needed
    if weight_unit == "Pounds":
        weight = weight * 0.453592

    # Calculate BMI using weight (kg) / height (m) squared
    bmi = weight / (height ** 2)

    # BMI rounded to two decimal places
    return f"Your BMI is: {bmi:.2f}"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
