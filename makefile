VERSION=0.1.0

build:
	docker build -t ufpa-sd-tiktaktoe:${VERSION} .

create:
	docker run --rm -it --net host ufpa-sd-tiktaktoe:${VERSION}

join:
	docker run --rm -it --net host ufpa-sd-tiktaktoe:${VERSION} -j $(UUID)
