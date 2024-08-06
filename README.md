# tap-lightspeed

`tap-lightspeed` is a Singer tap for lightspeed that produces JSON-formatted 
data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md) 

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-lightspeed --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

base_url: It can be either "https://api.webshopapp.com" or "https://api.shoplightspeed.com" depending on how your store was set.

language: The language available for your store or the language that the store was configured to use.

Sample config:
```$json
{
  "base_url": "https://api.webshopapp.com",
  "language": "nl",
  "api_key": "my_api_key",
  "api_secret": "my_api_secret"
}
```


### Source Authentication and Authorization

## Usage

You can easily run `tap-lightspeed` by itself or in a pipeline.

### Executing the Tap Directly

```bash
tap-lightspeed --version
tap-lightspeed --help
tap-lightspeed --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```
