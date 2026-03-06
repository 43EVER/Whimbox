from whimbox.common.utils.asset_utils import *
from whimbox.common.cvars import *
from whimbox.ui.template.posi_manager import Area


class TextTemplate(AssetBase):
    def __init__(self, text:str, cap_area:Area, name=None, match_mode=CONTAIN_MATCHING, print_log=LOG_WHEN_TRUE):
        if name is None:
            super().__init__(get_name_from_caller(depth=2))
        else:
            super().__init__(name)
            
        self.text = text
        self.cap_area = cap_area
        self.match_mode = match_mode
        self.print_log = print_log
    def gettext(self):
        return self.text

    def match_results(self, res:list):
        if isinstance(res, str):
            res = [res]
        for inp in res:
            #TODO: add match rules
            if inp == '':
                continue
            if self.match_mode == CONTAIN_MATCHING:
                if self.text in inp:
                    return True
                else:
                    continue
            elif self.match_mode == ACCURATE_MATCHING:
                if self.text == inp:
                    return True
                else:
                    continue
        return False

class Text(TextTemplate):
    def __init__(self, text, cap_area, name=None, print_log = LOG_WHEN_TRUE) -> None:
        if name is None:
            name = get_name_from_caller(depth=2)
        super().__init__(text, cap_area=cap_area, name=name, print_log=print_log)


# if __name__ == '__main__':  
#     print(text(conti_challenge))
