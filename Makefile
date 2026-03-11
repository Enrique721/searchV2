
SRC_MAIN_REGISTER := src/cadastro.py
SRC_MAIN_SEARCH := src/cli_consulta.py

REGISTER_BINARY_NAME=cadastro
SEARCH_BIANRY_NAME=cli_consulta

REGISTER_BINARY := dist/$(REGISTER_BINARY_NAME)
SEARCH_BINARY := dist/$(SEARCH_BINARY_NAME)

INSTALL_DIRECTORY := ~/.local/bin

$(REGISTER_BINARY): $(SRC_MAIN_REGISTER)
	../venv/bin/pyinstaller --onefile $(SRC_MAIN_REGISTER)

$(SEARCH_BINARY): $(SRC_MAIN_SEARCH)
	../venv/bin/pyinstaller --onefile $(SRC_MAIN_SEARCH)

run-clean-register: clean $(REGISTER_BINARY)
	./$(REGISTER_BINARY)
	
run-register: $(REGISTER_BINARY)
	./$(REGISTER_BINARY)

run-search: $(SEARCH_BINARY)
	./$(SEARCH_BINARY)
	
install-register: $(REGISTER_BINARY)
	mv $(REGISTER_BINARY) ~/.local/bin/

install: $(REGISTER_BINARY) $(REGISTER_SEARCH)
	mv dist/cadastro 

uninstall:
	@if [ -e "$(INSTALL_DIRECTORY)/$(SEARCH_BINARY_NAME)" ] || \
	     [ -e "$(INSTALL_DIRECTORY)/$(REGISTER_BINARY_NAME)" ]; then \
	    echo "Removing installed binaries..."; \
	    rm -f "$(INSTALL_DIRECTORY)/$(SEARCH_BINARY_NAME)" \
	          "$(INSTALL_DIRECTORY)/$(REGISTER_BINARY_NAME)"; \
	else \
	    echo "No installed binaries found."; \
	fi

clean:
	rm -rf dist build

.phony: run-register run-search install
