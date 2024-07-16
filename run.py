from flask import Flask, request, render_template_string
from datetime import datetime, timedelta

app = Flask(__name__)

# Constants
START_DATE = datetime(datetime.now().year, 2, 24)  # Start date: 24th of February of the current year
END_DATE = START_DATE + timedelta(days=365*3)  # End date: Three years from the start date
TOTAL_PERIOD_DAYS = (END_DATE - START_DATE).days
TOTAL_ALLOWED_MILEAGE = 60000  # Total allowed mileage in kilometers

# HTML form for input
INPUT_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Car Mileage Checker</title>
    <!-- Bootstrap CSS CDN -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<div class="container mt-5">
    <h2 class="mb-3">Enter your car's mileage (km):</h2>
    <form action="/check" method="post" class="mb-3">
        <div class="form-group">
            <input type="number" class="form-control" name="mileage" required>
        </div>
        <button type="submit" class="btn btn-primary">Check</button>
    </form>
</div>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""

@app.route('/')
def home():
    return INPUT_FORM

@app.route('/check', methods=['POST'])
def check_mileage():
    user_mileage = int(request.form['mileage'])
    today = datetime.now()
    days_elapsed = (today - START_DATE).days
    if days_elapsed < 0:
        message = "The mileage tracking period hasn't started yet."
        alert_class = "alert-warning"
    elif days_elapsed > TOTAL_PERIOD_DAYS:
        days_elapsed = TOTAL_PERIOD_DAYS  # Cap at the end of the period
    # Calculate pro-rated allowed mileage
    allowed_mileage = (days_elapsed / TOTAL_PERIOD_DAYS) * TOTAL_ALLOWED_MILEAGE
    mileage_difference = user_mileage - allowed_mileage

    if mileage_difference <= 0:
        message = f"Your mileage is within the allowed limit by <strong>{abs(mileage_difference):.2f}</strong> km. ({user_mileage}/{allowed_mileage:.2f})"
        alert_class = "alert-success"
    else:
        message = f"Your mileage exceeds the allowed limit by <strong>{mileage_difference:.2f}</strong> km! ({user_mileage}/{allowed_mileage:.2f})"
        alert_class = "alert-danger"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mileage Check Result</title>
        <!-- Bootstrap CSS CDN -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
    <div class="container mt-5">
        <div class="alert {alert_class}" role="alert">
            {message}
        </div>
        <a href="/" class="btn btn-primary">Check Another Mileage</a>
    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)