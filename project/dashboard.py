from flask import Blueprint, render_template, redirect, request
from . import db
from flask_login import login_required, current_user
from .models import Users, Topics
import csv
import os
from googleapiclient.discovery import build


dashboard = Blueprint('dashboard', __name__)

api_key = 'AIzaSyC0qvJDC0eOFTL7j368bmU2KaoUBaV1saY'

youtube = build('youtube', 'v3', developerKey=api_key)

def yt_search(topic):
    ##searching for playlists
    request_playlists = youtube.search().list(
            part="snippet",
            maxResults=25,
            q=topic,
            type="playlist",
    )
    response_playlists = request_playlists.execute()

    playlist_ids = []

    items_playlists = response_playlists['items']
    for i in items_playlists:
        playlist_ids.append(i['id']['playlistId'])


    #getting 1st video of playlist:
    video_ids = []
    for pid in playlist_ids:

        request_video = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=pid
        )

        respone_video = request_video.execute()

        items_videos = respone_video['items']

        request_sp_video = youtube.videos().list(
            part="snippet",
            id=items_videos[0]['contentDetails']['videoId']
        )

        response_sp_video = request_sp_video.execute()

        video_ids.append((items_videos[0]['contentDetails']['videoId'], response_sp_video['items'][0]['snippet']['title']))
    print(video_ids)
    return(video_ids)

@dashboard.route('/personalise')
@login_required
def personalise():
    math_topics = Topics.query.filter_by(subject='Math').all()
    return render_template('topic_questions.html', math_topics=math_topics)

@dashboard.route('/personalise', methods=['POST'])
def personalise_post():
    raw_data = []
    math_topics = Topics.query.filter_by(subject='Math').all()

    for i in range(len(math_topics)):
        r = int(request.form.get("math_1"))
        score = math_topics[i].importance + r
        item = {'id': math_topics[i].id, 'topic': math_topics[i].name, 'imp': math_topics[i].importance, 'diff': r, 'prereq':  math_topics[i].prerequisites, 'score': score}
        raw_data.append(item)

    
    #sorting the data based on score
    sorted_data = raw_data[:]

    n = len(sorted_data)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if sorted_data[j]['score'] < sorted_data[j + 1]['score']:
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]

    #function for getting index in list of a given id
    def index(l, id):
        for i in range(len(l)):
            if l[i]['id'] == id:
                return i
        
        return None

    #going through pre requisites to ensure it's above that particular topic
    p_data = sorted_data[:]

    flag = True
    while flag:
        flag = False
        for i in range(len(p_data)):
            prereqs = [x.strip() for x in p_data[i]['prereq'].split(',')]
            if prereqs[0] != 'NULL':
                #going through each prerequisite
                for p in prereqs:
                    index_prereq = index(p_data, int(p)) 
                    if index_prereq > i: #if index of prerequisite is greater than the index of the topic shift it to just before the topic
                        nd = p_data[:i] + [p_data[index_prereq]] + p_data[i:index_prereq] + p_data[index_prereq + 1:]
                        p_data = nd
                        flag = True

    order = []

    for i in p_data:
        order.append(i['id'])

    current_user.order = str(order)
    db.session.commit()

    return redirect('/dashboard')


@dashboard.route('/dashboard', methods=['GET'])
def dashboard_show():
    co = current_user.order[1:-1]
    topics_order =[x.strip() for x in co.split(',')]
    my_topics = []

    for i in topics_order:
        print(i)
        c_topic = Topics.query.filter_by(id=i).first()
        my_topics.append(c_topic)


    print(my_topics)
    return render_template('dashboard.html', topics=my_topics)


@dashboard.route('/search_videos', methods=['POST'])
def videos():
    topic_search = request.form.get('topic_name') + ' math ' + ' jee '
    vid_ids = yt_search(topic_search)

    return render_template('video_lists.html', vid_ids=vid_ids)


@dashboard.route('/watch_video', methods=['POST'])
def watch_video():
    video_id = request.form.get('video_id')
    current_user.last_watched = video_id
    return render_template("watch_video.html", video_id=video_id)



#HOUSEKEEPING - IGNORE
basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'static/topics_dummy.csv')

@dashboard.route('/add_data')
def dddddndnsd():
    with open(data_file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            new_topic = Topics(name=row[1], subject='Math', importance=int(row[2]), goal='JEE', grade=12, prerequisites=row[4])
            print(new_topic)
            db.session.add(new_topic)
            db.session.commit()    

    return "done"

    