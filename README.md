# project Bing / Diffbot (UpWork ID: 16568896)

## Installation

Unzip the ZIP file.

## Configuration

Edit the file `settings.ini`. It should contains the following information:
```ini

[bing]
api_key = my-bing-api-key
results_limit = 50
market = en-US
# latitude = 47.603450
# longitude = -122.329696

[diffbot]
token = my-diffbot-token

```

## How to use

### Usage

```


```
### Bing API

```shell
./bing_api -i bing-input.csv -o bing-output.csv
```
> OUTPUT
```
 37%|███████████████████████████████████████▌                                                                   | 37/100 [05:14<06:58,  1.64s/it]
```

### Diffbot API

#### Start a new job

```shell
./diffbot_api -i diffbot-input.csv -o diffbot-output.csv
```
> OUTPUT
```
 37%|███████████████████████████████████████▌                                                                   | 37/100 [05:14<06:58,  6.64s/it]
```

#### Resume a job

```shell
./diffbot_api -r 610a4b673c2747c7aa6377636018b7 -o diffbot-output.csv
```
> OUTPUT
```
Resuming bulk job with ID 610a4b673c2747c7aa6377636018b7.
 37%|███████████████████████████████████████▌                                                                   | 37/100 [05:14<06:58,  6.64s/it]
```


#### Download data from a job

```shell
./diffbot_api -d 67aa6e059b2b4f53a04287d221b92e -o diffbot-output.csv
```
> OUTPUT
```
Downloading data from bulk job with ID 67aa6e059b2b4f53a04287d221b92e.
Getting result data...
Result data downloaded.
Writing output file...
File written.
```

#### Get the status of a job
```shell
./diffbot_api -s 67aa6e059b2b4f53a04287d221b92e
```
> OUTPUT
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
