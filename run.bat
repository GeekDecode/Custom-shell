
docker run -it --env-file .env -v "%cd%:/app" my-ai-shell
:: Just type ./run_docker.ps1

::Build = Make the recipe (the Image).
::Run = Cook the meal (the Container).
::-it = I want to talk to it (Interactive).
::-v = Volume (Link my folders).
::--env = Give it my secrets (API Keys).