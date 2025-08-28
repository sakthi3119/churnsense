from setuptools import setup, find_packages

setup(
    name="churn-prediction",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.3,<3.0.0',
        'numpy>=1.21.0,<2.0.0',
        'scikit-learn>=1.0.2,<2.0.0',
        'pandas>=1.3.3,<2.0.0',
        'gunicorn>=20.1.0,<21.0.0',
        'Werkzeug>=2.0.3,<3.0.0',
        'python-dotenv>=0.19.2,<1.0.0',
        'scipy>=1.7.3,<2.0.0',
        'joblib>=1.1.0,<2.0.0',
        'threadpoolctl>=3.1.0,<4.0.0',
        'setuptools>=59.6.0,<60.0.0',
        'wheel>=0.37.1,<0.39.0'
    ],
    python_requires='>=3.9,<3.10',
    setup_requires=[
        'setuptools>=59.6.0,<60.0.0',
        'wheel>=0.37.1,<0.39.0'
    ]
)
