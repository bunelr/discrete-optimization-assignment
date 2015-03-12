# discrete-optimization-assignment
Webapp to collect, compile and validate OMA 2015's optimization assignment


Futur employer of Rudy and Alban, please don't judge us on this, it was thrown together in an afternoon to help out the class

## TODO:
Stop being so blatantly insecure (ie, running arbitrary code uploaded by people on the internet)



## Installation
This is currently run on a Digital Ocean Machine.
The description of how we run everything follows. It may not be the simplest but it consisted in what we were familiar with.

* Clone the repo on your server
* Create a python virtualenv in the app folder
````
cd discrete-optimization-assignment
virtualenv .
````
* Activate the virtualenv `source bin/activate`
* Install all the dependencies `pip install -r requirements.txt`
* Install a front end facing web server (such as Nginx), you can obtain it from your distribution's package manager
* Put the following configuration's snippet in `/etc/nginx/sites-available/assignment` and `/etc/nginx/sites-enabled/assignment` (It authorizes submission to take as much as 5 minutes to run, without the page erroring)

````
server {
    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_connect_timeout       300;
        proxy_send_timeout          300;
        proxy_read_timeout          300;
        send_timeout                300;
    }
}
````

* Restart the webserver so that it takes the changes into account: `/etc/init.d/nginx restart`
* In order to run the app even when we're not logged in the servor, we used superviord. To install it: `pip install supervisor`
* Drop the following snippet into `/etc/supervisor/conf.d`:

````
[program:assignment]
command = /home/user/discrete-optimization-assignment/run.sh
user = user                                                          ; User to run as
stdout_logfile = /home/user/log.txt
redirect_stderr = true                                                ; Save stderr in the same log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
````
* Install all the things that may be required by the students: make, gcc, ...

## Some notes:
* In the repo, the app is configured in debug mode. To deploy it, you should change the last line from

````python
    app.run(debug = True, use_reloader = False, port=8000)
````

to

````python
    app.run(port=8000)
````

* You should also change the password in the `config.py` file.
* Before the first run, you may have to create an empty halloffame file and submission directory: `echo "{}" > halloffame.json && mkdir submission`

* There is some basic monitoring going on, if you want to use it, you can install an Agent from Datadog. It is not required.
