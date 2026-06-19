from project_setup_helper.os_detect import get_platform_key


def test_platform_key_is_known():
    assert get_platform_key() in {"macos_apple_silicon", "macos_other", "windows", "linux"}
