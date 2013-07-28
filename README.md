# REDCaptainHook

This project aims to implement a site-wide application that responds to REDCap Data Entry triggers by queuing work to be done. Users will be able to log in, setup their projects, triggers and processes and RCH will do the rest.

## Development

### Environment variables

These environment variables are used in development.

*   RCH_DEV_DB_HOST
*   RCH_DEV_DB_PASS
*   RCH_DEV_DB_USER
*   RCH_DEV_DB_PORT
*   RCH_DEV_DB_NAME
*   SECRET_KEY

You should also set `DJANGO_SETTINGS_MODULE` to `redcaptainhook.settings.dev` so you don't always have to specify `--settings`.

### Requirements

Setup a virtual environment and `pip install -r reqs/dev.text`. That should build everything you need in the dev environment.

Scott Burns
scott.s.burns@vanderbilt.edu

