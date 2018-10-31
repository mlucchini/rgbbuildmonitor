.DEFAULT_GOAL := copy

.user    := pi
.machine := 192.168.69.67
.dir     := ws/buildmonitor

help:
	@echo ""
	@echo "Available commands :"
	@echo ""
	@echo "  make \t\t\tcopies current directory"
	@echo "  make copy\t\tcopies current directory"
	@echo "  make install\t\tcopies current directory and installs dependencies"
	@echo ""

copy:
	rsync -r ./* $(.user)@$(.machine):~/$(.dir)

install: copy
	ssh $(.user)@$(.machine) " \
	pip3 install -r $(.dir)/requirements.txt"

.PHONY: copy install
