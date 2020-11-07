import random
import hashlib
import math

class CommonController:
    """
    Generates an id
    """
    @classmethod
    def generate_id(self, base_str = ""):
        h = str(base_str) + str(random.randint(100000, 999999))
        h = hashlib.sha1(h.encode("utf-8"))
        return h.hexdigest()


    """
    Extracts an integer or returns default
    """
    @classmethod
    def extract_integer_or(self, value, default = 1):
        if isinstance(value, int):
            return value
        matches = re.match(r"^\d+", value)
        if not matches:
            return int(default)
        else:
            return int(matches.group())
    

    """
    Formats a number of seconds to the [00:]00:00 format
    """
    @classmethod
    def format_duration(self, duration):
        duration = round(duration)
        seconds = duration % 60
        minutes = math.floor(duration / 60) % 60
        output = "%02d:%02d" % (minutes, seconds)
        hours = math.floor(duration / 3600)
        if hours:
            output = "%2d:%s" % (hours, output)
        return output

