import subprocess
import time
import csv
import argparse
import os
from datetime import datetime

import matplotlib.pyplot as plt


def fetch_data():
    cmd = ["kubectl", "top", "pod", "--containers"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.split("\n")
    timestamp = datetime.now().strftime('%H:%M:%S')
    return timestamp, lines[1:-1]


def parse_data(timestamp, lines):
    data_dict = {}
    for line in lines:
        parts = line.split()
        pod_name, container_name, cpu, memory = parts[0], parts[1], parts[2], parts[3]
        key = f"{pod_name}_{container_name}"
        if key not in data_dict:
            data_dict[key] = []
        data_dict[key].append([timestamp, pod_name, container_name, cpu, memory])
    return data_dict


def save_to_csv(container_data, key, output_dir):
    filename = os.path.join(output_dir, f"{key}.csv")
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["timeStamp","POD", "NAME", "CPU(cores)", "MEMORY(bytes)"])
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(container_data)


def plot_graphs(key, output_dir):
    filename = os.path.join(output_dir, f"{key}.csv")
    timestamps = []
    cpus = []
    memories = []

    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip header
        for row in csvreader:
            timestamps.append(row[0])  # Timestamp
            cpus.append(int(row[3].rstrip('m')))  # CPU
            memories.append(int(row[4].rstrip('Mi')))  # Memory

    plt.figure(figsize=(15, 5))

    # CPU graph
    plt.subplot(1, 2, 1)
    plt.plot(timestamps, cpus, label="CPU Usage")
    plt.xlabel('Time')
    plt.ylabel('CPU (milli-cores)')
    plt.title(f"CPU Usage for {key}")
    plt.xticks(rotation=45)
    plt.legend()

    # Memory graph
    plt.subplot(1, 2, 2)
    plt.plot(timestamps, memories, label="Memory Usage")
    plt.xlabel('Time')
    plt.ylabel('Memory (MiB)')
    plt.title(f"Memory Usage for {key}")
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{key}_usage.png"))
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor k8s pod resource usage.")
    parser.add_argument("-d", "--dir", help="Directory to save CSV files to.", default="output_files")
    parser.add_argument("-t", "--time", help="Duration to monitor (in seconds).", type=int, default=200)
    parser.add_argument("-test", "--test", help="Duration to monitor (in seconds).", type=str, default="wesql80-20.sh")

    args = parser.parse_args()

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    end_time = time.time() + args.time
    print(args.test)
    output = subprocess.check_output(["bash",args.test])
    print(output.decode('utf-8'))
    time.sleep(50)
    print("--------------- begin monitor ---------------")
    try:
        while time.time() < end_time:
            timestamp, lines = fetch_data()
            data_dict = parse_data(timestamp, lines)
            for key, container_data in data_dict.items():
                save_to_csv(container_data, key, args.dir)
                print(f"Data for {key} saved to {key}.csv in {args.dir}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    print("--------------- end monitor ---------------")

    # # Generate graphs
    # for key in data_dict.keys():
    #     plot_graphs(key, args.dir)
