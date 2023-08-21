import argparse
import csv
import pandas as pd

import figure_util


# 初始化累加器


def calculate_average_usage(filename):
    """计算CSV文件中的CPU和内存的平均使用率."""
    total_cpu = 0
    total_memory = 0

    with open(filename, 'r') as file:
        reader = csv.reader(file)

        # 跳过表头
        next(reader)

        # 计数器，记录总行数
        count = 0

        for row in reader:
            cpu = int(row[3][:-1])  # 提取CPU值，去掉末尾的"m"并转换为整数
            memory = int(row[4][:-2])  # 提取内存值，去掉末尾的"Mi"并转换为整数

            total_cpu += cpu
            total_memory += memory
            count += 1

    # 计算平均值
    avg_cpu = total_cpu / count
    avg_memory = total_memory / count
    # print(filename)
    # print("avg_cpu : " + str(avg_cpu))
    # print("avg_memory :" + str(avg_memory))

    return avg_cpu, avg_memory


def sum_cpu_memory(fileStr, dir: str):
    total_cpu = 0
    total_memory = 0
    for item in fileStr:
        avg_cpu, avg_memory = calculate_average_usage(dir + "/" + item)
        total_cpu = total_cpu + avg_cpu
        total_memory = total_memory + avg_memory
    return total_cpu, total_memory


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Monitor k8s pod resource usage.")
    parser.add_argument("-d", "--dir", help="Directory to save CSV files to.", type=str, default="output_files")
    parser.add_argument("-o", "--output", help="Directory to save output result csv", type=str, default="output.csv")
    args = parser.parse_args()
    dirs = args.dir.split(" ")
    print(dirs)
    fileStr = ["vt-mysql-0_mysql.csv", "vt-mysql-1_mysql.csv", "vt-mysql-2_mysql.csv"]
    fileStr = ["vt-mysql-0_mysql.csv", "vt-mysql-0_vttablet.csv", "vt-mysql-1_mysql.csv", "vt-mysql-1_vttablet.csv",
               "vt-mysql-2_mysql.csv", "vt-mysql-2_vttablet.csv", "vt-vtgate-67b774c449-tlnmw_vtgate.csv"]

    data = {'cpu': [], 'memory': []}
    for dir in dirs:
        total_cpu, total_memory = sum_cpu_memory(fileStr, dir)
        print("total cpu : " + str(total_cpu))
        print("total memory : " + str(total_memory))
        data['cpu'].append(total_cpu)
        data['memory'].append(total_memory)
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data, index=dirs)

    # Write the DataFrame to CSV
    df.to_csv(args.output)

    figure_util.Draw(
        figureTitle="Resource",
        configs={
            'filename': args.output
        }
    )
