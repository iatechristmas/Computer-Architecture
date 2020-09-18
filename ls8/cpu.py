"""CPU functionality."""

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100


import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # memory 
        self.ram = [0] * 256
        # instruction register

        self.registers = [0] * 8

        # program counter
        self.pc = 0

        self.running = False

        self.branch_table = {}
        self.branch_table[HLT] = self.HLT
        self.branch_table[LDI] = self.LDI
        self.branch_table[PRN] = self.PRN
        self.branch_table[ADD] = self.ADD
        self.branch_table[SUB] = self.SUB
        self.branch_table[MUL] = self.MUL
        self.branch_table[PUSH] = self.PUSH
        self.branch_table[POP] = self.POP
        
        self.branch_table[CMP] = self.CMP
        self.branch_table[JMP] = self.JMP
        self.branch_table[JNE] = self.JNE
        self.branch_table[JEQ] = self.JEQ

        self.branch_table[AND] = self.AND
        self.branch_table[OR] = self.OR
        self.branch_table[XOR] = self.XOR
        self.branch_table[NOT] = self.NOT
        self.branch_table[SHL] = self.SHL
        self.branch_table[SHR] = self.SHR
        self.branch_table[MOD] = self.MOD

        self.stack_pointer = 7

        self.registers[self.stack_pointer] = 0xF4 # initialize stack pointer

        self.fl = 0

        
    def ram_read(self, address):
        # # if self.ir == 0:
        #     operand_1 = self.memory[self.pc + 1]
        #     operand_2 = self.memory[self.pc + 2]
        #     self.pc += 2
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    
    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #         self.ram[address] = instruction
        #         address += 1

        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        try:

            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        # base 2 as second argument
                        n = int(n, 2)

                    except ValueError:
                        print(f"Invalid number '{n}'")

                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]

        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]

        elif op == "CMP":
            if self.registers[reg_a] == self.registers[reg_b]:
                self.fl = 0b00000001
            if self.registers[reg_a] > self.registers[reg_b]:
                self.fl = 0b00000010
            if self.registers[reg_a] < self.registers[reg_b]:
                self.fl = 0b00000100
        
        elif op == "AND":
            self.registers[reg_a] &= self.registers[reg_b]

        elif op == "OR":
            self.registers[reg_a] |= self.registers[reg_b]

        elif op == "XOR":
            self.registers[reg_a] ^= self.registers[reg_b]

        elif op == "NOT":
            self.registers[reg_a] = ~self.registers[reg_b]

        elif op == "SHL":
            self.registers[reg_a] <<= self.registers[reg_b]

        elif op == "SHR":
            self.registers[reg_a] >>= self.registers[reg_b]

        elif op == "MOD":
            self.registers[reg_a] %= self.registers[reg_b]

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
        self.running = True
        while self.running:
            ir = self.ram[self.pc]  # Instruction Register, copy of the currently-executing instruction

            if ir in self.branch_table:
                self.branch_table[ir]()

            else:
                print(f"Unknown instruction {ir}")
    #         operand_a = self.ram_read(self.pc + 1)
    #         operand_b = self.ram_read(self.pc + 2)

    #         if ir == 0b00000001:  # HLT
    #             self.HLT()

    #         elif ir == 0b10000010: # LDI
    #             self.LDI()

    #         elif ir == 0b01000111:  # PRN
    #             self.PRN()

    #         elif ir == 0b10100010:  # MUL
    #             self.alu("MUL", operand_a, operand_b)

    #         else:

    # def helper_function(self, operation_string):
    #     reg_a = self.ram[self.pc + 1]
    #     reg_b = self.ram[self.pc + 2]
        
    #     self.alu(operation_string, reg_a, reg_b)

    #     self.pc += 3

    def MOD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("MOD", reg_a, reg_b)

        self.pc += 3

    def SHR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("SHR", reg_a, reg_b)

        self.pc += 3

    def SHL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("SHL", reg_a, reg_b)

        self.pc += 3

    def NOT(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("NOT", reg_a, reg_b)

        self.pc += 3

    def XOR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("XOR", reg_a, reg_b)

        self.pc += 3

    def OR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("OR", reg_a, reg_b)

        self.pc += 3

    def AND(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("AND", reg_a, reg_b)

        self.pc += 3

    def JEQ(self):
        if self.fl == 0b00000001:
            self.pc = self.registers[self.ram_read(self.pc + 1)]
        else:
            self.pc += 2

    def JNE(self):
        if self.fl != 0b00000001:
            self.pc = self.registers[self.ram_read(self.pc + 1)]
        else:
            self.pc += 2

    def JMP(self):
        self.pc = self.registers[self.ram_read(self.pc + 1)]

    def CMP(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("CMP", reg_a, reg_b)

        self.pc += 3    

    def PUSH(self):
        self.registers[self.stack_pointer] -= 1
        reg_num = self.ram[self.pc + 1]
        value = self.registers[reg_num]
        top_of_stack_addr = self.registers[self.stack_pointer]
        self.ram[top_of_stack_addr] = value

        self.pc += 2

    def POP(self):
        reg_num = self.ram[self.pc + 1]
        top_of_stack_addr = self.registers[self.stack_pointer]
        value = self.ram[top_of_stack_addr]
        self.registers[reg_num] = value
        self.registers[self.stack_pointer] += 1    

        self.pc += 2

    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("ADD", reg_a, reg_b)

        self.pc += 3
        
    def SUB(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("SUB", reg_a, reg_b)

        self.pc += 3

    def MUL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]

        self.alu("MUL", reg_a, reg_b)

        self.pc += 3

    def HLT(self):
        self.running = False

    def LDI(self):
        reg_num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.registers[reg_num] = value

        self.pc += 3

    def PRN(self):
        reg_num = self.ram[self.pc + 1]
        print(self.registers[reg_num])

        self.pc += 2

