---
layout: post
title: serverless app
date: 2020-11-26 15:10 +0100
tags: [AWS, lambda, serverless, corona]
---

As everybody who is a researcher have to have voice opinion, no mather ones expertise, I
am going to get in to the corona game (albeit a bit late). I wanted to have a reason to
develope a serverless app using aws lambda so I chose this. I want to
write an app that:
1. Triggers approximately when new data is uploaded (14:00 CET)
2. Downloads the data to a private s3 bucket
3. Reads and plots the data
4. Saves the plot to a public s3 bucket for display on my website

I decided on using the chalice framework and continuos deployment in AWS.  I am basing
this project on what I learned from
[this](https://www.linkedin.com/learning/deploying-rest-services-with-chalice-for-aws/)
 EXCELLENT chalice course on linkedin learning by Lawrence Ogrodnek. It is mainly focused on
 RESTapis, but there are enough hints about how to do what I want to do to get me started.
 This project requires aws setup and the aws-cli, git and anaconda installed.

1st I created a new folder for the project and setup new environment in conda with chalice and boto3.

```bash
conda create -n fhm python=3.7
```
using 3.8 created errors during the deployment face. I said yes when prompted and continued with:

```bash
conda activate fhm
pip install chalice
pip install boto3
```

In our folder we initialize and move into our new project

```bash
 chalice new-project fhm-plot-data
 cd fhm_plot_data
```
I used _ insteead of - first and this was not liked by code deploy.
# Continuos deployment
This section deals with setting up continuos deployment, it is not necessary to make the app deploy and run. I want to try continuos integration using AWS services:

```bash
 chalice generate-pipeline --pipeline-version v2 buildspec.yml pipeline.json  
 aws cloudformation deploy --stack-name fhm-pipeline --template-file pipeline.json --capabilities CAPABILITY_IAM
 git init
```
I got a lot of errors and I think the code above should give you what I ended upp doing. (I ran
multiple versions of chalice generate until I had something that let met trough the build without error)

added the following to .gitignore:

```
*.pyc
__pycashe__/
```
and committed
```bash
git add -A .
git commit -m "first commit"
```
And added the following to the end of the .git/config file:

```
[credential]
	helper = 
	helper = !aws codecommit credential-helper $@
	UseHttpPath = true
```
I copied the url from aws code commit

and ran:
```bash
git remote add origin https://git-codecommit.eu-north-1.amazonaws.com/v1/repos/fhm-plot-data
git push origin master
```

And after trying multiple versions of the pipeline.yml for a couple of hours it worked!


# Setting up the download
The file we want to get is returned as a RESTapi GET, so we we need to the requests package which is
not installed by default in the python version run by lambda. I added "requests" to
"requirements.txt" and ran 
```python
pip install -r requirements.txt.
```
I changed app.py to:
```python
from chalice import Chalice, Cron
import requests
import boto3

app = Chalice(app_name='fhm_plot_data')

@app.schedule(Cron(14, 13, '?', '*', 'MON-FRI', '*'))
def get_fhm_data(event):
    bucket_name = 'folkhalso'
    folkfilename = 'FHM.xlsx'
    url = 'https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data'

    file_content = get_file_content_from_url(url)

    s3 = boto3.resource('s3')

    s3.Bucket(bucket_name).put_object(Key=folkfilename, Body=file_content)

def get_file_content_from_url(url):
    response = requests.get(url)
    return response.content
```

chalice is supposed to give access to resources automatically but did not do so for the s3 bucket,
so I wrote a custom policy policy-dev.json and placed it in the .chalice folder. This policy gives
read write access to the s3 bucket and ability to write logs


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::folkhalso/*"
        },
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:*:logs:*:*:*",
            "Effect": "Allow"
        }
    ]
}
```


# Adding plotting
To be able to read the file and plot I plan to use pandas and matplotlib. This is one of the reasons
I went with chalice in the first place. Implementing the first function in AWS and bundling it with
with the request manually was quite straight forward. Doing the same with pandas and matplotlib,
which both are dependent on numpy, was not as easy. One can make custom machine images but I wanted
to try this first. In chalice we can simply add the things we need to the requirements.txt, so I 
updated it to:
```
requests
pandas
matplotlib
xlrd
```
To install the requirements during the build I updated  buildspec.yml to:
```yml
artifacts:
  files:
  - transformed.yaml
  type: zip
phases:
  install:
    commands:
    - pip install --upgrade awscli
    - aws --version
    - pip install 'chalice>=1.21.0,<1.22.0'
    - pip install -r requirements.txt
    - pip install pytest
  build:
    commands:
    - pytest -v
  post_build:
    commands:
    - chalice package /tmp/packaged
    - aws cloudformation package --template-file /tmp/packaged/sam.json --s3-bucket ${APP_S3_BUCKET}--output-template-file transformed.yaml
version: '0.1'
```
I am running a couple of unit tests and plan to add more to the function, so they are
run during the build face.

I added the plotting to the app.py file (and call it from the get_fhm_data).

```python
from chalice import Chalice, Cron
import requests
import boto3
import io
import pandas as pd
import matplotlib.pyplot as plt

app = Chalice(app_name='fhm_plot_data')

@app.schedule(Cron(14, 13, '?', '*', 'MON-FRI', '*'))
def get_fhm_data(event):
    bucket_name = 'folkhalso'
    folkfilename = 'FHM.xlsx'
    url = 'https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data'

    file_content = get_file_content_from_url(url)

    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=folkfilename, Body=file_content)

    update_corona_plot()


def get_file_content_from_url(url):
    response = requests.get(url)
    return response.content


def buffer_from_from_bucket(bucket_name, filename):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, filename)
    return obj.get()['Body'].read()


def read_tab_excell_from_bucket(bucket_name, filename, tabname):
    buffer = buffer_from_from_bucket(bucket_name, filename)
    tab = pd.read_excel(buffer, sheet_name=tabname)
    return tab


def get_date_and_numbers(tab):
    datename, n_name = tab.columns
    dates = tab[datename]
    n = tab[n_name].astype(int).values
    if dates.values[-1] == 'Uppgift saknas':
        dates = dates.values[:-1]
        n = n[:-1]
    return pd.to_datetime(dates).values, n


def corona_plot(plot_dicts):
    fig, ax = plt.subplots()
    for plot_dict in plot_dicts:
        label = plot_dict['name']
        x = plot_dict['x']
        y = plot_dict['y']
        ax.scatter(x, y, label=label)
    ax.set_xlabel('datum')
    ax.set_ylabel('antal')
    ax.legend()
    fig.autofmt_xdate()
    return fig


def update_corona_plot():
    bucket_name = 'folkhalso'
    folkfilename = 'FHM.xlsx'
    tabnames = ['Antal avlidna per dag', 'Antal intensivvårdade per dag']
    plot_dicts = []
    for tabname in tabnames:
        tab = read_tab_excell_from_bucket(bucket_name, folkfilename, tabname)
        dates, n = get_date_and_numbers(tab)
        shortened_tabname = tabname.split()[1]
        plot_dict = {'name': shortened_tabname, 'x': dates, 'y': n}
        plot_dicts.append(plot_dict)
    fig = corona_plot(plot_dicts)

    file_content = io.BytesIO()
    fig.savefig(file_content, format='png')

    file_content.seek(0)
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key='coronaplot.png', Body=file_content)
```

After committing and waiting for the code to build I tested it in aws lambda and it works. To make
the resulting plot publicly available I went into the s3 bucket and updated the policy to:

```python
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::folkhalso/coronaplot.png"
        }
    ]
}
```
There is now public access to the image of the plot and we can display it here:
![corona graph](https://folkhalso.s3.eu-north-1.amazonaws.com/coronaplot.png)

continues with
[serverless app 2]({{ site.baseurl }}{% link _posts/2020-11-27-serverless-app-2.md %})

<iframe src="https://open.spotify.com/embed/track/3OcBH9Vzd1UwJkQd3r1dVG" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
/Jonas