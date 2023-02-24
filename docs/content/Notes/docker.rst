Docker your applications
=========================




Installation
^^^^^^^^^^^^

Install Docker Desktop on MAC or WINDOWS. 

For MAC, simply drag the docker.app to Application folder is not enough, you have to click and run the app so that the ``docker`` will be added to the system bin.

For WINDOWS, you need restart computer, just follow the installation prompts.


Push
^^^^^^



https://stackoverflow.com/questions/41984399/denied-requested-access-to-the-resource-is-denied-docker


::
	
	docker images

	docker login

	docker tag firstimage YOUR_DOCKERHUB_NAME/firstimage


	docker push YOUR_DOCKERHUB_NAME/firstimage



	docker exec test /bin/sh -c "ls data"

	docker exec -i test bash < run.sh

Ways to use existing docker as a test
^^^^^^^^^^^^^^^^^^^^^^

I have my previous easy-prime docker. It is for prime editing. But users come to me a lot for just sgRNA design. I modified my code a little bit and I don't want to build a docker image from scratch. This is how I test my code and build new image:


::
	
	# First, create a testing container to test my code, my easy-prime will always use 80, so I have to create a new port. The resulting new link is: http://127.0.0.1:90/
	docker container create -p 80:80 -p 90:90 -v /e/Docker/easy_gRNA_design:/app2 --name tmp3 liyc1989/easy_prime
	# I can then using docker desktop to open a terminal, go to app2 and test my code.
	# remember for your docker file, you need to change its port to 90 for testing

	# Then, once the code is finished, we need to create a new container and replace the old files in "app" folder.
	docker container create -p 80:80 --name tmp4 liyc1989/easy_prime
	# suppose your are in your working dir
	docker cp app.py tmp4:/app
	docker cp config.yaml tmp4:/app
	docker cp utils.py tmp4:/app
	
	# Last, create new image and push to docker hub
	docker commit tmp4 easy_ngg_design
	docker login
	docker tag easy_ngg_design liyc1989/easy_ngg_design
	docker push liyc1989/easy_ngg_design













