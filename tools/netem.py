import argparse


def gen_netem_script(netems, dev, filters):
    """Generates a tc netem script

    netems  a list of arguments for netem qdiscs
    dev     dev argument of 'tc'
    filters a list with the same size as 'netems'. Each element is a list of
            IP addresses that will be filtered and queued to the corresponding qdisc
    """
    assert len(netems) == len(
        filters
    ), "Number of filter groups must match number of netem argument groups"

    script = [
        "# Generated by netem.py",
        "set +e",
        f"tc qdisc del dev {dev} root 2> /dev/null",
        "set -ex",
        f"tc qdisc add dev {dev} root handle 1: htb",
    ]

    for i, netem in enumerate(netems):
        script += [
            f"tc class add dev {dev} parent 1: classid 1:{i+1} htb rate 1gbit",
            f"tc qdisc add dev {dev} parent 1:{i+1} handle {(i+1)*10}: netem {netem}",
        ]
    for i, filter in enumerate(filters):
        for ip in filter:
            script += [
                f"tc filter add dev {dev} parent 1: protocol ip prio 1 u32 match ip dst {ip} flowid 1:{i+1}"
            ]
    script += [
        "set +x",
        "echo",
        'echo "***** QDISC ******"',
        f"tc -col qdisc show dev {dev}",
        "echo",
        'echo "***** CLASS ******"',
        f"tc -col class show dev {dev}",
        "echo",
        'echo "***** FILTER ******"',
        f"tc -col filter show dev {dev}",
        "echo",
    ]
    return "\n".join(script)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate netem script")
    parser.add_argument("netem", help="Netem commands")
    parser.add_argument(
        "-d", "--dev", default="eth0", help="Network interface to apply on"
    )
    parser.add_argument("-f", "--filter", nargs="*", help="IP addresses to apply on")

    args = parser.parse_args()
    if args.filter is None:
        args.filter = []
    print(gen_netem_script([args.netem], args.dev, [args.filter]))
