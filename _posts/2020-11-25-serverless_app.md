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

I decided on using the chalice framework and continuos deployment in AWS. 1st I created a new
folder for the project and setup new environment in conda with chalice and boto3.

conda create -n fhm

I accepted the location and then ran:

conda activate fhm
pip install chalice
pip install boto3
