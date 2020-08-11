"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.reg = [None] * 8
        # pc: program counter
        self.pc = 0

        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010

    # accept the address to read and return the value stored there
    # mar: Memory address register, the address that is being read
    def ram_read(self, mar):
        return self.ram[mar]

    # accept a value to write, and the address to write it to.
    # mar: Memory address register, the address that is being read
    # mdr: Memory data register, the data that is being written
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # R0
            0b00001000, # 8
            0b01000111, # PRN R0
            0b00000000, # R0
            0b10000010, # LDI R1,9
            0b00000001,
            0b00001001,
            0b10100010, # MUL R0,R1
            0b00000000,
            0b00000001,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True


        while running:
            # ir: instruction register
            ir = self.ram_read(self.pc)
            num_operands = ir >> 6  # extract # of operands

            if ir == self.LDI: # LDI R0,8
                # put 8 in register 0
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b

            if ir == self.PRN: # PRN R0
                # print register 0
                operand_a = self.ram_read(self.pc + 1)
                print(self.reg[operand_a])

            if ir == self.MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] *= self.reg[operand_b]
            
            # if ir == int(0b00000001): # HLT
            if ir == self.HLT:
                running = False

            self.pc += num_operands + 1  # + 1 for the command itself

