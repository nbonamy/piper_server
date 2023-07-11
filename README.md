# piper server

## Installation

By default you can just need to `pip install -r requirements.txt`.

But the python version of piper does not respect punctuation properly. So you can install a piper distribution in the `bin` folder. In that case, the server will use this and stream data back.

## Voices

You need to download piper voices files in the `voices` folder. Currently only `medium` quality is supported. Place both files under the voice name.

Example:
```
voices/ryan/en_US-ryan-medium.onnx
voices/ryan/en_US-ryan-medium.onnx.json
```

## Configuration

The configuration file is `config/config.yml`. Current parameters are:

- `http_server_port`: port to listen on (default `5008`)
- `voice`: default voice to use (default `ryan`)

## API

Only one endpoint is available: `GET /synthesize`. It accepts two query parameters:

- `text`: text to synthesize
- `voice` (optional): voice to use

