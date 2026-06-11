# CNN Fear & Greed Index for TradingView Pine Seeds

This repository is designed to maintain a daily-updated TradingView Pine Seeds dataset for the CNN Fear & Greed Index.

## Architecture

CNN Fear & Greed historical dataset  
→ GitHub Actions daily update  
→ TradingView Pine Seeds CSV format  
→ TradingView Pine Script using `request.seed()`

## Data Source

Primary source:

https://raw.githubusercontent.com/whit3rabbit/fear-greed-data/main/fear-greed.csv

The dataset starts from 2011-01-03 and is updated from CNN's live data source by the upstream project.

## TradingView Pine Seeds Symbol

Source name:

```text
seed_kings_fng
```

Symbol:

```text
CNN_FGI
```

## CSV Format

TradingView Pine Seeds requires OHLCV format:

```text
YYYYMMDDT,open,high,low,close,volume
```

Because the Fear & Greed Index is a single daily value, open/high/low/close are all set to the same value.

Example:

```text
20110103T,68.0,68.0,68.0,68.0,0
```

## Daily Update

GitHub Actions runs every weekday at 23:30 UTC.

You can also manually run it from:

```text
Actions → Update CNN Fear Greed Pine Seed → Run workflow
```

## TradingView Usage

After this repo is accepted/used as a TradingView Pine Seeds source, paste the Pine Script from:

```text
pine/cnn_fear_greed_index.pine
```

into TradingView Pine Editor.
