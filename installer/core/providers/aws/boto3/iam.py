import boto3


def get_iam_client(access_key, secret_key, session_token):
    """
    Returns the client object for AWS IAM

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        obj: AWS IAM Object
    """
    return boto3.client(
        'iam',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token)


def get_iam_resource(access_key, secret_key, session_token):
    """
    Returns the Resource client object for AWS IAM

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        obj: AWS IAM Resource Object
    """
    return boto3.client(
        'sts',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token)


def get_user(access_key, secret_key, session_token):
    """
    Returns the username of the given user credentails

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        arn (str): AWS IAM User name
    """
    iam = get_iam_resource(access_key, secret_key, session_token)
    arn = iam.CurrentUser().arn

    return arn


def get_current_user(access_key, secret_key, session_token):
    """
    Returns the user detials of the given user credentails

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        user (obj): AWS IAM User
    """
    iam = get_iam_resource(access_key, secret_key, session_token).get_caller_identity()
    return 'ADMIN' #iam['Arn'].split('/')[-1]


def get_aws_account_user(access_key, secret_key, session_token):
    """
    Returns the user details of the current user

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        obj: AWS IAM User
    """
    return get_iam_resource.CurrentUser(access_key, secret_key, session_token)


def get_iam_user_policy_names(access_key, secret_key, session_token, arn):
    """
    Returns the policy names of the current user has

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        arn (str): AWS user name

    Returns:
        policy_names (list): List of policy names the current user has
    """
    iam_client = get_iam_client(access_key, secret_key, session_token)
    attached_policies = iam_client.list_attached_role_policies(RoleName=arn)['AttachedPolicies']
    attached_policy_names = [policy['PolicyName'] for policy in attached_policies]
    user_policy_names = iam_client.list_role_policies(RoleName=arn)['PolicyNames']

    return attached_policy_names + user_policy_names


def get_group_managed_policy_names(iam_client, groups):
    """
    Returns the group managed policy names of the current user

    Args:
        iam_client (obj): IAM client obj
        groups (list): User groups

    Returns:
        policy_names (list): List of group managed policy names the current user has
    """
    policy_names = []
    for group in groups:
        attached_policies = iam_client.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']
        policy_names += [policy['PolicyName'] for policy in attached_policies]

    return policy_names


def get_group_policy_names(iam_client, groups):
    """
    Returns the group policy names of the current user

    Args:
        iam_client (obj): IAM client obj
        groups (list): User groups

    Returns:
        policy_names (list): List of group policy names the current user has
    """
    policy_names = []
    for group in groups:
        group_policy_names = iam_client.list_group_policies(GroupName=group['GroupName'])['PolicyNames']
        policy_names += group_policy_names

    return policy_names


def get_user_group_policy_names(access_key, secret_key, session_token, arn):
    """
    Returns all group user policies of a user

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        arn (str): AWS user name

    Returns:
        policy_names (list): List of  all goup policy names the current user has
    """
    iam_client = get_iam_client(access_key, secret_key, session_token)
    #groups = iam_client.list_groups_for_user(UserName=arn)['Groups']
    groups = iam_client.list_groups()['Groups']
    group_managed_policy_names = get_group_managed_policy_names(iam_client, groups)
    group_policy_names = get_group_policy_names(iam_client, groups)

    return group_managed_policy_names + group_policy_names


def get_all_policy_names(access_key, secret_key, session_token):
    """
    Returns all group and user policies of a user

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        policy_names (list): List of  all goup policy names and user policy names the current user has
    """
    iam = get_iam_resource(access_key, secret_key, session_token)
    arn = iam.get_caller_identity().arn

    user_policy_names = get_iam_user_policy_names(access_key, secret_key, session_token, arn)
    user_group_policy_names = get_user_group_policy_names(access_key, secret_key, session_token, arn)

    return user_policy_names + user_group_policy_names


def create_iam_service_linked_role(access_key, secret_key, session_token, service_name, desc):
    """
    Create AWS ES service linked role

    Args:
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key
        service_name (str): Service name
        desc (str): Descsription

    Returns:
        Set: True if created else false with error
    """
    role_name = "AWSServiceRoleForAmazonElasticsearchService"
    iam_client = get_iam_client(access_key, secret_key, session_token)
    try:
        iam_client.create_service_linked_role(
            AWSServiceName=service_name,
            Description=desc
        )
        return True, None
    except Exception as e:
        return False, str(e)


def check_role_exists(role_name, access_key, secret_key, session_token):
    """
    Check wheter the given IAM role already exists in the AWS Account

    Args:
        role_name (str): Role name
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        Boolean: True if env exists else False
    """
    iam_client = get_iam_client(access_key, secret_key, session_token)
    try:
        role = iam_client.get_role(RoleName=role_name)
        return True if role else False
    except:
        return False


def check_policy_exists(policy_name, access_key, secret_key, session_token, account_id):
    """
    Check wheter the given IAM policy already exists in the AWS Account

    Args:
        policy_name (str): Policy name
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        Boolean: True if env exists else False
    """
    iam_client = get_iam_client(access_key, secret_key, session_token)
    policy_arn = "arn:aws:iam::%s:policy/%s" % (str(account_id), policy_name)

    try:
        policy = iam_client.get_policy(PolicyArn=policy_arn)
        return True if policy else False
    except:
        return False


def check_instance_profile_exists(instance_profile_name, access_key, secret_key, session_token):
    """
    Check wheter the given IAM instance profile already exists in the AWS Account

    Args:
        instance_profile_name (str): Instance profile name
        access_key (str): AWS Access Key
        secret_key (str): AWS Secret Key

    Returns:
        Boolean: True if env exists else False
    """
    iam_client = get_iam_client(access_key, secret_key, session_token)
    try:
        profile = iam_client.get_instance_profile(InstanceProfileName=instance_profile_name)
        return True if profile else False
    except:
        return False
