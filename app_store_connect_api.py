"""
Core API logic for App Store Connect.
This file contains the business logic for fetching data,
which can be used by both the MCP server and a web server.
"""

from appstore_service.AppStore import AppStore

app_store = AppStore()

def list_apps():
    """Returns a list of applications."""
    return app_store.list_apps()

def get_app_info(bundle_id):
    """Returns detailed information for a single app."""
    if not bundle_id:
        return {"error": "Missing required parameter: bundleId"}, 400
    return app_store.get_app_info(bundle_id)

def list_beta_testers(group_id):
    """Returns a list of beta testers for a specific group."""
    if not group_id:
        return {"error": "Missing required parameter: groupId"}, 400
    return app_store.list_testers_in_group(group_id)

def list_beta_groups(bundle_id):
    """Returns a list of beta groups for an app."""
    if not bundle_id:
        return {"error": "Missing required parameter: bundleId"}, 400
    return app_store.get_beta_groups(bundle_id)

def list_testers_in_group(group_id):
    """Returns a list of beta testers for a specific group."""
    if not group_id:
        return {"error": "Missing required parameter: groupId"}, 400
    return app_store.list_testers_in_group(group_id)

def list_builds(bundle_id):
    """Returns a list of builds for an app."""
    if not bundle_id:
        return {"error": "Missing required parameter: bundleId"}, 400
    return app_store.get_builds(bundle_id)

def release_version(bundle_id, version_string, build_number, platform="IOS"):
    """Releases a new version of an app."""
    if not all([bundle_id, version_string, build_number]):
        return {"error": "Missing required parameters: bundle_id, version_string, build_number"}, 400
    return app_store.release_version(bundle_id, version_string, build_number, platform)

def submit_for_review(bundle_id, version):
    """Submitting an app version for review."""
    if not bundle_id or not version:
        return {"error": "Missing required parameters: bundleId, version"}, 400
    return app_store.assign_build(version)

def create_beta_group(name, bundle_id):
    """Creating a new beta group."""
    if not name or not bundle_id:
        return {"error": "Missing required parameters: name, bundleId"}, 400
    return app_store.create_beta_group(name, bundle_id)

def add_beta_tester_to_group(email, group_id):
    """Adding a beta tester to a group."""
    if not email or not group_id:
        return {"error": "Missing required parameters: email, groupId"}, 400
    return app_store.add_tester_to_group(email, group_id)

def remove_beta_tester_from_group(email, group_id, bundle_id):
    """Removing a beta tester from a group."""
    if not email or not group_id or not bundle_id:
        return {"error": "Missing required parameters: email, groupId, bundleId"}, 400
    return app_store.remove_tester_from_group(email, group_id, bundle_id)

def get_performance_metrics(bundle_id):
    """Returns a list of performance metrics for an app."""
    if not bundle_id:
        return {"error": "Missing required parameter: bundleId"}, 400
    return app_store.get_performance_metrics(bundle_id)