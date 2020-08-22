import random
import hashlib

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
