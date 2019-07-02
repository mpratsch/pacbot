import boto3


def get_ecr_client(access_key, secret_key, session_token, region):
    """
    Returns the client object for AWS ECR (Elastic COntainer Repository)

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        region (str): AWS Region

    Returns:
        obj: AWS ECR Object
    """
    return boto3.client(
        "ecr",
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token)


def check_ecr_exists(repo_name, access_key, secret_key, session_token, region):
    """
    Check wheter the given ECR already exists in AWS account

    Args:
        repo_name (str): Repository name
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        region (str): AWS Region

    Returns:
        Boolean: True if env exists else False
    """
    client = get_ecr_client(access_key, secret_key, session_token, region)
    try:
        response = client.describe_repositories(repositoryNames=[repo_name])
        return True if len(response['repositories']) else False
    except:
        return False
