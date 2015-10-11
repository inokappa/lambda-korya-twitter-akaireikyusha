## Lambda -> twitter tutorial for Python

### Required

- Python
- [BeautifulSoup]()
- [python-twitter]()
- twitter Account

### How to Use

- Modules Install

```sh
% mkdir path/to/dir
% pip install BeautifulSoup -t /path/to/dir
% pip install twitter -t /path/to/dir
```

- Write Lambda function code

```sh
% cd path/to/dir
% vim lambda_function.py
```

- Creata Lambda function and function code

```sh
% zip -r your_function.zip *
% aws lambda --region ap-northeast-1 \
  create-function \
    --function-name your_function \
    --runtime python2.7 \
    --role arn:aws:iam::1234567890123:role/lambda_basic_execution \
    --handler lambda_function.handler \
    --zip-file fileb://your_function.zip
```

- Update function code

```sh
% zip -r your_function.zip * 
# Important 'fileb//', See http://docs.aws.amazon.com/cli/latest/reference/lambda/update-function-code.html.
% aws lambda --region ap-northeast-1 update-function-code --function-name your_function --zip-file fileb://your_function.zip
```
