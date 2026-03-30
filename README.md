SocialNet - Full-Stack Social Platform
A modern, responsive social networking web application built with Python (Flask), SQLAlchemy, and Bootstrap. This project allows users to share posts, follow friends, and engage with content in real-time.

 Features
User Authentication: Secure Sign-up and Login using password hashing.
Dynamic Feed: A personalized home page with a three-column layout.
Username Search: Find posts from specific users instantly.
Engagement Tools: Real-time Like/Dislike functionality using AJAX (no page refresh).
Commenting System: Add and delete comments on any post.
Social Graph: Follow and Unfollow users with a dedicated "Followers List" view.
Profile Customization: Upload profile pictures and update your bio.
Media Support: Upload and display images within posts.

Tech Stack
Front-End:
  HTML5 / Jinja2 (Templating)
  Bootstrap 4 (Responsive UI/UX)
  JavaScript / AJAX 
  FontAwesome (Iconography)

Back-End:
  Python 3
  Flask (Web Framework)
  Flask-Login (Session Management)

Database & Storage:
  SQLite (Relational Database)
  SQLAlchemy (ORM)
  Werkzeug (Secure File Uploads)

pip install flask flask-sqlalchemy flask-login
Run the application:
  python main.py
  Access in Browser:
  Open http://127.0.0.1:5000/
  
