import requests
import datetime
import json
import pandas as pd
import plotly
import plotly.graph_objs as go

s1_orig = "Jetex Industries, 01, Malwa Building"
s1_dest = "Hank Impex Pvt Ltd - Shah Trading Company, Kurla Industrial Estate Private Limited"

s2_orig = "Hank Impex Pvt Ltd - Shah Trading Company, Kurla Industrial Estate Private Limited"
s2_dest = "Bank of India HMPL Surya Nagar"

traffic_model = 'best_guess'
api_key = 'AIzaSyDsfA4MeDEOw80H2j1n59XWOQsx2ggiTGE'
url_main = 'https://maps.googleapis.com/maps/api/distancematrix/json'

dep_time_for_ts = '2018-03-04T00:00:00'
dep_time_1 = '2018-03-04T06:00:00'
dep_time_2 = '2018-03-04T18:00:00'

def time_to_epoch(time_string):
    pytime = datetime.datetime.strptime(time_string,"%Y-%m-%dT%H:%M:%S")
    pytime_local = pytime - datetime.timedelta(minutes=330)
    epoch = (pytime_local - datetime.datetime(1970,1,1)).total_seconds()
    return(int(epoch))

def epoch_to_time(epoch):
    t = datetime.datetime.fromtimestamp(float(epoch))
    fmt = "%H:%M:%S"
    return(t.strftime(fmt))

def construct_url(orig, dest, dep_time, api_key=api_key):
    url = url_main+'?origins={x}&destinations={y}&departure_time={z}&key={key}'.format(
    x=orig,
    y=dest,
    z=str(dep_time),
    key=api_key)
    return(url)

def construct_ts(orig, dest):
    ts_dict = dict()
    time_list = list()
    duration_list = list()
    for span in range(1,49):
        print(span)
        dep_time = time_to_epoch(dep_time_for_ts) + 1800 * span
        url = construct_url(orig, dest, dep_time)
        print(url)
        page = requests.get(url)
        data = json.loads(page.content)
        time_list.append(epoch_to_time(dep_time))
        duration_list.append(data["rows"][0]["elements"][0]["duration_in_traffic"]["value"])
    ts_dict["departure_time"]=time_list
    ts_dict["duration_in_traffic"]=duration_list
    return(ts_dict)

ts1 = construct_ts(s1_orig, s1_dest)
ts2 = construct_ts(s2_orig, s2_dest)

df1 = pd.DataFrame(ts1)
df2 = pd.DataFrame(ts2)

df1.index = df1.departure_time
df2.index = df2.departure_time

trace1 = go.Scatter(x=df1.index, y=df1.duration_in_traffic, name='Stretch1')
trace2 = go.Scatter(x=df2.index, y=df2.duration_in_traffic, name='Stretch2')

data = [trace1, trace2]

layout = go.Layout(
    title='Time Spent on Stretches (in Seconds)',
    yaxis=dict(
        title='Stretch1'
    ),
    xaxis=dict(
        title='Local Time on 4th March 2018'
    ),   
    yaxis2=dict(
        title='Stretch2',
        titlefont=dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        overlaying='y',
        side='right'
    )
)

plotly.offline.plot({
    "data":data,
    "layout":layout
    })






