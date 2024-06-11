import allure


def test(page):
    allure.step("Navigate to flo web")
    page.navigate_to_flo_web()
    assert False
