from whimbox.task.task_template import TaskTemplate, register_step
from whimbox.interaction.interaction_core import itt
from whimbox.ui.ui_assets import *
from whimbox.common.utils.utils import is_chinese
from whimbox.common.keybind import keybind
from whimbox.common.utils.ui_utils import wait_until_appear
import time, re

class PickupTask(TaskTemplate):
    def __init__(self, session_id):
        super().__init__(session_id=session_id, name="pickup_task")
        self.material_count_dict = {}

    @register_step("开始采集")
    def step1(self):
        retry_time = 2
        while not self.need_stop():
            if wait_until_appear(IconPickupFeature, area=AreaPickup, retry_time=retry_time):
                retry_time = 1
                itt.key_press(keybind.KEYBIND_INTERACTION)
                time.sleep(0.5) # 等待采集结果文字出现
                texts = itt.ocr_multiple_lines(AreaMaterialGetText)
                for text in texts:
                    if "精粹" in text or "心得" in text or "种子" in text:
                        continue
                    else:
                        pattern = r"^(.+?)[×xX]([0-9]+(?:\.[0-9]+)?)$"
                        match = re.match(pattern, text)
                        if match:
                            pickup_item = match.group(1)
                            if pickup_item in self.material_count_dict:
                                self.material_count_dict[pickup_item] += 1
                            else:
                                self.material_count_dict[pickup_item] = 1
                        elif is_chinese(text):
                            pickup_item = text
                            if pickup_item in self.material_count_dict:
                                self.material_count_dict[pickup_item] += 1
                            else:
                                self.material_count_dict[pickup_item] = 1
            else:
                break
        
        if len(self.material_count_dict) == 0:
            self.update_task_result(message="未采集到物品")
            return
        count_str_list = []
        for key, value in self.material_count_dict.items():
            count_str_list.append(f"{key}x{value}")
        res = ",".join(count_str_list)
        res = f"获得{res}"
        self.update_task_result(
            message=res,
            data=self.material_count_dict
        )
    
    def handle_finally(self):
        pass

if __name__ == "__main__":
    pickup_task = PickupTask(session_id="debug")
    pickup_task.task_run()
