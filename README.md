# MASV webhook handler
This is a solution for MASV. It allows of the uploader in a Portal to specify a recipient email address so the notification can be sent to a specific person dynamically.

1. Create a Lambda function in AWS using the code in lambda_function.py. Enable a public Function URL.
2. Create a MASV Portal with a Custom Form and add a new required field called Recipient Email with a key of recipient_email.
3. Use the MASV API to get a User Token. https://developer.massive.io/masv-api/auth/
4. Create a Custom Webhook using "package.finalized" as the event and the Lambda Function URL as the url. https://developer.massive.io/masv-api/webhooks/#create-webhook
5. List the Portals and copy the entire Portal object for the next step. https://developer.massive.io/masv-api/portals/#listing-portals
6. Attach the Custom Webhook to the Portal. https://developer.massive.io/masv-api/webhooks/#attach-custom-webhook-to-portal
7. Create a MASV API Key. https://developer.massive.io/masv-api/apikeys/
8. In the Lambda function, add an Environment Variable named MASV_API_KEY with a value of the API Key created in the last step.
9. Modify the allowedDomains list in the code to include all the email domains you will allow notifications to be sent to.