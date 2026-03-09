from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Dict, Iterator, Optional


WaitPolicy = str


@dataclass
class AcquireResult:
    acquired: bool
    reason: str = ""


class _ResourceSlot:
    def __init__(self) -> None:
        self.condition = threading.Condition()
        self.active = False
        self.owner: Optional[str] = None


class ToolInvocationCoordinator:
    def __init__(self) -> None:
        self._slots: Dict[str, _ResourceSlot] = {}
        self._slots_lock = threading.Lock()

    def _get_slot(self, resource_group: str) -> _ResourceSlot:
        with self._slots_lock:
            slot = self._slots.get(resource_group)
            if slot is None:
                slot = _ResourceSlot()
                self._slots[resource_group] = slot
            return slot

    def acquire_sync(
        self,
        *,
        resource_group: str,
        owner: str,
        wait_policy: WaitPolicy,
        stop_event: Optional[threading.Event] = None,
        on_wait: Optional[Callable[[], None]] = None,
        poll_interval: float = 0.1,
    ) -> AcquireResult:
        slot = self._get_slot(resource_group)
        wait_notified = False
        with slot.condition:
            while slot.active:
                if wait_policy == "skip_if_busy":
                    return AcquireResult(False, "busy")
                if stop_event is not None and stop_event.is_set():
                    return AcquireResult(False, "stopped")
                if not wait_notified and on_wait is not None:
                    on_wait()
                    wait_notified = True
                slot.condition.wait(timeout=poll_interval)
            if stop_event is not None and stop_event.is_set():
                return AcquireResult(False, "stopped")
            slot.active = True
            slot.owner = owner
            return AcquireResult(True)

    def release(self, *, resource_group: str, owner: str) -> None:
        slot = self._get_slot(resource_group)
        with slot.condition:
            if not slot.active:
                return
            if slot.owner != owner:
                return
            slot.active = False
            slot.owner = None
            slot.condition.notify_all()

    @contextmanager
    def hold_sync(
        self,
        *,
        resource_group: str,
        owner: str,
        wait_policy: WaitPolicy,
        stop_event: Optional[threading.Event] = None,
        on_wait: Optional[Callable[[], None]] = None,
    ) -> Iterator[AcquireResult]:
        result = self.acquire_sync(
            resource_group=resource_group,
            owner=owner,
            wait_policy=wait_policy,
            stop_event=stop_event,
            on_wait=on_wait,
        )
        try:
            yield result
        finally:
            if result.acquired:
                self.release(resource_group=resource_group, owner=owner)


tool_invocation_coordinator = ToolInvocationCoordinator()
