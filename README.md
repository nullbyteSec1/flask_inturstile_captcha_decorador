# flask_inturstile_captcha_decorador
A simple decorator for integrating Cloudflare Turnstile CAPTCHA into Flask applications.

## Overview

This repository provides a lightweight Python decorator to protect your Flask routes with Cloudflare Turnstile. It verifies the CAPTCHA response from the client before allowing the request to proceed.

## Installation

1.  **Dependencies:** Ensure you have `flask` and `httpx` installed.

    ```sh
    pip install flask httpx
    ```

2.  **Add the decorator file:** Copy the `turnstile_decorator.py` file into your Flask project directory.

## Usage

Follow these steps to integrate the decorator into your Flask application.

### 1. Backend Setup

In your main Flask application file (e.g., `app.py`), import and initialize the `FlaskTurnstile` class. Then, apply the `@turnstile.required` decorator to any route you want to protect.

You will need your **Site Key** and **Secret Key** from your Cloudflare Turnstile dashboard.

```python
# app.py
from flask import Flask, render_template, jsonify
from turnstile_decorator import FlaskTurnstile

app = Flask(__name__)

# Replace with your actual Cloudflare Turnstile keys
TURNSTILE_SITE_KEY = "YOUR_CLOUDFLARE_SITE_KEY"
TURNSTILE_SECRET_KEY = "YOUR_CLOUDFLARE_SECRET_KEY"

# Initialize the FlaskTurnstile class
turnstile = FlaskTurnstile(
    site_key=TURNSTILE_SITE_KEY,
    secret_key=TURNSTILE_SECRET_KEY
)

@app.route("/")
def index():
    # Pass the site key to the template
    return render_template("index.html", site_key=TURNSTILE_SITE_KEY)

@app.route("/protected-form", methods=["POST"])
@turnstile.required
def protected_form():
    # This code will only run if the Turnstile CAPTCHA is valid
    return jsonify({"success": True, "message": "Form submitted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)

```

### 2. Frontend Setup

In your HTML template, you need to include the Cloudflare Turnstile script and place the widget inside your form.

Create a `templates/index.html` file:

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Turnstile Demo</title>
    <!-- 1. Include the Turnstile script -->
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</head>
<body>
    <h1>Protected Form</h1>
    <form id="myForm" action="/protected-form" method="POST">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <br><br>

        <!-- 2. Add the Turnstile widget to your form -->
        <div class="cf-turnstile" data-sitekey="{{ site_key }}"></div>
        <br>
        
        <button type="submit">Submit</button>
    </form>

    <div id="result"></div>

    <script>
        // Optional: Handle the form submission with JavaScript to display the result
        document.getElementById('myForm').addEventListener('submit', async function(event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const resultDiv = document.getElementById('result');

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();

                if (response.ok) {
                    resultDiv.innerHTML = `<p style="color:green;">${data.message}</p>`;
                } else {
                    resultDiv.innerHTML = `<p style="color:red;">Error: ${data.message}</p>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<p style="color:red;">A network error occurred.</p>`;
            }
             // Reset the Turnstile widget after submission
            turnstile.reset();
        });
    </script>
</body>
</html>
```

When the user submits the form, the decorator will verify the `cf-turnstile-response` token sent in the form data. If the verification fails, it will return a `403 Forbidden` response with a JSON error message.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
