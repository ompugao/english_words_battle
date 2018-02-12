NAME=ewb
TEST_NAME=test_ewb
VERSION=latest
PWD=`pwd`

build:
	docker build -t $(NAME):$(VERSION) .

restart: stop start

start:
	docker run -itd --rm \
		--name $(NAME) \
		-v $(PWD)/config:/ewb/src/config \
		$(NAME):$(VERSION) \
		/bin/bash -c "cd /ewb/src; python main.py"


contener=`docker ps -a -q`
image=`docker images | awk '/^<none>/ { print $$3 }'`

clean:
	@if [ "$(image)" != "" ] ; then \
		docker rmi $(image); \
	fi
	@if [ "$(contener)" != "" ] ; then \
		docker rm $(contener); \
	fi

stop:
	docker rm -f $(NAME)

attach:
	docker exec -it $(NAME) /bin/bash

logs:
	docker logs -f $(NAME)

test: build
	docker run -it --rm \
		--name $(TEST_NAME) \
		-v $(PWD)/config:/ewb/src/config \
		-v $(PWD)/tests:/ewb/tests \
		$(NAME):$(VERSION) \
		/bin/bash -c "cd /ewb; pytest"
