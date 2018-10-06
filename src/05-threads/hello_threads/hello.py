import time
import threading


def main():
    threads = [
        # daemon=True stops the threads running when the main thread finishes
        threading.Thread(target=greeter, args=("Michael", 10), daemon=True),
        threading.Thread(target=greeter, args=("Sarah", 5), daemon=True),
        threading.Thread(target=greeter, args=("Zoe", 2), daemon=True),
        threading.Thread(target=greeter, args=("Mark", 11), daemon=True),
    ]

    [t.start() for t in threads]    # return value is ignored

    print("This is other work.")
    print(2 * 2)

    [t.join(timeout=1) for t in threads]    # timeout=1 waits for 4 secs before terminating

    print("Done.")


def greeter(name: str, times: int):
    for i in range(0, times):
        print("{}. Hello there {}".format(i, name))
        time.sleep(1)


if __name__ == '__main__':
    main()
