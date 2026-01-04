from whimbox.common.utils.ui_utils import scroll_find_click
from whimbox.task.task_template import *
from whimbox.interaction.interaction_core import itt
from whimbox.ui.ui_assets import *
from whimbox.common.keybind import keybind

class PlaceItemTask(TaskTemplate):
    def __init__(self):
        super().__init__("place_item_task")

    @register_step("选择摆饰")
    def step1(self):
        if itt.get_img_existence(IconItemPlaceable):
            return
        else:
            itt.key_down(keybind.KEYBIND_ITEM)
            time.sleep(3)
            itt.key_up(keybind.KEYBIND_ITEM)
            if not scroll_find_click(AreaItemQuickList, IconItemPlaceable, scale=1.05, threshold=IconItemPlaceable.threshold, need_scroll=False):
                self.update_task_result(status=STATE_TYPE_FAILED, message="快捷物品中未找到摆饰")
                return STEP_NAME_FINISH

    @register_step("放置摆饰")
    def step2(self):
        itt.key_press(keybind.KEYBIND_ITEM)
        while not self.need_stop():
            itt.left_click()
            time.sleep(1)
            if itt.get_img_existence(IconItemCantPlace):
                itt.move_to((-200, 0), relative=True)
            else:
                self.log_to_gui("摆饰放置成功")
                break


if __name__ == "__main__":
    task = PlaceItemTask()
    result = task.task_run()
    print(result)