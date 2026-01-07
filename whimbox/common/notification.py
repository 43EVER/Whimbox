"""
Windows 通知模块
提供系统通知功能
"""
import os
import threading
from whimbox.common.logger import logger
from whimbox.config.config import global_config

# 尝试导入 win10toast
try:
    from win10toast import ToastNotifier
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False
    logger.warning("win10toast 未安装，Windows通知功能将不可用")


class WindowsNotifier:
    """Windows 通知管理器"""
    
    def __init__(self):
        self.toaster = None
        if TOAST_AVAILABLE:
            try:
                self.toaster = ToastNotifier()
            except Exception as e:
                logger.error(f"初始化 Windows 通知失败: {e}")
                self.toaster = None
    
    def is_enabled(self) -> bool:
        """检查通知功能是否启用"""
        try:
            enable_notification = global_config.get_bool("Path", "enable_windows_notification", False)
            return enable_notification and self.toaster is not None
        except Exception:
            return False
    
    def send_notification(self, title: str, message: str, status: str = "", threaded: bool = True):
        """
        发送 Windows 通知
        
        Args:
            title: 通知标题
            message: 通知内容
            status: 任务状态（用于选择图标）
            threaded: 是否在新线程中发送（避免阻塞主线程）
        """
        if not self.is_enabled():
            logger.debug("Windows 通知功能未启用或不可用")
            return
        
        if not message:
            logger.debug("通知消息为空，跳过发送")
            return
        
        def _send():
            try:
                duration = 5
                
                logger.debug(f"发送 Windows 通知: {title} - {message[:50]}...")
                
                self.toaster.show_toast(
                    title=title,
                    msg=message,
                    duration=duration,
                    threaded=False  # 在子线程中已经是异步的
                )
            except Exception as e:
                logger.error(f"发送 Windows 通知失败: {e}")
        
        if threaded:
            # 在新线程中发送通知，避免阻塞主流程
            thread = threading.Thread(target=_send, daemon=True)
            thread.start()
        else:
            _send()


# 全局通知器实例
_notifier = None


def get_notifier() -> WindowsNotifier:
    """获取全局通知器实例"""
    global _notifier
    if _notifier is None:
        _notifier = WindowsNotifier()
    return _notifier


def send_notification(title: str, message: str, status: str = ""):
    """
    发送 Windows 通知的便捷函数
    
    Args:
        title: 通知标题
        message: 通知内容
        status: 任务状态
    """
    notifier = get_notifier()
    notifier.send_notification(title, message, status)

