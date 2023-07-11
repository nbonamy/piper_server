# piper server

## Installation

By default you can just need to `pip install -r requirements.txt`.

But the python version of piper does not respect punctuation properly. So you can install a piper distribution in the `bin` folder. In that case, the server will use this and stream data back. Also the command line version supports streaming of synthesized audio so you may want to enable it if you generate long texts.

## Voices

You need to download piper voices files in the `voices` folder. Place both files under the voice name.

Example:
```
voices/ryan/en_US-ryan-medium.onnx
voices/ryan/en_US-ryan-medium.onnx.json
```

## Configuration

The configuration file is `config/config.yml`. Current parameters are:

- `http_server_port`: port to listen on (default `5008`)
- `voices`: default voices to use per language (default `ryan/medium` for all languages if not specified). You need to specify this per language.

Example:
```yaml
voices:
  fr-FR: gilles/low
```

## API

Only one endpoint is available: `GET /synthesize`. It accepts two query parameters:

- `text`: text to synthesize
- `lang`: language (will select `voice` automatically based on configuration)
- `voice` (optional): voice to use in the format `voice/quality`. If quality is not specified it defaults to medium

