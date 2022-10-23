
# mypower
Monitor house power consumption based on Mirubox

docker swarm update --dispatcher-heartbeat 600s
Launch:
docker stack deploy --compose-file docker-compose.yml mypower

Stop:
docker stack rm mypower
