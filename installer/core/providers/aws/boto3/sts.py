import boto3


def get_sts_client(access_key, secret_key, session_token):
    """
    Returns AWS sts client object

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        obj: AWS Sts client Object
    """
    return boto3.client(
        "sts",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token)


def get_user_account_id(access_key, secret_key, session_token):
    """
    Returns AWS user account id from the given credentials

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        account_id (str): AWS user account ID
    """
    return get_sts_client(access_key, secret_key, session_token).get_caller_identity().get('Account')
