import os
import json
import urllib3

allowedDomains = ["@trimble.com", "@cityworks.com"]
apiKey = os.environ['MASV_API_KEY']
apiBase = "https://api.massive.app/v1"

def get_response(method, url, params, headers):
    http = urllib3.PoolManager()
    if method == "GET":
        r = http.request(
            method,
            url,
            fields=params,
            headers=headers
        )
    elif method == "POST":
        encoded_data = json.dumps(params).encode('utf-8')
        r = http.request(
            method,
            url,
            body=encoded_data,
            headers=headers
        )
    return json.loads(r.data.decode('utf-8'))

def get_package_token(packageId, portalId):
    url = apiBase + "/portals/" + portalId + "/packages"
    params = {'finalized': '1'}
    headers = {'X-API-KEY': apiKey}
    response = get_response("GET", url, params, headers)
    packageToken = next(package['access_token'] for package in response if package['id'] == packageId)
    return packageToken

def get_recipient_email(packageId, packageToken):
    url = apiBase + "/packages/" + packageId + "/metadata"
    params = {}
    headers = {'X-Package-Token': packageToken}
    response = get_response("GET", url, params, headers)['fields']
    recipientEmail = next(field['value'] for field in response if field['name'] == "recipient_email")
    return recipientEmail

def send_email(recipientEmail, packageId, packageToken):
    url = apiBase + "/packages/" + packageId + "/links"
    params = {"email": recipientEmail}
    headers = {'X-Package-Token': packageToken, 'Content-Type': 'application/json'}
    response = get_response("POST", url, params, headers)
    return response

def lambda_handler(event, context):
    print("Received Event: {}".format(event))
    masvEvent = json.loads(event['body'])
    packageId = masvEvent['object']['id']
    packageName = masvEvent['object']['name']
    portalId = masvEvent['object']['portal_id']

    packageToken = get_package_token(packageId, portalId)
    recipientEmail = get_recipient_email(packageId, packageToken)

    if any(domain in recipientEmail.lower() for domain in allowedDomains):
        result = send_email(recipientEmail, packageId, packageToken)
        print("Sent email to {} for package {}".format(recipientEmail, packageName))
        print("Response: {}".format(result))
    else:
        print("Failed to send email to {}. The recipient domain must be in {}.".format(recipientEmail, allowedDomains))
