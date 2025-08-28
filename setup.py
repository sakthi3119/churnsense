from setuptools import setup, find_packages

setup(
    name="churn-prediction",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask==2.0.3',
        'numpy==1.20.3',
        'scikit-learn==1.0.2',
        'pandas==1.3.3',
        'gunicorn==20.1.0',
        'Werkzeug==2.0.3',
        'python-dotenv==0.19.2',
        'scipy==1.7.3',
        'joblib==1.1.0',
        'threadpoolctl==3.1.0'
    ],
    python_requires='>=3.9,<3.10'
)
