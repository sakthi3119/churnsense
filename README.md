# ChurnSense - Customer Churn Prediction

ChurnSense is a web application that predicts customer churn using machine learning. It helps businesses identify customers who are likely to stop using their services, allowing for proactive retention strategies.

## Features

- Modern, responsive UI with smooth animations
- Real-time churn prediction
- Confidence level visualization
- Detailed prediction results
- Mobile-friendly design
- Serverless deployment with Vercel

## Prerequisites

- Python 3.9 (required for Vercel deployment)
- pip (Python package manager)
- Vercel account (for deployment)
- Git (for version control)

## Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Customer-Churn-Prediction-Project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application locally:
   ```bash
   python app.py
   ```

## Vercel Deployment

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to your Vercel account:
   ```bash
   vercel login
   ```

3. Deploy to Vercel:
   ```bash
   vercel
   ```

4. Follow the prompts to complete the deployment.

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Flask configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key
```

## Project Structure

```
.
├── api/                  # API routes
│   └── index.py         # API entry point
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── app.py               # Main application
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
├── vercel-build.sh     # Build script
└── runtime.txt         # Python version specification
```

## Troubleshooting

- If you encounter module import errors, ensure all dependencies are installed
- Check the Vercel deployment logs for specific error messages
- Make sure all required files are included in the deployment (check `.vercelignore`)

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository.

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Customer-Churn-Prediction
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Deployment

### Heroku

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

4. Deploy your code:
   ```bash
   git push heroku main
   ```

5. Open the app in your browser:
   ```bash
   heroku open
   ```

### PythonAnywhere

1. Upload your code to a GitHub repository
2. Create a PythonAnywhere account and open a new console
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```
4. Create a virtual environment and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.8 venv
   pip install -r requirements.txt
   ```
5. Set up a new web app through the PythonAnywhere dashboard
6. Configure the WSGI file to point to your app

## Project Structure

```
.
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── static/                # Static files (CSS, JS, images)
│   ├── script.js          # Frontend JavaScript
│   └── styles.css         # Custom styles
├── templates/             # HTML templates
│   └── index.html         # Main application page
└── mlmodel.sav           # Trained machine learning model
```

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn
- **Styling**: Custom CSS with Flexbox and Grid
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Dataset used for training the model: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Inspired by various customer churn prediction projects
