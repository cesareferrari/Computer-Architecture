Operation       Boolean      Bitwise
AND                 &&          &


    0b10000011
&   0b01010101
    ----------
    0b00000001



ADD instruction

ADD = 0b10100000 
num_operands = ADD >> 6 # result 0b10 == 2

# is_alu_operation = ADD >> 5  # result: 0b101
# 0b101 & 0b001 # result: 0b1

is_alu_operation = (ADD >> 5) & 0b001  # result 0b1

pc += num_operands + 1

