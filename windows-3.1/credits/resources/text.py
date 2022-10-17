
from nefile.resource_table import ResourceType

## Models one "section" of credits from the Windows 3.1 credits screen.
##
## The section header scrolls upward from the bottom and stays persistent
## at the top of the credits screen while each of the lines in the 
## section content scroll upward beneath it.
##
## When all of the section lines have scrolled off the screen, the section
## header clears and the next section header begins scrolling upward.
class CreditsSection:
    def __init__(self, section_header_bytes, section_content_bytes):
        self.section_header = CreditLines(section_header_bytes)
        self.section_content = CreditLines(section_content_bytes)

## Models one or more text lines that are displayed sequentially in the 
## Windows 3.1 credits screen.
class CreditLines:
    def __init__(self, byte_string):
        if len(byte_string) == 0:
            return 

        # The first byte is an ID that uniquely identifies this set of lines
        # in the credits screen.
        self.id: int = byte_string[0]
        # A line break is encoded as a forward slash (/).
        # Each ASCII-decoded line is stored in its own list entry.
        encoded_lines = byte_string[1:].split(b'/')
        self.lines = [line.decode('ascii') for line in encoded_lines]

## Models the text of the credits from the Windows 3.1 credits screen.
class Windows31CreditsText:
    def __init__(self, shell_dll):
        # DECRYPT THE CREDITS DATA.
        CREDITS_TEXT_XOR_ENCRYPTION_KEY: int = 0x99
        xor_encrypted_credits: bytes = shell_dll.resource_table.resources[ResourceType.RT_RCDATA][9999].data.read()
        decrypted_credits: bytes = bytes([xored_byte ^ CREDITS_TEXT_XOR_ENCRYPTION_KEY for xored_byte in xor_encrypted_credits])
        credits_sections_bytes = decrypted_credits[1:].split(b'\x99')

        # READ THE DEDICATION MESSAGE.
        self.dedication_message = [CreditLines(line) for line in credits_sections_bytes[0:3]]

        # READ THE MAIN CREDITS.
        credits_sections_two_at_a_time = zip(*[iter(credits_sections_bytes[3:])] * 2)
        self.credits_sections = []
        for section_header, section_content in credits_sections_two_at_a_time:
            credits_section = CreditsSection(section_header, section_content)
            self.credits_sections.append(credits_section)