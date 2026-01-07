import boto3
import json
import os
from jinja2 import Template
import sys

# Define folders and S3 bucket from environment variables/arguments

S3_BUCKET_NAME = os.environ['S3_BUCKET']
AWS_REGION = os.environ['AWS_REGION']

def process_prompt_and_upload(config_file, bucket_name, region):
    # Load config and template
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    template_path = os.path.join('prompt_templates', config['template_file'])
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Render prompt
    template = Template(template_content)
    rendered_prompt = template.render(**config['variables'])

    # Invoke Bedrock
    bedrock = boto3.client(service_name='bedrock-runtime', region_name=region)
    body = json.dumps({
        "messages": [{"role": "user", "content": [{"type": "text", "text": rendered_prompt}]}],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000
    })
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0', # or another model
        contentType='application/json',
        accept='application/json',
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    generated_content = response_body['content'][0]['text']

    # Save to outputs folder
    output_filename = config_file.replace('prompts/', 'outputs/').replace('.json', f'.{config["output_format"]}')
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, 'w') as f:
        f.write(generated_content)
    print(f"Generated content saved to {output_filename}")

    # Upload to S3
    s3 = boto3.client('s3', region_name=region)
    environment = os.environ.get('ENVIRONMENT', 'beta')
    s3_key = f"{environment}/outputs/{os.path.basename(output_filename)}"
    s3.upload_file(output_filename, bucket_name, s3_key, ExtraArgs={'ContentType': f'text/{config["output_format"]}'})
    print(f"Uploaded {output_filename} to s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_prompt.py <prompt_config_file_path>")
        sys.exit(1)
    process_prompt_and_upload(sys.argv[1], S3_BUCKET_NAME, AWS_REGION)
