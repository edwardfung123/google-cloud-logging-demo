import webapp2
import logging
import json
from google.appengine.api import memcache

class IndexHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('To log, post to /')

  def _get_service(self):
    import httplib2
    from apiclient.discovery import build
    import os
    ''' Return the Cloud Logging API service '''
    is_local = os.environ['SERVER_SOFTWARE'].startswith('Development')
    logging.debug('is_local = {}'.format(is_local))
    scopes = ['https://www.googleapis.com/auth/logging.read', 'https://www.googleapis.com/auth/logging.write']
    if is_local:
      from oauth2client.client import SignedJwtAssertionCredentials
      with open("privatekey.json") as f:
          json_string = f.read()
          service_accout = json.loads(json_string)
          client_email = service_accout['client_email']
          private_key = service_accout['private_key']
          credentials = SignedJwtAssertionCredentials(client_email, private_key, scopes)
    else:
      from oauth2client.appengine import AppAssertionCredentials
      credentials = AppAssertionCredentials(scopes)

    http_auth = credentials.authorize(httplib2.Http(memcache))
    service = build('logging', 'v1beta3', http=http_auth)
    return service

  def post(self):
    msg = self.request.get('msg')
    cloud_logging = self._get_service()
    from google.appengine.api.app_identity import app_identity
    projectsId = app_identity.get_application_id()
    deviceid = 'test-test'
    logsId = 'barcamp2015'
    severity = 'DEBUG'
    logs = {
      'commonLabels': {
        'compute.googleapis.com/resource_id': deviceid,
        "compute.googleapis.com/resource_type": "instance",
      },
      'entries': [
        {
          "log": logsId,
          "metadata": {
            "serviceName": "compute.googleapis.com",
            "severity": severity,
          },
          "textPayload": msg,
        },
      ]
    }
    resp = cloud_logging.projects().logs().entries().write(projectsId=projectsId, logsId=logsId, body=logs).execute()
    logging.info(json.dumps(resp, sort_keys=True, indent=4))
    self.response.write('log saved')

app = webapp2.WSGIApplication([
  (r'/', IndexHandler),
  ], debug=True)

