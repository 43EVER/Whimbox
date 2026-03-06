import cv2
import numpy as np
from copy import deepcopy

from whimbox.common.utils.asset_utils import *
from whimbox.common.cvars import *
from whimbox.common.utils.img_utils import crop, process_with_hsv_limit


class ImgIcon(AssetBase):
    
    def __init__(self,
                 path=None,
                 name=None,
                 is_bbg=None,
                 bbg_posi=None,
                 cap_posi = None,
                 threshold=None,
                 hsv_limit=None,
                 gray_limit=None,
                 print_log = LOG_ALL if DEBUG_MODE else LOG_WHEN_TRUE,
                 anchor=ANCHOR_TOP_LEFT):
        """创建一个img对象，用于图片识别等。

        Args:
            path (str): 图片路径。
            name (str): 图片名称。默认为图片名。
            is_bbg (bool, optional): 是否为黑色背景图片. Defaults to True.
            bbg_posi (AnchorPosi/None, optional): 黑色背景的图片坐标，默认自动识别坐标. Defaults to None.
            cap_posi (AnchorPosi/str, optional): 截图坐标。注意：可以填入'bbg'字符串关键字，使用bbg坐标; 可以填入'all'字符串关键字，截图全屏. Defaults to None.
            threshold (float|tuple(float, float), optional): 匹配阈值. var1>var2. Defaults to 0.91.
            print_log (int, optional): 打印日志模式. Defaults to LOG_NONE.
            anchor (str, optional): 相对位置锚点. Defaults to ANCHOR_TOP_LEFT.
        """
        if name is None:
            super().__init__(get_name_from_caller(depth=2))
        else:
            super().__init__(name)
        
        if path is None:
            path = self.get_img_path()

        if threshold is None:
            threshold = 0.98

        self.origin_path = path
        self._init_is_bbg = is_bbg
        self._init_bbg_posi = bbg_posi
        self._init_cap_posi = cap_posi
        self._init_anchor = anchor

        self.threshold = threshold
        self.hsv_limit = hsv_limit
        self.gray_limit = gray_limit
        self.print_log = print_log

        self._raw_image = None
        self._image = None
        self._bbg_posi = None
        self._cap_posi = None
        self._cap_center_position_xy = None
        self._is_bbg_resolved = None
        self._loaded = False

    def _ensure_loaded(self):
        if self._loaded:
            return

        raw_image = cv2.imread(self.origin_path)
        if raw_image is None:
            raise FileNotFoundError(f"image not found or unreadable: {self.origin_path}")

        is_bbg = self._init_is_bbg
        if is_bbg is None:
            is_bbg = raw_image.shape == (1080, 1920, 3)

        if is_bbg and self._init_bbg_posi is None:
            bbg_posi = asset_get_bbox(raw_image, anchor=self._init_anchor)
        else:
            bbg_posi = self._init_bbg_posi

        if self._init_cap_posi == 'bbg':
            cap_posi = bbg_posi
        elif self._init_cap_posi is None and is_bbg:
            cap_posi = bbg_posi
        elif self._init_cap_posi == 'all':
            cap_posi = AnchorPosi(0, 0, 1920, 1080)
        else:
            cap_posi = self._init_cap_posi

        if cap_posi is None:
            cap_posi = AnchorPosi(0, 0, 1080, 1920)

        if is_bbg:
            image = crop(raw_image, bbg_posi)
        else:
            image = raw_image.copy()

        if self.hsv_limit is not None:
            temp_image = process_with_hsv_limit(image, self.hsv_limit[0], self.hsv_limit[1])
            box = asset_get_bbox(temp_image)
            image = crop(temp_image, box, copy=False)
        elif self.gray_limit is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
            _, temp_image = cv2.threshold(image, self.gray_limit[0], self.gray_limit[1], cv2.THRESH_BINARY)
            box = asset_get_bbox(temp_image)
            image = crop(temp_image, box, copy=False)

        self._raw_image = raw_image
        self._image = image
        self._bbg_posi = bbg_posi
        self._cap_posi = cap_posi
        self._cap_center_position_xy = cap_posi.get_center()
        self._is_bbg_resolved = is_bbg
        self._loaded = True

    @property
    def raw_image(self):
        self._ensure_loaded()
        return self._raw_image

    @property
    def image(self):
        self._ensure_loaded()
        return self._image

    @property
    def bbg_posi(self):
        self._ensure_loaded()
        return self._bbg_posi

    @property
    def cap_posi(self):
        self._ensure_loaded()
        return self._cap_posi

    @property
    def cap_center_position_xy(self):
        self._ensure_loaded()
        return self._cap_center_position_xy

    @property
    def is_bbg(self):
        self._ensure_loaded()
        return self._is_bbg_resolved
            
    def copy(self):
        return deepcopy(self)
    
    def show_image(self):
        cv2.imshow('123', self.image)
        cv2.waitKey(0)


class GameImg(AssetBase):
    def __init__(self, path=None, name=None):
        if name is None:
            super().__init__(get_name_from_caller(depth=2))
        else:
            super().__init__(name)
        
        if path is None:
            path = self.get_img_path()
    
        self.origin_path = path
        self._raw_image = None
        self._loaded = False

    def _ensure_loaded(self):
        if self._loaded:
            return
        raw_image = cv2.imread(self.origin_path, cv2.IMREAD_UNCHANGED)
        if raw_image is None:
            raise FileNotFoundError(f"image not found or unreadable: {self.origin_path}")
        self._raw_image = raw_image
        self._loaded = True

    @property
    def raw_image(self):
        self._ensure_loaded()
        return self._raw_image
    
    def copy(self):
        return deepcopy(self)
    

if __name__ == '__main__':
    # img = refrom_img(cv2.imread("assets\\imgs\\common\\coming_out_by_space.jpg"),posi_manager.get_posi_from_str('coming_out_by_space'))
    # cv2.imwrite("assets\\imgs\\common\\coming_out_by_space.jpg", img)
    # get_img_from_imgname(COMING_OUT_BY_SPACE)
    # pname = F_BUTTON
    # p = auto_import_img("assets\\imgs\\common\\ui\\" + "time_menu_core" + ".jpg", "swimming")
    # print(p)
    pass
