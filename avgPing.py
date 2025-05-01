import re

print("請貼上 ping 結果，輸入 END 結束輸入：")

while True:
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    data = "\n".join(lines)
    times = [float(match) for match in re.findall(r'time=([\d.]+) ms', data)]
    if times:
        avg_time = sum(times) / len(times)
        print(f"平均 time = {avg_time:.2f} ms\n")
    else:
        print("沒有找到 time=?? ms 的數值！\n")
    print("請繼續貼上 ping 結果，輸入 END 結束輸入：")
