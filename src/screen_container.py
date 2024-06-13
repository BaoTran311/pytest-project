from src.utils import appium_util


class iPhoneContainer:

    def __init__(self):
        ...

    def launch_flo_iphone(self):
        driver = appium_util.init_appium_driver("iPhone")
        self.__setattr__("_driver", driver)
        return self

