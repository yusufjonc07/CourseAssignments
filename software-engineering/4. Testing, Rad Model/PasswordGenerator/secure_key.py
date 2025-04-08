import random
import string
from pydantic import Field, BaseModel

class PasswordGenerator(BaseModel):
    
    num_upper: int = Field(4, gt=0, lt=5)
    num_lower: int = Field(4, gt=0, lt=5)
    num_digits: int = Field(3, gt=0, lt=5)
    num_symbols: int = Field(2, gt=0, lt=5) 
    
    def get(self):
        upper_chars = random.choices(
            string.ascii_uppercase, k=self.num_upper
        )
        lower_chars = random.choices(
            string.ascii_lowercase, k=self.num_lower
        )
        digit_chars = random.choices(
            string.digits, k=self.num_digits
        )
        symbol_chars = random.choices(
            string.punctuation, k=self.num_symbols
        )

        password_list = upper_chars + lower_chars + digit_chars + symbol_chars
        
        random.shuffle(password_list)
        return ''.join(password_list)
