.PHONY: validate build test package publish clean license all

export AWS_DEFAULT_REGION ?= us-east-1
#export AWS_SERVERLESS_BUCKET ?= 
#export VERSION=

validate:
	@sam validate

build:
	@sam build

test: build
	@sam local invoke \
		--event tests/test.json --env-vars tests/env.json

package: validate
	@sam package \
		--s3-bucket $(AWS_SERVERLESS_BUCKET) \
		--s3-prefix $(shell basename $(CURDIR)) \
		--output-template-file packaged.yaml

publish: build package
	@sam publish \
		--template packaged.yaml \
		--semantic-version $(or $(VERSION), 1.0.0)

clean:
	@rm -f packaged.yaml
	@rm -rf .aws-sam

license:
	@find src/* -type d -exec cp LICENSE {} \;

all: clean publish