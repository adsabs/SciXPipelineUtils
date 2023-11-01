"""
Pulled from prototype code:
https://github.com/uuid6/prototypes/commit/475ad927455a2d35aaade518a1928aec93d78a5c
"""

import random
import time
import uuid


class scix_uuid:
    def uuid7():
        """Generates a 128-bit version 7 UUID with nanoseconds precision timestamp and random node

        example: 061cdd23-93a0-73df-a200-6ff3e72d92e9

        format: unixts|subsec_a|version|subsec_b|variant|subsec_seq_node

        :return: uuid.UUID
        """

        sequenceCounter = 0
        _last_v7timestamp = 0
        uuidVariant = "10"

        uuidVersion = "0111"  # ver 7
        sec_bits = 36  # unixts at second precision
        subsec_bits = 30  # Enough to represent NS
        version_bits = 4  # '0111' for ver 7
        variant_bits = 2  # '10' Static for UUID
        sequence_bits = 8  # Enough for 256 UUIDs per NS
        node_bits = (
            128 - sec_bits - subsec_bits - version_bits - variant_bits - sequence_bits
        )  # 48

        ### Timestamp Work
        # Produces unix epoch with nanosecond precision
        timestamp = time.time_ns()  # Produces 64-bit NS timestamp
        # Subsecond Math
        subsec_decimal_digits = 9  # Last 9 digits of are subsection precision
        subsec_decimal_divisor = 10**subsec_decimal_digits  # 1000000000 NS in 1 second
        integer_part = int(timestamp / subsec_decimal_divisor)  # Get seconds
        sec = integer_part
        # Conversion to decimal
        fractional_part = round(
            (timestamp % subsec_decimal_divisor) / subsec_decimal_divisor, subsec_decimal_digits
        )
        subsec = round(fractional_part * (2**subsec_bits))  # Convert to 30 bit int, round

        ### Binary Conversions
        ### Need subsec_a (12 bits), subsec_b (12-bits), and subsec_c (leftover bits starting subsec_seq_node)
        unixts = f"{sec:036b}"
        subsec_binary = f"{subsec:030b}"
        subsec_a = subsec_binary[:12]  # Upper 12
        subsec_b_c = subsec_binary[-18:]  # Lower 18
        subsec_b = subsec_b_c[:12]  # Upper 12
        subsec_c = subsec_binary[-6:]  # Lower 6

        ### Sequence Work
        # Sequence starts at 0, increments if timestamp is the same, the sequence increments by 1
        # Resets if timestamp int is larger than _last_v7timestamp used for UUID generation
        # Will be 8 bits for NS timestamp
        if timestamp <= _last_v7timestamp:
            sequenceCounter = int(sequenceCounter) + 1

        if timestamp > _last_v7timestamp:
            sequenceCounter = 0

        sequenceCounterBin = f"{sequenceCounter:08b}"

        # Set these two before moving on
        _last_v7timestamp = timestamp

        ### Random Node Work
        randomInt = random.getrandbits(node_bits)
        randomBinary = f"{randomInt:048b}"

        # Create subsec_seq_node
        subsec_seq_node = subsec_c + sequenceCounterBin + randomBinary

        ### Formatting Work
        # Bin merge and Int creation
        UUIDv7_bin = unixts + subsec_a + uuidVersion + subsec_b + uuidVariant + subsec_seq_node
        UUIDv7_int = int(UUIDv7_bin, 2)

        # Convert Hex to Int then splice in dashes
        UUIDv7_hex = f"{UUIDv7_int:032x}"  # int to hex
        UUIDv7_formatted = "-".join(
            [
                UUIDv7_hex[:8],
                UUIDv7_hex[8:12],
                UUIDv7_hex[12:16],
                UUIDv7_hex[16:20],
                UUIDv7_hex[20:32],
            ]
        )

        return uuid.UUID(UUIDv7_formatted)

"""
This loops through all the uuid attributes and adds them to the scix_uuid class so they are accessible
and scix_uuid can be treated as a drop-in replacement for uuid.
"""
for i in dir(uuid):
    setattr(scix_uuid, i, getattr(uuid, i))
