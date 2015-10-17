# Google Cloud Logging Demo
This Google App Engine application is a demo for BarCamp HK 2015. The goal of
this project is to illustrate how to use the Google Cloud Logging API. The
version of Google Cloud Logging API is _v1beta3_.

# Requirments
- Google Cloud SDK (for deploying the code to GAE)
- A Google Project (made in Google Developer Console)

# Usage
simply send a http POST request to `/` with the following data

- msg: the message to be logged.

```bash
  curl -d "msg=Hello" https://YOU_PROJECT.appspot.com/
```
