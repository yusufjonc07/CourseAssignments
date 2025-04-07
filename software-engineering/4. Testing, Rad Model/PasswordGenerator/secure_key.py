import random
import string
from pydantic import Field, BaseModel

SHOULD = "should be between 1 and 5"

class PasswordGenerator(BaseModel):
    
    num_upper: int = Field(4, gt=0, lt=5, description=f"Number of upper-case letters {SHOULD}")
    num_lower: int = Field(4, gt=0, lt=5, description=f"Number of lower-case letters {SHOULD}")
    num_digits: int = Field(3, gt=0, lt=5, description=f"Number of digits {SHOULD}")
    num_symbols: int = Field(2, gt=0, lt=5, description=f"Number of other keyboard characters {SHOULD}") 
    
    def get(self):
        upper_chars = random.choices(string.ascii_uppercase, k=self.num_upper)
        lower_chars = random.choices(string.ascii_lowercase, k=self.num_lower)
        digit_chars = random.choices(string.digits, k=self.num_digits)
        symbol_chars = random.choices(string.punctuation, k=self.num_symbols)

        password_list = upper_chars + lower_chars + digit_chars + symbol_chars
        
        random.shuffle(password_list)
        return ''.join(password_list)


passwd_gen = PasswordGenerator()

# with default
print(passwd_gen.get())