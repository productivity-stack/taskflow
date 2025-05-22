# Taskflow API

A productivity-focused task management platform built with Django REST Framework.


## 1. Clone the Repository

To clone the repository initially:

```bash
git clone https://github.com/productivity-stack/taskflow.git
```

If you have already cloned the repository and want to update it, use the following command:

```bash
git pull origin master
```


## 2. System Requirements

You'll need Python 3, python3-pip, and python3-venv to be installed on your machine:

On Linux, via apt:

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

Install Python on Windows:

1. Download the latest version of Python from [python.org](https://www.python.org/downloads/).
2. Run the installer and ensure to select "Add Python to PATH" during installation to add Python to your system's PATH for use in Command Prompt.


## 3. Python Environment

For maintaining a clean development environment, it's recommended to use a virtual environment for installing application-specific packages. There are various methods to create virtual environments, such as using Pipenv. Below is an example demonstrating how to set up a virtual environment using native tools:

Windows:
```bash
cd taskflow
python -m venv venv
```

Linux:
```bash
cd taskflow
python3 -m venv .venv
```

**NOTE**: Ensure you add your virtual environment directory to .gitignore to avoid committing unnecessary files to your repository.

Then, install the requirements in your virtual environment. But first, you need to activate the environment:

Windows:
```bash
venv\Scripts\activate
```

Linux:
```bash
source .venv/bin/activate
```

To install all requirements for local development, run the following command:

```bash
pip install -r requirements/local.txt
```

To deactivate the virtual environment you just need to run the following commands:

```bash
deactivate
```


## 4. Run Server

If you want to run the app locally, run the following command:

```bash
python manage.py runserver
```

You can see the application in a browser, at [http://localhost:8000](http://localhost:8000).
