---
layout: post
title: serverless app 2
date: 2020-11-27 10:10 +0100
tags: [AWS, lambda, serverless, corona]
---
Continued from [serverless app]({{ site.baseurl }}{% link _posts/2020-11-26-serverless-app.md %})

Another interesting source of for following corona in sweden is the number of dead this yes
from all causes compared to the number of dead previous years. This data is published every
monday. My plan is to expand our app into several independent lambda functions. I want to
add one that downloads the all causes death data on mondays and separate the plotting function
to a separate lambda function. A lambda function can be triggered by a put event in an s3 bucket,
but this does not work when using continuos deployment. Therefore I switched to doing deployment
using chalice deploy. This is nice as we can separate the functions doing the downloading and plotting as we will now have two separate download functions which should trigger the same plotting
function. The not so nice thing is that all the work I did on getting continuos integration to work
is for naught.

Another nice thing I found is that chalice can create a layer of the packages we use instead of
including them in the lambda function. This makes the the lambda functions very much leaner taking
up much less space. This is done by adding the following to the config.json:

```json
  "automatic_layer": true
```

I added the get_scb_function added the s3 trigger to the update corona plot function and
refactored out some reused code as functions. (this is only part of the code)
```python
@app.schedule(Cron(14, 13, '?', '*', 'MON-FRI', '*'))
def get_fhm_data(event):
    bucket_name = 'folkhalso'
    filename = 'FHM.xlsx'
    url = 'https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data'

    get_data_from_url(url, bucket_name, filename)


@app.schedule(Cron(10, 10, '?', '*', 'MON', '*'))
def get_scb_data(event):
    bucket_name = 'folkhalso'
    filename = 'SCB.xlsx'
    url = 'https://www.scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/tabell-och-diagram/preliminar-statistik-over-doda/'

    get_data_from_url(url, bucket_name, filename)
    

@app.on_s3_event(bucket='folkhalso', events=['s3:ObjectCreated:*'], suffix='.xlsx')
def update_corona_plot(event):
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
    image_filaname = 'coronaplot.png'
    save_file_to_bucket(image_filaname, bucket_name, file_content)


def save_file_to_bucket(filename, bucket_name, file_content):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=filename, Body=file_content)


def get_data_from_url(url, bucket_name, filename):
    file_content = get_file_content_from_url(url)
    save_file_to_bucket(filename, bucket_name, file_content)
```

The next step is adding the excess mortality data to the plot. My plan for this is a bit involved
and I will do a separate post on that. Now the application looks like this:


![app](/images/fhm/app1.png)
    


/Jonas