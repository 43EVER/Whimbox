from whimbox.task.task_template import *
from whimbox.interaction.interaction_core import itt
from whimbox.common.utils.ui_utils import*
from whimbox.ui.ui_assets import *

class TransAnimalTask(TaskTemplate):
    def __init__(self, times=1):
        super().__init__("trans_animal_task")
        self.times = times
    
    @register_step("变身动物")
    def step1(self):
        while not self.need_stop() and self.times > 0:
            if not wait_until_appear(TextTransAnimal, retry_time=10):
                self.update_task_result(status=STATE_TYPE_FAILED, message="未找到变身按钮")
                return STEP_NAME_FINISH
            itt.key_press(keybind.KEYBIND_INTERACTION)
            itt.delay(2, comment="等待变身完成")
            self.times -= 1
        itt.key_press(keybind.KEYBIND_BACK)
        itt.wait_until_stable(threshold=0.95)
        if not scroll_find_click(AreaDialog, "确认", str_match_mode=0, need_scroll=False):
            self.update_task_result(status=STATE_TYPE_FAILED, message="未找到确认按钮")
            return STEP_NAME_FINISH

if __name__ == "__main__":
    trans_animal_task = TransAnimalTask(times=3)
    result = trans_animal_task.task_run()
    print(result)