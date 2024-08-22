#!/bin/sh
echo "Building"

cd request_ride_planning
mkdir package

pip install -r requirements.txt --target package/ --platform manylinux2014_x86_64 --only-binary=:all: --implementation cp --python-version 3.12
cp -r src/ package/src/

rm -f function.zip
cd package
zip -r9 ../function.zip *
cd ..
zip -g function.zip main.py

cd ..

echo "Packaging"
aws cloudformation package --template-file template.yaml --s3-bucket ride-planning-package-bucket-321321321 --s3-prefix ride-planning --output-template-file output.yaml
echo "Deploying"
aws cloudformation deploy --template-file output.yaml --stack-name ride-planning --capabilities CAPABILITY_NAMED_IAM


echo "Cleaning"
rm -rf /request_ride_planning/package
rm -rf /request_ride_planning/function.zip

echo "Concluded"

