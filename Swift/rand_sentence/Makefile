SWIFTC=xcrun -sdk macosx swiftc 
SOURCE=main.swift

randomSentences:$(SOURCE)
	$(SWIFTC) $(SOURCE) -o $@
	cp -f $@ ../bin/$@
