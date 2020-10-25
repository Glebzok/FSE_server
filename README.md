# Skoltech scientific papers searching application (backend)


## System deployment
You can either build and deploy the system using Docker (with Dockerfile) or deploy it directly to Heroku (with Procfile)

Heroku:
```bash
sudo snap install heroku --classic
heroku login
git clone https://github.com/Glebzok/FSE_server.git
cd FSE_server
heroku create
git push heroku master
heroku ps:scale web=1
```

## Initializing papers database
When the application is deployed, only 200 papers per year are downloaded to the database, (we are restricted by Heroku), you can change that by modifying the Dockerfile or Procfile accordingly (see add_articles.py), or runing add_articles.py manually.
You can specify the number of years and the number of papers per year to download.
```bash
python3 add_articles.py --help # to get help
python3 add_articles.py -r # download all the papers from https://neurips.cc/
```

## Checking papers downloading progreess
After the the system deployment is started, you can check how many papers are downloaded at the moment by listing papers_data/pdf folder
```bash
ls /papers_data/pdf | wc -l
```

## Accessing the server running on Heroku
To access the server running on Heroku via terminal, you should run the following command
```bash
heroku ps:exec
```

## Adding new papers to the papers base
You can add new papers in addition to ones downloaded from https://neurips.cc/.
To do that you should place them in pdf format in ./papers_data/new_papers folder (by default, can be changed in the code)
and name them with the name, that you want them to be named in the base and run add_articles script without -r flag 
```bash
python3 add_articles.py
```

## Papers indexing
Papers indexing is performed automatically, when add_articles script is run

## API
The server has two endpoints: /hello and /search_by_query
The first one is made for server pinging purpose. It returns hello message in response to GET request.
The second one is for query answering purpose. It receives a search query as an url argument 'query' and returns
the response in the following JSON format.
```json
{'response':{'result': [{'name': paper1_name, 'link': paper1_link.pdf}, 
                        {'name': paper2_name, 'link': paper2_link.pdf}]}}
``` 
Where name is a paper name and link is a link to it

## Pinging
If the system is deployed on Heroku, then you should ping it every 30 minutes or it wll go to sleep and all the data
will be lost, for these purposes, ping script exists. You can run it locally to ensure that the server is running. 
