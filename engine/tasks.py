"""
Background task loop for Auto-Pilot mode
"""
import asyncio
import time
import threading
from typing import Callable, Optional

from .utils import log


class TaskLoop:
    """Background task loop for periodic execution"""
    
    def __init__(self, interval_s: int = 15):
        """
        Initialize task loop
        
        Args:
            interval_s: Interval between runs in seconds
        """
        self.interval_s = interval_s
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_run = 0
        self._lock = threading.Lock()
    
    def start(self, coro: Callable):
        """
        Start the background loop
        
        Args:
            coro: Async coroutine to run periodically
        """
        with self._lock:
            if self._running:
                log.warning("TaskLoop already running")
                return
            
            self._running = True
            self._thread = threading.Thread(
                target=self._run_loop,
                args=(coro,),
                daemon=True
            )
            self._thread.start()
            log.info(f"TaskLoop started (interval={self.interval_s}s)")
    
    def stop(self):
        """Stop the background loop"""
        with self._lock:
            if not self._running:
                return
            
            self._running = False
            log.info("TaskLoop stopped")
    
    def _run_loop(self, coro: Callable):
        """Internal loop runner"""
        while self._running:
            try:
                current_time = time.time()
                
                # Check if enough time has passed
                if current_time - self._last_run >= self.interval_s:
                    # Run the coroutine
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(coro())
                        loop.close()
                        self._last_run = current_time
                    except Exception as e:
                        log.error(f"TaskLoop execution error: {e}")
                
                # Sleep briefly
                time.sleep(1)
                
            except Exception as e:
                log.error(f"TaskLoop error: {e}")
                time.sleep(5)
    
    @property
    def is_running(self) -> bool:
        """Check if loop is running"""
        return self._running
