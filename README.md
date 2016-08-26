# project Bing / Diffbot (UpWork ID: 16568896)

## Installation

Unzip the ZIP file.

## Configuration

Edit the file `settings.ini`.

## How to use

### Bing API

```shell
./bing_api -i bing-input.csv -o bing-output.csv
```

```
 37%|███████████████████████████████████████▌                                                                   | 37/100 [05:14<06:58,  1.64s/it]
```

### Diffbot API

#### Start a new job

```shell
./diffbot_api -i diffbot-input.csv -o diffbot-output.csv
```

```
Starting bulk job with ID dc1a6178d9b540a59124d54f6d57d5.
 37%|███████████████████████████████████████▌                                                                   | 37/100 [05:14<06:58,  6.64s/it]
```

#### Resume a job

```shell
./diffbot_api -r 610a4b673c2747c7aa6377636018b7 -o diffbot-output.csv
```

```
Resuming bulk job with ID 610a4b673c2747c7aa6377636018b7.
 37%|███████████████████████████████████████▌                                                                   | 37/100 [05:14<06:58,  6.64s/it]
```


#### Download data regardless of the status of the job.


```shell
./diffbot_api -r 67aa6e059b2b4f53a04287d221b92e -f -o diffbot-output.csv
```

```
Resuming bulk job with ID 83f3c757915545c09e845573e30690.
Force flag set, do not wait for job's completion.
Downloading result data...
Converting data to CSV...
Writing output file to output.csv...
Done!
```

#### Get the status of a job
```shell
./diffbot_api -s 67aa6e059b2b4f53a04287d221b92e
```

```
Getting status of job with ID 83f3c757915545c09e845573e30690.

        ID: 83f3c757915545c09e845573e30690
        Current Status: Job has completed and no repeat is scheduled.
        Job Started: 2016-08-20 02:16:58
        Job Completed: 2016-08-20 02:17:36
        Pages Attempted: 6
        Pages Processed: 6
        Email Notification: 
```


## Troubleshooting

Both programs write logs resp. in `bing-api.log` and `diffbot-api.log`
