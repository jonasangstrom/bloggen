---
layout: post
title: serverless app
date: 2020-11-25 14:44 +0100
tags: [AWS, lambda, serverless, corona]
---

As everybody who is a researcher have to have voice opinion, no mather ones expertise, I
am going to get in to the corona game (albeit a bit late). I wanted to have a reason to
develope a serverless app using aws lambda and I this could be a good project. I want to
write an app that:
1. Triggers approximately when new data is uploaded
2. Downloads the data to a private s3 bucket
3. Reads and plots the data
4. Saves the plot to a public s3 bucket for display on my website

I decided on using the chalice framework and continuos deployment in AWS.  I am basing
this project on what I learned from the EXCELLENT on
[this](https://www.linkedin.com/learning/deploying-rest-services-with-chalice-for-aws/)
chalice course on linkedin learning by Lawrence Ogrodnek. It is mainly focused on RESTapis,
but we there are enough hints about how to do what I want to do to get me started in, what I
hope is the right direction. This project requires that you have the aws setup and the aws-cli, git
and anaconda installed.

1st I created a new folder for the project and setup new environment in conda with chalice and boto3.

```bash
conda create -n fhm python=3.7
```
using 3.8 created errors during the deployment face

I accepted the location and then ran:

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
"requirements.txt".

I changed app.py to:

```python
from chalice import Chalice, Cron
import requests
import boto3

app = Chalice(app_name='fhm_plot_data')

@app.schedule(Cron(14, 14, '?', '*', 'MON-FRI', '*'))
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
to try this first.
