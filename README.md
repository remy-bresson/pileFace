# pileFace
Simple project using AWS api gateway integration with :
- AWS Lambda (in python)
- AWS Step function
- AWS Dynamo DB

It's also contain a Step function definition.
Everything is deployed using SAM + Cloudformation.

You must create a S3 bucket to support the SAM deployment, and activate versionning on this S3 bucket, then update cicd/deploy.sh with the s3 bucket url  (myS3BucketForDeployment variable)

As this project is using code signing aws functionnality you must first deploy the signing resources (just one thime before the first deployment) :
sam deploy -t ./signingCode/samSigning.yaml --stack-name lambdaSigningStack 

You now need to go on aws console, Signer service (as the cli as no way to read Versioned Profile ARN), open the signing profile created at previous step and copy :
* Profile name
* Versioned Profile ARN (!!! not the Profile ARN VERY IMPORTANT)
In cicd/deploy.sh, copy the value from the aws Signer console: 
* signingName = [Profile name]
* signingVersionnedArn = [Versioned Profile ARN]


To deploy it : 
- cd cicd
- ./deploy.sh




## NOTE
Nothing has been done regarding UI except initializing a react project
