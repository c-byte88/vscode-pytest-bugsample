"""This module contains acceptance test helpers."""


def remove_dbfs_prefix(platform_layer_path: str) -> str:
    """
    Remove dbfs prefix from the platform layer path available in includes/global/constants.

    Args:
        platform_layer_path (str): Constant with the container path in datalake

    Returns:
        str: path without "dbfs/" as dbutils does not needs it
    """
    if len(platform_layer_path.split('/dbfs')) != 1:
        mount_point_path = platform_layer_path.split('/dbfs')[1]
    elif len(platform_layer_path.split('dbfs:')) != 1:
        mount_point_path = platform_layer_path.split('dbfs:')[1]
    else:
        mount_point_path = platform_layer_path

    return mount_point_path
