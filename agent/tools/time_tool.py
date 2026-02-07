"""Time utility tools"""
from datetime import datetime
import time


class TimeTool:
    """Time-related utilities"""

    @staticmethod
    def get_current_time():
        """Get current time in formatted string"""
        now = datetime.now()
        # Format: "2026-02-06 19:45 (Friday)"
        day_name = now.strftime("%A")
        formatted_time = now.strftime("%Y-%m-%d %H:%M")
        return f"{formatted_time} ({day_name})"

    @staticmethod
    def get_current_datetime():
        """Get current datetime with more details"""
        now = datetime.now()
        return {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
            "timestamp": now.timestamp(),
            "formatted": TimeTool.get_current_time()
        }

    @staticmethod
    def get_time_info():
        """Get comprehensive time information"""
        now = datetime.now()
        info = {
            "current_time": TimeTool.get_current_time(),
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "weekday": now.strftime("%A"),
            "week_number": now.isocalendar()[1],
            "day_of_year": now.timetuple().tm_yday,
            "is_dst": time.daylight
        }
        return info

    @staticmethod
    def format_time(timestamp=None):
        """Format a timestamp or current time"""
        if timestamp is None:
            dt = datetime.now()
        else:
            dt = datetime.fromtimestamp(timestamp)
        
        day_name = dt.strftime("%A")
        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        return f"{formatted} ({day_name})"
