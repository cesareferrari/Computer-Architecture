"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 8
        self.pc = 0
        self.reg = [None] * 8

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
            command = self.ram[self.pc]

            if command == 0b10000010: # LDI R0,8
                # put 8 in register 0
                register_index = self.ram[self.pc + 1]
                number_to_save = self.ram[self.pc + 2]
                self.reg[register_index] = number_to_save
                self.pc += 3

            if command == int(0b01000111): # PRN R0
                # print register 0
                register_index = self.ram[self.pc + 1]
                print(self.reg[register_index])
                self.pc += 2
            
            if command == int(0b00000001): # HLT
                running = False

