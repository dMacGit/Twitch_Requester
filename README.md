


# Twitch_Requester
### Current Release | [![Version](https://img.shields.io/badge/Release-v0.2.0-brightgreen.svg)](https://github.com/dMacGit/Twitch_Requester/releases/tag/v0.2.0)

*A simple test app that requests live stream data using the twitch tv api*

### Important note:


**Requires the Requests Dependency** [![Requests](https://img.shields.io/badge/Release-v2.11.1-blue.svg)](https://pypi.python.org/pypi/requests)
**& uses the** [json](https://docs.python.org/2/library/json.html) module

**To add Requests module use** [pip](https://docs.python.org/3/installing/) **and simply type** `$ pip install requests`

-> *__Don't have pip? Install using the guide here__* [pip install](https://packaging.python.org/installing/) 

This test app requires that an app id is already requested from an existing Twitch account.
In order to use this app and the api, the id must be sent with certain requests.

To use an app id with this test app, simply create a `config.text` file with the line `id:` then your app id.

_example:_ `id:my_id`

