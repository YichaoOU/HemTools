Hosting web server on AWS
=========================

Latest updates
^^^^^^^^^^^

My AWS EC2 instance is somehow completely down and I have no clue how to fix it. I can't even SSH to it. I also tried rebuild/ clone the environment, they all failed.

I decided to use docker container and AWS ECS (a subset of EC2) to host my web application because EC2 is so hard to manage:

- 1. I have to build the VM by SSH to it and install some dependencies and download some data. Now with docker container, I can just do it locally and then check if my modification looks correct or not.

- 2. If the server error happends again, I can just create a new and upload the docker contaniner without building the dependencies ever again.


My deployment is finally succedded, according to this tutorial: https://acloudguru.com/blog/engineering/deploying-a-containerized-flask-application-with-aws-ecs-and-docker

.. note:: The above link is old. AWS updated its UI, so those screenshot are misleading now. The steps are: Create Cluster X, create task definition, click Cluster X and select create task. Another important note, you have to update "Security Groups" for this task as: IP4, HTTP, TCP 80 0.0.0.0/0

The key is to directly use port 80 in app.py

::

	if __name__ == "__main__":
	    app.run(host='0.0.0.0', port=80)

and in the ``Dockerfile``

::

	EXPOSE 80

The following tutorial didn't work, mainly due to port 8050 issues. I don't know if it is because AWS updated their protocol.

- https://towardsdatascience.com/deploy-containerized-plotly-dash-app-to-heroku-with-ci-cd-f82ca833375c
- https://towardsdatascience.com/how-to-use-docker-to-deploy-a-dashboard-app-on-aws-8df5fb322708


I found docker hub upload speed is slower than AWS ECR. But it is free. With hg19 genome, my docker size is almost 8GB. But I found it is fine as long as your docker size is below 20GB.

my commands
-------

::

	# create docker
	docker build -t easy_prime .
	# test docker container to identify bugs before publish
	docker run -p 80:80 easy_prime
	# upload docker container
	docker tag easy_prime:latest liyc1989/easy_prime:latest
	docker push liyc1989/easy_prime:latest
	# set up AWS sever using browser
	# Remember to add port mapping 80


AWS ECS change IP everytime
^^^^^^^^^^^^^^^

May need to use load balancer: https://www.youtube.com/watch?v=TsVO14-lqp0



Summary
^^^^^^

You can get a free one-year account on: https://aws.amazon.com/free/

Currently, I'm not sure whether or not AWS will charge you if the web app has been over-used, like CPU time is above their "free zone".

8/4/2020

It turns out that you can easily pass the free 750 hours (= 1 month) if you don't know that you have servicea in more than one cluster. It finally charged me $4 in July and estimated to be $8 per month.

I then terminated all services and asked for refund.

8/20/2020

Seems that ``eb create`` will create running instances in multiple areas, e.g., N.virginia and Orengan.

Usage
^^^^^

Step 1: register an AWS account
------------------------------

You can use the free one here: https://aws.amazon.com/free/

Go to: https://console.aws.amazon.com, and create a new access key

.. image:: ../../images/AWS_1.png
	:align: center

.. image:: ../../images/AWS_2.png
	:align: center


Step 2: install command line tools for ``AWS Elastic Beanstalk``
------------------------------

::

	conda install -c contango awsebcli

## awsebcli conda is only available in win64, however, I successfully installed it in macOS, not sure why.


Step 3: Dash app toy example
------------------------------

Now, suppose you have a Dash app already and you want to deploy it to EB.

Ref: https://medium.com/@korniichuk/dash-on-aws-44a0f50a030a

Create a new folder, ``test``, and copy the following dash app and save it as ``application.py``. This is a keyword.

For other keywords, see http://www.zhengwenjie.net/beanstalk/

::

	import dash
	import dash_html_components as html

	app = dash.Dash(__name__)

	app.scripts.config.serve_locally = True
	app.css.config.serve_locally = True

	app.layout = html.Div([
	    html.H1('Hello, World!')
	])

	application = app.server

	if __name__ == '__main__':
	    application.run(debug=True, port=8080)

Next, 

Copy python dependencies and save it as ``requirements.txt``. Again, keywords.

::

	dash==0.39.0
	dash-daq==0.1.0

Then, open terminal, to go folder ``test`` and type the following command:

::

	eb init
	# It may ask you to input id and password that you created in step1
	# Do you want to set up SSH for your instances?
	# (Y/n): Enter n
	eb create
	eb open

If you see Hello World, then congratulations!


Step 4: Upload your own Dash app
------------------------------

Basically, if you have finished step 3 then you should be able to upload any python programs. 

