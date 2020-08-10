Hosting web server on AWS
=========================


Summary
^^^^^^

You can get a free one-year account on: https://aws.amazon.com/free/

Currently, I'm not sure whether or not AWS will charge you if the web app has been over-used, like CPU time is above their "free zone".

8/4/2020

It turns out that you can easily pass the free 750 hours (= 1 month) if you don't know that you have servicea in more than one cluster. It finally charged me $4 in July and estimated to be $8 per month.

I then terminated all services and asked for refund.

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



Notes
^^^^^

::

	eb logs
	eb ssh

