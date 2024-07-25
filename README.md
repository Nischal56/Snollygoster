# Student Study Planner
The biggest platform in the world, especially in rural areas, used for the purpose of learning (recreational or not) is YouTube. Unfortunately YouTube is not built for education and EdTech platforms such as Unacademy and Byjus may not be financially feasible for everyone. Our project optimises YouTube for education and gives a personalised roadmap for the student while removing any distraction that YouTube can entice students with.

## Installation
- Python 3 needs to be installed

Use the following commands :
```
git clone https://github.com/nischalkashyap56/Study-Planner-App.git
pip install flask, flask_sqlalchemy, flask_login
run create_db.py
export FLASK_APP='project'
flask run
```
- In another terminal open project_calendar
```
python calendarapp.py
```

## Functionalities 

```
1. Provides integration of YouTube videos into the web app
2. Utilises secure authentication using Google OAuth
3. Uses Google Calendar API to autmatically schedule study sessions on Google Calendar
4. Notifications of study sessions with relevant link sent through Google Calendar API
5. Accurate algorithm to optimise and personalise the planning process to each individual student
```

## Technologies Used
```
1. Flask
2. SQLAlchemy
3. Google Calendar API
4. Youtube API
```
