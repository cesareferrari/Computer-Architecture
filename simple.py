PRINT_TIM      =  0b00000001
HALT           =  0b00000010
PRINT_NUM      =  0b01000011  # command 3
SAVE           =  0b10000100
PRINT_REGISTER =  0b01000101
ADD            =  0b10000110  # command 6


# Rules of our game
## we store everything in memory
## we move our PC to step through memory, and execute commands

memory = [
    PRINT_TIM, 
    PRINT_TIM,
    PRINT_NUM,
    99,
    SAVE, 
    42,  # number to save
    2,   # register to save into R2
    SAVE, 
    42,  # number to save
    3,   # register to save into R3
    ADD, # R2 + R3 and save in R2
    2,   # register index
    3,   # register index
    PRINT_REGISTER,
    2,
    HALT,       # <--- PC
          ]

running = True
pc = 0

# save the number 42 into R2
# what arguments does SAVE require?

# registers (use as variables)
# R0-R7
registers = [None] * 8

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

    if command == HALT:
        running = False

    pc += num_operands + 1   # + 1 for the command itself