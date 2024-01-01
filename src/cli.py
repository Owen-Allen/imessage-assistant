import argparse
import re

class ArgParseWrapper:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='A chat script that responds to texts using Chat GPT')
        self._setup_arguments()

    def _setup_arguments(self):
        # Phone number argument
        self.parser.add_argument('-phone', type=self.format_and_validate_phone_number,
                                 help='Phone number in 9-digit format or +1 followed by 9 digits')

        # Safe mode flag
        self.parser.add_argument('--safe-mode', action='store_true',
                                 help='Enable safe mode')

    def parse_args(self):
        return self.parser.parse_args()

    @staticmethod
    def format_and_validate_phone_number(phone_number):
        phone_number = ArgParseWrapper.format_phone_number(phone_number)
        phone_number = ArgParseWrapper.validate_phone_number(phone_number)
        return phone_number

    @staticmethod
    def format_phone_number(phone_number):
        if(not phone_number.startswith('+1')):
            phone_number = "+1" + phone_number
        return phone_number

    @staticmethod
    def validate_phone_number(phone_number):
        # Validate the phone number format
        pattern = r'\+1\d{10}$'
        if not re.match(pattern, phone_number):
            raise argparse.ArgumentTypeError("Phone number must be in the 9-digit format or +1 followed by 9 digits.")
        return phone_number
    

def main():
    parser = ArgParseWrapper()
    args = parser.parse_args()

    print(f"Phone number: {args.phone}")
    if args.safe_mode:
        print("Safe mode is enabled")

if __name__ == "__main__":
    main()