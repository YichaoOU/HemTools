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

