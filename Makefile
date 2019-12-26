SHELL = /usr/bin/env bash -xeuo pipefail
stack_name=''

isort:
	pipenv run isort -rc \
		src \
		tests/

lint:
	pipenv run flake8 \
		src \
		tests/

black:
	pipenv run black \
		src/ \
		tests/

package:
	rm -rf dist
	mkdir dist
	pipenv run aws cloudformation package \
		--template-file sam.yml \
		--s3-bucket $$ARTIFACTS_S3_BUCKET \
		--output-template-file dist/template.yml

deploy: package
	pipenv run aws cloudformation deploy \
		--template-file dist/template.yml \
		--stack-name $(stack_name) \
		--role-arn $(AWS_CFN_DEPLOY_ROLE_ARN) \
		--no-fail-on-empty-changeset

test-unit:
	AWS_DEFAULT_REGION=ap-northeast-1 \
	AWS_ACCESS_KEY_ID=dummy \
	AWS_SECRET_ACCESS_KEY=dummy \
	PYTHONPATH=src \
	pipenv run pytest tests/unit --cov-config=setup.cfg --cov=src;