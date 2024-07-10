<<<<<<< HEAD
# KnowledgeHub

KnowledgeHub is an innovative and interactive platform designed to facilitate knowledge sharing through articles, comments, and user interactions. It aims to create a vibrant community where users can learn from each other by sharing insights, experiences, and expertise. The platform empowers users to create and share articles on various topics, engage in meaningful discussions through comments, and follow their favorite authors to stay updated with their latest posts.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Team Members](#team-members)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

### Problem Statement
In today's information-rich world, individuals often struggle to find reliable and insightful content on specific topics. Traditional blogs and information-sharing platforms lack the interactive elements that foster community and engagement. There is a need for a platform that not only provides high-quality content but also encourages user participation and collaboration.

### Solution
KnowledgeHub addresses these challenges by offering a user-friendly platform where individuals can:
- Create and share articles.
- Engage through comments.
- Follow authors and receive notifications about new articles.

## Features

### MVP (Minimum Viable Product)
- User authentication: sign-up and login.
- Article management: create, view, update, delete articles.
- Comment system: add, view, delete comments on articles.
- User following: follow/unfollow other users, view a list of followed users.

### Stretch Features
- Notifications: receive notifications via Email/SMS when followed users post new articles.
- Likes: like articles and comments.
- Search: search articles by title or content.
- Filter: filter articles by categories or tags.
- Profile management: update profile information.

## Technology Stack

### Frontend
- React
- React Router
- Formik for forms and validation
- CSS for styling

### Backend
- Flask
- SQLAlchemy for ORM
- RESTful API

### Database
- PostgreSQL

### Notifications
- Email and SMS integration

### Deployment
- Render or Heroku

## Installation

### Prerequisites
- Node.js and npm
- Python 3.x
- PostgreSQL

### Backend Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/knowledgehub.git
    cd knowledgehub
    ```

2. Set up a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the backend dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database:
    ```sh
    psql
    CREATE DATABASE knowledgehub;
    ```

5. Run the Flask application:
    ```sh
    export FLASK_APP=run.py
    flask db init
    flask db migrate
    flask db upgrade
    flask run
    ```

### Frontend Setup
1. Navigate to the `client` directory:
    ```sh
    cd client
    ```

2. Install the frontend dependencies:
    ```sh
    npm install
    ```

3. Start the React development server:
    ```sh
    npm start
    ```

## Usage

1. Start the backend server:
    ```sh
    flask run
    ```

2. Start the frontend development server:
    ```sh
    npm start
    ```

3. Open your browser and navigate to `http://localhost:3000`.

## API Endpoints

### User Endpoints
- `GET /users/<user_id>`: Get user details.
- `POST /users`: Create a new user.
- `PUT /users/<user_id>`: Update user details.
- `DELETE /users/<user_id>`: Delete a user.

### Article Endpoints
- `GET /articles`: Get all articles.
- `GET /articles/<article_id>`: Get a specific article.
- `POST /articles`: Create a new article.
- `PUT /articles/<article_id>`: Update an article.
- `DELETE /articles/<article_id>`: Delete an article.

### Comment Endpoints
- `GET /comments`: Get all comments.
- `GET /comments/<comment_id>`: Get a specific comment.
- `POST /comments`: Create a new comment.
- `PUT /comments/<comment_id>`: Update a comment.
- `DELETE /comments/<comment_id>`: Delete a comment.

## Team Members
- Nicole Apono
- Dennis Githaiga
- Joy Simiyu
- Tony Brian
- John-Alexander Kamau

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License.

=======
<<<<<<< HEAD
# KnowlegbeHub
=======
# Phase 4 Full-Stack Application Project Template

## Learning Goals

- Discuss the basic directory structure of a full-stack Flask/React application.
- Carry out the first steps in creating your Phase 4 project.

---

## Introduction

Fork and clone this lesson for a template for your full-stack application. Take
a look at the directory structure before we begin (NOTE: node_modules will be
generated in a subsequent step):

```console
$ tree -L 2
$ # the -L argument limits the depth at which we look into the directory structure
.
├── CONTRIBUTING.md
├── LICENSE.md
├── Pipfile
├── README.md
├── client
│   ├── README.md
│   ├── package.json
│   ├── public
│   └── src
└── server
    ├── app.py
    ├── config.py
    ├── models.py
    └── seed.py
```

A `migrations` folder will be added to the `server` directory in a later step.

The `client` folder contains a basic React application, while the `server`
folder contains a basic Flask application. You will adapt both folders to
implement the code for your project .

NOTE: If you did not previously install `tree` in your environment setup, MacOS
users can install this with the command `brew install tree`. WSL and Linux users
can run `sudo apt-get install tree` to download it as well.

## Where Do I Start?

Just as with your Phase 3 Project, this will likely be one of the biggest
projects you've undertaken so far. Your first task should be creating a Git
repository to keep track of your work and roll back any undesired changes.

### Removing Existing Git Configuration

If you're using this template, start off by removing the existing metadata for
Github and Canvas. Run the following command to carry this out:

```console
$ rm -rf .git .canvas
```

The `rm` command removes files from your computer's memory. The `-r` flag tells
the console to remove _recursively_, which allows the command to remove
directories and the files within them. `-f` removes them permanently.

`.git` contains this directory's configuration to track changes and push to
Github (you want to track and push _your own_ changes instead), and `.canvas`
contains the metadata to create a Canvas page from your Git repo. You don't have
the permissions to edit our Canvas course, so it's not worth keeping around.

### Creating Your Own Git Repo

First things first- rename this directory! Once you have an idea for a name,
move one level up with `cd ..` and run
`mv python-p4-project-template <new-directory-name>` to change its name (replace
<new-directory-name> with an appropriate project directory name).

> **Note: If you typed the `mv` command in a terminal within VS Code, you should
> close VS Code then reopen it.**

> **Note: `mv` actually stands for "move", but your computer interprets this
> rename as a move from a directory with the old name to a directory with a new
> name.**

`cd` back into your new directory and run `git init` to create a local git
repository. Add all of your local files to version control with `git add --all`,
then commit them with `git commit -m'initial commit'`. (You can change the
message here- this one is just a common choice.)

Navigate to [GitHub](https://github.com). In the upper-right corner of the page,
click on the "+" dropdown menu, then select "New repository". Enter the name of
your local repo, choose whether you would like it to be public or private, make
sure "Initialize this repository with a README" is unchecked (you already have
one), then click "Create repository".

Head back to the command line and enter
`git remote add origin git@github.com:github-username/new-repository-name.git`.
NOTE: Replace `github-username` with your github username, and
`new-repository-name` with the name of your new repository. This command will
map the remote repository to your local repository. Finally, push your first
commit with `git push -u origin main`.

Your project is now version-controlled locally and online. This will allow you
to create different versions of your project and pick up your work on a
different machine if the need arises.

---

## Setup

### `server/`

The `server/` directory contains all of your backend code.

`app.py` is your Flask application. You'll want to use Flask to build a simple
API backend like we have in previous modules. You should use Flask-RESTful for
your routes. You should be familiar with `models.py` and `seed.py` by now, but
remember that you will need to use Flask-SQLAlchemy, Flask-Migrate, and
SQLAlchemy-Serializer instead of SQLAlchemy and Alembic in your models.

The project contains a default `Pipfile` with some basic dependencies. You may
adapt the `Pipfile` if there are additional dependencies you want to add for
your project.

To download the dependencies for the backend server, run:

```console
pipenv install
pipenv shell
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

Check that your server serves the default route `http://localhost:5555`. You
should see a web page with the heading "Project Server".

### `client/`

The `client/` directory contains all of your frontend code. The file
`package.json` has been configured with common React application dependencies,
include `react-router-dom`. The file also sets the `proxy` field to forward
requests to `"http://localhost:5555". Feel free to change this to another port-
just remember to configure your Flask app to use another port as well!

To download the dependencies for the frontend client, run:

```console
npm install --prefix client
```

You can run your React app on [`localhost:3000`](http://localhost:3000) by
running:

```sh
npm start --prefix client
```

Check that your the React client displays a default page
`http://localhost:3000`. You should see a web page with the heading "Project
Client".

## Generating Your Database

NOTE: The initial project directory structure does not contain the `instance` or
`migrations` folders. Change into the `server` directory:

```console
cd server
```

Then enter the commands to create the `instance` and `migrations` folders and
the database `app.db` file:

```
flask db init
flask db upgrade head
```

Type `tree -L 2` within the `server` folder to confirm the new directory
structure:

```console
.
├── app.py
├── config.py
├── instance
│   └── app.db
├── migrations
│   ├── README
│   ├── __pycache__
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── models.py
└── seed.py
```

Edit `models.py` and start creating your models. Import your models as needed in
other modules, i.e. `from models import ...`.

Remember to regularly run
`flask db revision --autogenerate -m'<descriptive message>'`, replacing
`<descriptive message>` with an appropriate message, and `flask db upgrade head`
to track your modifications to the database and create checkpoints in case you
ever need to roll those modifications back.

> **Tip: It's always a good idea to start with an empty revision! This allows
> you to roll all the way back while still holding onto your database. You can
> create this empty revision with `flask db revision -m'Create DB'`.**

If you want to seed your database, now would be a great time to write out your
`seed.py` script and run it to generate some test data. Faker has been included
in the Pipfile if you'd like to use that library.

---

#### `config.py`

When developing a large Python application, you might run into a common issue:
_circular imports_. A circular import occurs when two modules import from one
another, such as `app.py` and `models.py`. When you create a circular import and
attempt to run your app, you'll see the following error:

```console
ImportError: cannot import name
```

If you're going to need an object in multiple modules like `app` or `db`,
creating a _third_ module to instantiate these objects can save you a great deal
of circular grief. Here's a good start to a Flask config file (you may need more
if you intend to include features like authentication and passwords):

```py
# Standard library imports

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Local imports

# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)

```

Now let's review that last line...

#### CORS

CORS (Cross-Origin Resource Sharing) is a system that uses HTTP headers to
determine whether resources from different servers-of-origin can be accessed. If
you're using the fetch API to connect your frontend to your Flask backend, you
need to configure CORS on your Flask application instance. Lucky for us, that
only takes one line:

```py
CORS(app)

```

By default, Flask-CORS enables CORS on all routes in your application with all
fetching servers. You can also specify the resources that allow CORS. The
following specifies that routes beginning with `api/` allow CORS from any
originating server:

```py
CORS(app, resources={r"/api/*": {"origins": "*"}})

```

You can also set this up resource-by-resource by importing and using the
`@cross_origin` decorator:

```py
@app.route("/")
@cross_origin()
def howdy():
  return "Howdy partner!"

```

---

## Updating Your README.md

`README.md` is a Markdown file that describes your project. These files can be
used in many different ways- you may have noticed that we use them to generate
entire Canvas lessons- but they're most commonly used as homepages for online
Git repositories. **When you develop something that you want other people to
use, you need to have a README.**

Markdown is not a language that we cover in Flatiron's Software Engineering
curriculum, but it's not a particularly difficult language to learn (if you've
ever left a comment on Reddit, you might already know the basics). Refer to the
cheat sheet in this lesson's resources for a basic guide to Markdown.

### What Goes into a README?

This README should serve as a template for your own- go through the important
files in your project and describe what they do. Each file that you edit (you
can ignore your migration files) should get at least a paragraph. Each function
should get a small blurb.

You should descibe your application first, and with a good level of detail. The
rest should be ordered by importance to the user. (Probably routes next, then
models.)

Screenshots and links to resources that you used throughout are also useful to
users and collaborators, but a little more syntactically complicated. Only add
these in if you're feeling comfortable with Markdown.

---

## Conclusion

A lot of work goes into a full-stack application, but it all relies on concepts
that you've practiced thoroughly throughout this phase. Hopefully this template
and guide will get you off to a good start with your Phase 4 Project.

Happy coding!

---

## Resources

- [Setting up a respository - Atlassian](https://www.atlassian.com/git/tutorials/setting-up-a-repository)
- [Create a repo- GitHub Docs](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
- [Python Circular Imports - StackAbuse](https://stackabuse.com/python-circular-imports/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
>>>>>>> master
>>>>>>> 6fa0ac67801c587893554e1d464e7cde6c19e590
# Prac