I want to put my Easy-Prime tool up there and have encountered several problems. Here's how I solved them.

1. I put all the dependencies in ``requirements.txt``, I didn't specify version because I think it could cause conficts.

::

	dash
	dash-daq
	biopython
	dash-bio
	dash-html-components
	joblib
	matplotlib
	numpy
	pandas
	plotly
	plotly-express
	PyYAML
	scikit-image
	scikit-learn
	scipy
	seaborn

2. I had a gcc problem and found a solution. First, create a folder called ``.ebextensions`` and a file inside it called, ``01_packages.config``.

::

	packages:
	  yum:
	    gcc-c++: []
	    unixODBC-devel: []
	    python3-devel: []

The indent should be spaces, not tab.

3. I found using SSH is the easiest way install things.

``eb ssh`` will ssh to your instances in the current working dir, otherwise you can use ``eb ssh env_name``.

Your app is stored at ``/var/app/current`` and your python is ``/var/app/venv/bin/python``

By default, you can't write in these dirs, so you need to add ``sudo``. I don't know why they give you sudo option, but not directly writable.

``sudo yum groupinstall "Development Tools"``

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compile-software.html

Again, this is obviously necessary, but you have to install it yourself.

Default EB size is 8G, now if I put hg19.fa, it also used all the space and I got no space error. I have to increase the space in EC2. I don't know if it will cause extra money.

To update your code on EB, use ``eb deploy``


``eb deploy`` will remove every old code. If I have small changes, I will directly modify the code online. There should some git pull method.

To increase space, simply increase the volumn on the webpage will not work. Follow the method here: https://til.codes/extending-the-disk-space-on-an-amazon-ec2-instance/ did not completely solve my problem, but did give me a good start. So eventually, the command I'm using is:

::

	lsblk # to look at the space

	sudo growpart /dev/xvda 1

	sudo xfs_growfs -d /mnt


TODO: I heard that "AWS S3 + Lambda" is much cheaper.


Step 5. update eb app
^^^^^^^^^^^^^^^

Please do not delete or rebuild your env, otherwise you will have to configure a lot of things. 

Things I have done, install many python packages, e.g. dash, and some bioinformatics tools, htslib.

Now I have a new dash app, all I need to do is upload this as a zip folder and then deploy it, all using a browser!


Where to upload and deploy
------------------

link: https://us-west-2.console.aws.amazon.com/elasticbeanstalk/home?region=us-west-2#/environments

Find your application, click Actions and go to view versions.

.. image:: ../../images/how_to_find_upload_button.png
	:align: center

Click upload first, when it is finish, then choose this new app and deploy it.

.. image:: ../../images/how_to_deploy_and_upload.png
	:align: center

Then you can view deploy logs

.. image:: ../../images/deploy_message.png
	:align: center

Once you have successfully deployed, you can then use the ssh terminal to do further updates, like I need to download hg19 to this /var/app/current folder.

.. image:: ../../images/where_to_find_instance.png
	:align: center

.. image:: ../../images/where_to_find_connect.png
	:align: center

.. image:: ../../images/browser_ssh_connect.png
	:align: center


Upload size error
^^^^^^^^

::

	nano /etc/nginx/nginx.conf

add ``client_max_body_size  50M;``. Then ``service nginx restart`` or ``systemctl reload nginx``.

The bw file I'm using "https://www.dropbox.com/s/ojqvi0pbnw975cl/SRR8056671_293T.rmdup.uq.bw"

::


	server {
	listen80 default_server;
	access_log    /var/log/nginx/access.log main;
	client_header_timeout 60;
	       client_body_timeout   60;
	keepalive_timeout     60;
	       client_max_body_size  50M;
	gzipoff;
	gzip_comp_level4;
	gzip_types text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript;
	# Include the Elastic Beanstalk generated locations
	include conf.d/elasticbeanstalk/*.conf;
	}

Notes
^^^^^

::

	eb logs
	eb ssh

Your DASH stdout is here: ``/var/log/web.stdout.log``


re-build instances
^^^^^^^^^^

Today when I check again on Easy-Prime, the server is down! And I found that the enviorment is just gone. I have to start over. My AWS EB instance was replaced with a new one. I checked online, this could be caused by AWS auto-scaling. But I'm still not sure why it happened. Now I have to reinstalled everything.


Memory allocation problem
^^^^^^

 5891 webapp    20   0 1388604 199624  51280 S  0.0 19.8   0:02.30 gunicorn                                                                                                  
17153 webapp    20   0  234568  17876   2952 S  0.0  1.8  21:46.91 gunicorn 

solution: find the one with higher memory usage and kill it. `top -u webapp`
