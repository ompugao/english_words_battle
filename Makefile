NAME=ewb
TEST_NAME=test_ewb
VERSION=latest
PWD=`pwd`

.PHONY: build
build:
	docker build -t $(NAME):$(VERSION) .

.PHONY: restart
restart: stop start

.PHONY: start
start:
	docker run -itd --rm \
		--name $(NAME) \
		-v $(PWD)/config:/ewb/src/config \
		$(NAME):$(VERSION) \
		/bin/bash -c "cd /ewb/src; python main.py"


container=`docker ps -a -q`
image=`docker images | awk '/^<none>/ { print $$3 }'`

.PHONY: clean
clean:
	@if [ "$(image)" != "" ] ; then \
		docker rmi $(image); \
	fi
	@if [ "$(container)" != "" ] ; then \
		docker rm $(container); \
	fi

.PHONY: stop
stop:
	docker rm -f $(NAME)

.PHONY: attach
attach:
	docker exec -it $(NAME) /bin/bash

.PHONY: logs
logs:
	docker logs -f $(NAME)

.PHONY: test
test: build
	docker run -it --rm \
		--name $(TEST_NAME) \
		-v $(PWD)/config:/ewb/src/config \
		-v $(PWD)/tests:/ewb/tests \
		$(NAME):$(VERSION) \
		/bin/bash -c "cd /ewb; pytest"
