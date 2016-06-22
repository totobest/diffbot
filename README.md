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

```shell
./diffbot_api -i diffbot-input.csv -o diffbot-output.csv
```
> OUTPUT
```
 37%|███████████████████████████████████████▌                                                                   | 37/100 [05:14<06:58,  6.64s/it]
```


## Troubleshooting

Both programs write logs resp. in `bing-api.log` and `diffbot-api.log`
