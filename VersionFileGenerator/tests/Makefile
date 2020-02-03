BUILD_DIR = ./build

CFLAGS = \
	-Wall \
	-Wextra \
	-Wpedantic

OPTIMIZATION = -O0

INCLUDES = -I.

SOURCES = \
	version.c \
	main.c

OBJECTS = $(addprefix $(BUILD_DIR)/,$(notdir $(SOURCES:.c=.o)))
vpath %.c $(sort $(dir $(SOURCES)))

$(BUILD_DIR)/%.o: %.c $(BUILD_DIR)
	@echo "Building $<"
	gcc -c $(CFLAGS) $(INCLUDES) $< -o $@

$(BUILD_DIR)/main.exe: $(OBJECTS) Makefile
	@echo "Creating $@"
	gcc $(OBJECTS) -o $@

$(BUILD_DIR):
	@echo "Building build directory"
	@mkdir -p $@

clean:
	@echo "Removing build directory"
	@rm -rf $(BUILD_DIR)

run:
	$(BUILD_DIR)/main.exe
