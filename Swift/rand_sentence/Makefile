SWIFTC=xcrun -sdk macosx swiftc
FLAGS=''
SOURCE=main.swift

randomSentences:$(SOURCE)
	@echo "Compiling $@..."
	@$(SWIFTC) $(FLAGS) $(SOURCE) -o $@ && \
	 echo "Copy executable to $$(realpath ../bin/$@)" && \
	 cp -f $@ ../bin/$@
	@make clean

clean:
	@echo "Clean up..." && \
	 rm -f randomSentences && \
	 echo "Cleaning sucess."
