# Create a new Flask app project for your coursework

## Create coursework repository

Create a repository using the appropriate GitHub classroom assignment:

[Group](https://classroom.github.com/a/VkwVuaik) - choose the group name (this should already be available as you created it for coursework 1).

[Individual](https://classroom.github.com/a/39daJxVs)

You will need to add your data set to the new repository. Only one person needs to do this for a group. Make sure you 'add' the files, 'commit' them and 'push' them back to GitHub so your teammates can 'pull' the changes to their local development environments.

You will need to access information from COMP0035 though you don't have to put this in the repository. Useful files include: target audience, wireframes, application design, database design. You should also consider creating a setup.py and a folder for tests (as per COMP0035 coursework 2).

## Create a new project with a basic Flask app

In PyCharm Professional (not available in the community edition), when you select the menu option File > New project there is an option to create a new Flask project and this will install Flask and any dependencies and create the basic folder structure and app.py.
The [PyCharm documentation is here](https://www.jetbrains.com/help/pycharm/creating-flask-project.html).

In VS Code follow the [instructions here](https://code.visualstudio.com/docs/python/tutorial-flask) to create a new project, create a venv and install Flask.

For other IDEs follow the [installation instructions](https://flask.palletsprojects.com/en/2.0.x/installation/) in the Flask documentation. You will then need to create the following two subdirectories in your Flask project
directory: `/static` and `/templates`.

## Create a requirements.txt

If you are using another method to manage dependencies then you can continue to use that instead; otherwise completed this activity to create a requirements.txt file.

Open the Terminal in PyCharm or VS Code. Make sure your venv is activated.

Enter `pip freeze > requirements.txt`

This will generate a requirements.txt file with the package dependencies for the project. Note: if you add more
dependency packages to your project you will need to either add these to requirements.txt or run the command again and
replace the existing file.

## Add a .gitignore file

If you are using PyCharm and have installed and enabled the .ignore plug in then you should be able to
select `File | New | .ignore file | .gitignore`. If you search for 'python' you should find and select the JetBrains and the Python templates and create the .ignore.

If you are using VSCode you may want to install [this extension](https://marketplace.visualstudio.com/items?itemName=codezombiech.gitignore) which allows you to create a .gitignore file by choosing templates for Python.

Alternatively you can copy a `.gitignore` from one of your earlier projects into this project directory.

## Create a new python package for the app

In PyCharm use the File | New | Package menu option. Give it an appropriate name that has meaning for your app. Use all lowercase and avoid spaces.

In VS Code create a New Folder in the Explorer pane. Again give it an appropriate name that has meaning for your app. Use all lowercase and avoid spaces. The inside the folder you just created, create a New File called `__init__.py`. Pycharm creates `__init__.py` when you select the Python Package option for the new file so PyCharm users don't need to create this file.

## Move the `static` and `templates` folders and app.py into the python package you just created

If you created a new Flask project in PyCharm then you should use refactoring to move the `static` and `templates` folders into your app folders. In PyCharm you can use Refactor | Move (though dragging to another folder within PyCharm refactors by default).

In VS Code you will need to create the two folders inside the app folder you created. Make sure you name them correctly and use all lowercase.

## Create setup.py and MANIFEST.in

Read [Making the project installable](https://flask.palletsprojects.com/en/2.2.x/tutorial/install/#make-the-project-installable) and then create a `setup.py` for your project. You may also wish to create a `MANIFEST.in` as described in the documentation.

The setup.py file describes your project and the files that belong to it. It might look like this (replace `my_app` with the name of your app):

```python
# setup.py

from setuptools import find_packages, setup

setup(
    name='my_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-sqlalechemy',
    ],
)
```

The `install_requires` lists packages that are required, you may think this is the same as `requirements.txt` however their uses are slightly different and you should read the [documentation](https://packaging.python.org/discussions/install-requires-vs-requirements/).

To include other files, such as the static and templates directories, `include_package_data` is set. Python needs another file named [`MANIFEST.in`](https://docs.python.org/2/distutils/sourcedist.html#the-manifest-in-template) to tell what this other data is. It might look like this:

```text
# MANIFEST.in

graft my_app/static
graft my_app/templates
global-exclude *.pyc
```

## Check your structure

You should now have something like this:

```
/projectname
    /my_app_name
        __init__.py
        app.py
        /static
            ... css will go here
        /templates
            ... html files will go here
    /venv
    .gitignore
    README.md
    setup.py
    MANIFEST.in
    requirements.txt
```

## Create a basic Flask app

If you are using PyCharm Professional and used the 'New Flask Project' method then you will already have a file called `app.py`. Use the menu option File | Refactor and move it to the `/my_fist_app` package.

If you are using any other IDE then in the `/my_first_app` directory create a file called `app.py` with the following code:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
```

Run the Flask app and check that it launches.

See [Flask structure recommendations](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/) for more guidance.

## Other actions

Other steps you could consider for configuring the Flask app include:

1. Creating the app using the [application factory pattern](https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/#application-factories). This is also explained in this week's coding activities.
2. [Config handling](https://flask.palletsprojects.com/en/2.2.x/config/#configuration-handling) to allow Flask to be run in different enviornments such as dev, test and production. Options include config from file, config from class or config from environment variables.
3. Use [Blueprints](https://flask.palletsprojects.com/en/2.2.x/blueprints/#modular-applications-with-blueprints).
