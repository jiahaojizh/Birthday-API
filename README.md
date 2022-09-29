# Birthday-API  

Birthday-API is a REST API that has one endpoint /hello/{username} and it allows two operations:  

*GET /hello/{username}* this endpoint returns:
  - 404 ERROR, if the username does not exist
  - 200 OK, “Hello, <username>! Your birthday is in N day(s)” if the birthday of the user is not today
  - 200 OK, “Hello, <username>! Happy birthday!”
  
*PUT /hello/{username}  { “dateOfBirth”: “YYYY-MM-DD” }* this endpoint returns:
  - 400 ERROR, if the username does not contain only letters
  - 400 ERROR, if the date is later than NOW or is not a correct date, for example 1998-00-00
  - 204 NO CONTENT, if the put has created/updated the username correctly
  
## Directory structure  

  - *database/*: This directory contains the database to be mounted in the docker container
  - *flaskr/*: This directory contains the source code and a script for creating the database
  - *tests/*: This directory contains the unittests for the app
  - *Dockerfile*: The docker file to create the app, based on python:3.10
  - *install.bash*: This is a script that builds the docker image, handles the database creation, and runs the docker container mounting the volume
  - *requirements.txt*: This file contains the required dependencies for python
  - *Vagrantfile*: This file contains information for creating a virtualbox based on ubuntu/focal64 with the necessary software to run the api locally
  
## How to deploy  

  For now only details for linux will be provided, however as it is mounted in docker, it easy to deploy in any OS:  
  
### Having a linux machine with docker installed  

If you have a linux machine with docker installed it is as easy as cloning the repository, give run permissions to install.bash and run it:
```
git clone https://github.com/jiahaojizh/Birthday-API.git
cd Birthday-API
sudo chmod +x install.bash
./install.bash
```
### Having a another OS  
If you have another OS you can build your environment using the Vagrantfile:

You will need [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/) installed on your computer. How to deploy a vagrant machine is out of scope of this project.  

## Usage examples:

Currently the API is deployed in the port 80.

GET operation:
  ```curl localhost:80/hello/user```
  
PUT operation:
  ```curl http://localhost:80/hello/user -d "dateOfBirth=1998-09-21" -X PUT```

### System diagram in AWS (Currently)

![image](https://user-images.githubusercontent.com/114239936/193149162-fd73ea4e-48ec-461c-9718-9bf389818704.png)

Currently, our app is deployed in a docker container inside a EC2 instance. However, there are changes regarding to the architecture that are planned to implement to comply with the No-Downtime production deployment in the following section

### Future work

Due to the deadline there are some additions to the architecture that could not be implemented, this section is intended to share info regarding to improvements.

#### No-downtime production deployment

![image](https://user-images.githubusercontent.com/114239936/193149669-c1878590-987a-4080-904c-2a79ecd387cf.png)

This is a first version of the architecture for a more robust deployment.  
  - An nginx as load balancer is added
  - The load is distributed initially on both servers
  - When there is a new release, one server handles all the load (Green), while the other gets updated (Blue)
  - After the update, the load gets handled by the Blue
  - If everything goes fine, the green is updated and the load is distributed again, otherwise the blue is rolled back to the previous version

#### Change database to postgresql or another database with more features

![image](https://user-images.githubusercontent.com/114239936/193153107-932fed33-9a21-4f9f-852f-93b1a7d30c0a.png)

Sqlite was used because it was easy to deploy and test and it does not require much effort. To scale sqlite in a AWS environment, a solution could be to share a volume across the servers.

However a proper solution would be to deploy a postgresql for instance on another docker container to have service/database separated, and tested better or use any cloud service.

#### Add syntax and code quality checkers
To ensure that our code has no vulnerabilities and comply with the standards

#### Automate the pipeline
Adding CI/CD pipelines, for all the lifecycle from testing to deployment

Those are some of the features that are missing among others.

  

