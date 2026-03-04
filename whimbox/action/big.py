from whimbox.interaction.interaction_core import itt
from whimbox.common.utils.ui_utils import *
from whimbox.task.task_template import *
from whimbox.ability.ability import ability_manager
from whimbox.ability.cvar import ABILITY_NAME_BIG

class BigTask(TaskTemplate):
    def __init__(self, session_id):
        super().__init__(session_id=session_id, name="BigTask")
    
    @register_step("开始变大")
    def step1(self):
        if not ability_manager.change_ability(ABILITY_NAME_BIG):
            self.update_task_result(status=STATE_TYPE_FAILED, message="切换变大能力失败")
            return STEP_NAME_FINISH
        itt.right_click()

    def handle_finally(self):
        pass

if __name__ == "__main__":
    task = BigTask(session_id="debug")
    task.task_run()
