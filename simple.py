import sys

PRINT_TIM      =  0b00000001
HALT           =  0b00000010
PRINT_NUM      =  0b01000011  # command 3
SAVE           =  0b10000100
PRINT_REGISTER =  0b01000101
ADD            =  0b10000110  # command 6
PUSH           =  0b01000111  # 1 operand, command 7
POP            =  0b01001000  # 1 operand, command 7


# Rules of our game
## we store everything in memory
## we move our PC to step through memory, and execute commands

memory = [None] * 256

running = True
pc = 0

def load_program():
    address = 0

    try:
        with open(sys.argv[1]) as file:
            for line in file:
                comment_split = line.split("#")
                possible_num = comment_split[0]

                if possible_num == '':
                    continue

                if possible_num[0] == '1' or possible_num[0] == '0':
                    num = possible_num[:8]
                    print(f'{num}: {int(num, 2)}') # integer base 2

                    memory[address] = int(num, 2)
                    address += 1

    except FileNotFoundError:
        print(f"{sys.argv[0]}: {sys.argv[1]} not found")

load_program()

# save the number 42 into R2
# what arguments does SAVE require?

# registers (use as variables)
# R0-R7
registers = [None] * 8
registers[7] = 0xF4

while running:

    command = memory[pc]
    num_operands = command >> 6

    if command == PRINT_TIM:
        print("Tim!")

    if command == PRINT_NUM:
        number_to_print = memory[pc + 1]
        print(number_to_print)

    if command == SAVE:
        num = memory[pc + 1]
        index = memory[pc + 2]
        registers[index] = num

    if command == PRINT_REGISTER:
        reg_idx = memory[pc + 1]
        print(registers[reg_idx])

    if command == ADD:
        reg1_idx = memory[pc + 1]
        reg2_idx = memory[pc + 2]

        registers[reg1_idx] += registers[reg2_idx]

    if command == PUSH:
        # decrement stack pointer
        registers[7] -= 1
        # look ahead in memory to get register number
        register_number = memory[pc + 1]
        # get value from register
        number_to_push = registers[register_number]
        # copy into stack
        sp = registers[7]
        memory[sp] = number_to_push

    if command == POP:
        sp = registers[7]
        # get value of last position of sp
        popped_value = memory[sp]
        # get register number
        register_number = memory[pc + 1]
        # copy into a register
        registers[register_number] = popped_value
        # increment sp
        registers[7] += 1


    if command == HALT:
        running = False

    pc += num_operands + 1   # + 1 for the command itself
