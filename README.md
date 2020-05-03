# ASM2BF
## ASM2BF - Assembly to Brainfuck, is a project dedicated to proving once and for all that *you can* program anything with Brainfuck

### What can this project do?
Currently, we can convert some basic MIPS commands into Brainfuck code that actually runs.
The whole MIPS instruction set we used as reference can be found [here](http://www.mrc.uidaho.edu/mrc/people/jff/digital/MIPSir.html).

### What are the setbacks?
The Brainfuck code we give as output is BIG, and doesn't support all MIPS command.
The full list of MIPS commands we support can be found in [MIPS_instruction_set](constants/MIPS_instruction_set.py).

### How do I use it?
This will most likely run "forever":\
Make sure you have bfi

    pip install bfi
then run

    python main.py <input_ASM_file> 
Or (and recommended): hook into our code and call the functions in converters/main_converter.py\
You'll probably get a memory error. To solve this, you're gonna have to deal with less MIPS functions.
This can be done by changing the variable PATTERNS in converters/ASM2HBF, and reducing the number of key-value pairs.

### How does it roughly work?
In some sense, we simulate a CPU.\
There are two parts to the output Brainfuck code:
1. The first part of the brainfuck code writes the MIPS commands into the brainfuck memory segment.
2. The second part reads the MIPS command written in step 1 and runs them.

### How does it work, in detail?
#### Creating HBF
We developed a compiler of some sort, from HBF to BF.
- HBF - High Brainfuck, a language we invented
- BF - Brainfuck

Inventing the language and building the compiler were two operations that happened together.
We saw what function we would like to have, and added it to the compiler.\
We started out by abstracting the Brainfuck memory segment, and treating it as an array of matrices of cells instead of a simple array of cells.
The commands added were (up), (down), (left), and (right):
- (up) - When seeing this command, the compiler will replace it with a > 
- (down) - When seeing this command, the compiler will replace it with a <
- (left) - When seeing this command, the compiler will replace it with a >*[height of matrix]
- (right) - When seeing this command, the compiler will replace it with a <*[height of matrix]
- \> - When seeing this command, the compiler will replace it with a >\*[height of matrix]*[width of matrix]
- \< - When seeing this command, the compiler will replace it with a <\*[height of matrix]*[width of matrix]

So the origin of the matrix is the bottom-right cell, and then we continue upwards, drifting into the next column. Yeah, bottom-right. Not standard. Deal with it.\
\
From there, we continued to decide what the values in the matrix will hold:
- In the right most column, we hold the "value" of the current matrix which is the actual number we want to hold
- In column 2, the next one to the left, we hold the if column, used for ifs
- In column 3, we hold temporary values
- In column 4, we hold all the flags we might need
- In column 5, we hold the save\load data, when we want to copy the information in the current column so that we can edit it without worrying about keeping it.

Notice we decided at an early stage we were going to work with binary, so each cell in the matrix holds either 0 or 1 (except for a very specific edge case, which we don't go into in this explanation).\
We added functions as needed, until we got a sufficiently complicated language. All functions, after passing through the compiler, are turned into the 8 basic Brainfuck commands.

#### Converting the assembly code
Once we had a language (HBF) complex enough to work with, we started the conversion of MIPS to this language.\
This has 2 parts - initialising the memory segment, and running the ASM code saved in memory:
- Initialising the memory segment:\
We first wrote some code (in python) that takes some compiled ASM code as input, and outputs the BF code that writes this ASM code to the Brainfuck memory.
In this BF code we first initialise some flags, including the register flag, code segment, ALU, etc.
Once done with that, we also write the ASM code to the Brainfuck memory segment, in the same binary format it came in.
- Running the ASM code saved in memory:\
We build a big loop in HBF, that runs so long as we are still in the code segment we initialised.
In this loop, for every command we encounter, we check if it is of type a. If it is, we run command a; if isn't we continue on to command b and so on.
Once done with all commands, we increment the instruction pointer - which in our case means moving the "ip" flag.\
Notice this part is not dependent on the input ASM code

Once we create these two bits of HBF code, we connect them together and send them to the HBF to BF compiler.\
The output code we get is in pure Brainfuck and does the same calculation as the original MIPS code.

### Why is it built this way?
The main setback with the Brainfuck language is that we have minimal control over the instruction pointer.
This led us to believe the only way we could allow true control over which command we run, including the JMP command, is by saving these commands to the Brainfuck memory segment.
