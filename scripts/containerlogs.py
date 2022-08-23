#!/usr/bin/python3
import docker
import sys
import datetime


def get_container_stat(container_name):
    global container_status
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    docker_client = docker.from_env()
    try:
        container = docker_client.containers.get(container_name)
        container_stat = container.stats(stream=False)
        container_status = container.attrs['State']['Status']

        if container_status == "running":
            # cpu usage calculation
            cpu_delta = container_stat['cpu_stats']['cpu_usage']['total_usage'] - container_stat['precpu_stats']['cpu_usage']['total_usage']
            system_cpu_delta = container_stat['cpu_stats']['system_cpu_usage'] - container_stat['precpu_stats']['system_cpu_usage']
            number_cpus = container_stat['cpu_stats']['online_cpus']
            cpu_usage_perc = round(((cpu_delta / system_cpu_delta) * number_cpus * 100), 2)

            # memory usage calculation
            mem_used = container_stat['memory_stats']['usage'] - container_stat['memory_stats']['stats']['inactive_file']
            mem_available = container_stat['memory_stats']['limit']
            mem_usage_perc = round(((mem_used / mem_available) * 100), 2)

            logentry = str(timestamp) + "," + container_name + "," + str.upper(container_status) + "," + str(cpu_usage_perc) + "," + str(mem_usage_perc)
        else:
            logentry = str(timestamp) + "," + container_name + "," + str.upper(container_status) + "," + "NULL" + "," + "NULL"
        return logentry
    except docker.errors.NotFound as dockerErr:
        print("ERROR: " + "{}".format(dockerErr.explanation))


if __name__ == "__main__":
    try:
        container_name = sys.argv[1]
        result = get_container_stat(container_name)
        logfile_name = "webserver-stats.log"
        log_headers = "TIMESTAMP,NAME,STATUS,CPU%,MEM%"

        with open(logfile_name, 'a') as logfile:
            if logfile.tell() == 0:
                logfile.write("{}\n".format(log_headers))

            logfile.write("{}\n".format(result))
            logfile.close()

    except IndexError:
        print("Please enter container name. Usage: containerlogs.py <container_name>")
