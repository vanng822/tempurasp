OS := $(shell uname)
tag := $(shell cat VERSION)
name := tempurasp
image_tag := $(name):$(tag)

ifeq ($(OS),Darwin)
DOCKER := docker
CPU_TEMP := $(shell pwd)/fake_cpu_temp
GPU_TEMP := $(shell pwd)/fake_gpu_temp
else
DOCKER := sudo docker
CPU_TEMP := /sys/class/thermal/thermal_zone0/temp
GPU_TEMP := /tmp/gpu_temp
endif

build:
	$(DOCKER) build -t $(image_tag) .

run:
	$(DOCKER) run --restart=always --network raspberrypi3_default \
		-v $(CPU_TEMP):/cpu_temp \
		-v $(GPU_TEMP):/gpu_temp \
	 	--ip 172.18.0.6 --name $(name) -d -it $(image_tag)

stop:
	$(DOCKER) stop $(name)

rm:
	$(DOCKER) rm $(name)

deploy:
	make stop
	make rm
	make run
