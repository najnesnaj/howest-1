FASTAPI and the model
---------------------

this Dockerfile contains a fastapi application on port 8002

it takes the ticker symbol (DEZ:DE) as input, gets the market_cap from the database, and checks it it contains a pattern


(The model is trained in directory ana_synthetic)


creating a model
----------------
sudo docker build -t ana_model .
sudo docker system prune -a --volumes
sudo docker run -d --name ana_model -p 8002:8002 --network postgres_default ana_model


TODO
-----

This is WIP, I wanted to have the dockercontainer train the model as well, hence the presence of dockervolumes


