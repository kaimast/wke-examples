#! /bin/env python3

''' Script to benchmark MongoDB '''

# pylint: disable=too-many-locals

from typing import Any

from wke import Cluster, Configuration, MeasurementFailedError
from wke.measurement import MeasurementSession
from wke.logging import MetaLogger
from wke.benchmark import benchmark_main

def run_measurement(params: dict[str, Any], collect_statistics: bool,
              result_printer, verbose=False) -> bool:
    ''' Our custom benchmark function '''

    def get_opts(arg_names, params):
        ''' Get a subset of the parameters needed for a specific target '''
        return dict((k, params[k]) for k in arg_names)

    cluster = Cluster(path='cluster.toml')
    config = Configuration("mongodb")
    session = MeasurementSession(cluster, config, verbose=verbose,
           collect_statistics=collect_statistics)

    nodes = cluster.create_slice()
    num_servers = 1
    num_clients = 1

    servers = nodes.create_subslice(num_servers)
    clients = nodes.create_subslice(num_clients)

    logger = MetaLogger(session.log_dir)
    logger.print(f'Running benchmark on with parameters: {params}')

    # add the server address to parameters, so it can be passed to targets
    params["server-address"] = nodes.get_internal_addrs()[0]

    session.run_background(servers, "run-mongod")

    success = session.run(clients, 'prepare-data',
            options=get_opts(['server-address', 'num-entries'], params))

    if not success:
        return False

    try:
        opt_names = [
            'server-address', 'num-entries', 'client-multiply',
            'write-chance', 'num-operations'
        ]
        total_num_ops=num_clients*params['client-multiply']*params["num-operations"]

        result = session.measure(clients, "client-ops",
            num_operations=total_num_ops,
            options=get_opts(opt_names, params))

    except MeasurementFailedError as err:
        logger.print(str(err))
        return False

    extra_data = {
        "throughput": round(result.throughput, 3),
    }

    result_printer.print(session.uid, params, extra_data)
    return True

def main():
    ''' The entrypoint of our benchmark script '''

    parameters = {
        "num-entries": {
            "default": 100000,
            "about": "How many entries does the database have initially",
        },
        "write-chance": {
            "default": 0,
            "about": "Likelihood that a client operation is a write",
        },
        "num-operations": {
            "default": 1000,
            "about": "How many requets to issue (per client)",
        },
        "client-multiply": {
            "default": 32,
            "about": "How many clients per client machine",
        }
    }

    benchmark_main(parameters, run_measurement)

if __name__ == "__main__":
    main()
