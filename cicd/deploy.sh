#!/bin/sh
myS3BucketForDeployment="s3://edfx-rbn-pileface/swagger/"

signingName="PileFaceSigningProfile_LIRVA8ZRwYzt"
signingVersionnedArn="arn:aws:signer:eu-west-3:361509912577:/signing-profiles/PileFaceSigningProfile_LIRVA8ZRwYzt/rSAd0xLAYa"

currentDir=`pwd`

aws s3 cp ../swaggers/pileface.yaml $myS3BucketForDeployment


# Zip register lambda function
rm ../lambda/register/register.zip
zip -j ../lambda/register/register.zip ../lambda/register/*.py

# Zip with dependency bet lambda function
cd ../lambda/bet/package
rm ../bet.zip
zip -r ../bet.zip package/* .
cd ..
zip bet.zip *.py


cd $currentDir

sam package -t sam.yaml --signing-profiles BetBackend=$signingName RegisterBackend=$signingName --s3-bucket edfx-rbn-pileface --output-template-file packagedsam.yaml 
sam deploy -t packagedsam.yaml  --capabilities  CAPABILITY_IAM CAPABILITY_NAMED_IAM --stack-name pileface --parameter-overrides UidDeployment=77 LambdaSigningProfileProfileVersionArn=$signingVersionnedArn
