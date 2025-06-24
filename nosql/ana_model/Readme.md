creating a model
----------------
sudo docker build -t ana_model .sudo docker system prune -a --volumes
sudo docker run -d --name ana_model -p 8002:8002 --network postgres_default ana_model


ask a LLM model to describe a pattern, 
based on this description, create a python script to generate synthetic data,
based on the synthetic data create a model


g



