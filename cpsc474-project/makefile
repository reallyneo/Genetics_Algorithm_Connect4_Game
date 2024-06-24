# Define compiler and flags
CC = python3
CFLAGS = -m

# Define source files
SRC = connect4.py

# Define target names
TARGET = connect4

# Define phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Rule to build the target
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $< -o $@

# Rule to clean the build files
clean:
	rm -f $(TARGET)