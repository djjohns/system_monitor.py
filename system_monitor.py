import psutil
import time
from plyer import notification


# Set the threshold values for CPU usage, memory usage, GPU usage, and battery level
cpu_threshold = 40  # Percentage
memory_threshold = 40  # Percentage
C_disk_usage_threshold = 40  # Percentage
D_disk_usage_threshold = 40  # Percentage
battery_threshold = 100  # Percentage

app_name = "System Monitor"


def convert_bytes_to_gb(bytes):
    bytes_to_gb = bytes / (1024**3)
    return bytes_to_gb


# Infinite loop to continuously monitor system resources
while True:
    try:

        # Check CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        if cpu_usage >= cpu_threshold:
            message = f"CPU usage is high: {cpu_usage}%"

            notification.notify(
                title="Resource Alert",
                message=message,
                app_name=app_name,
                timeout=10,
            )

        # Check memory usage
        memory_usage = psutil.virtual_memory().percent
        mem_available = convert_bytes_to_gb(psutil.virtual_memory().available)
        mem_total = convert_bytes_to_gb(psutil.virtual_memory().total)

        if memory_usage >= memory_threshold:
            message = f"""
            Memory usage is high: {memory_usage}%
            Memory Total: {mem_total:.2f} GB
            Memory Available: {mem_available:.2f} GB
            """

            notification.notify(
                title="Resource Alert",
                message=message,
                app_name=app_name,
                timeout=10,
            )

        # Check battery level
        battery = psutil.sensors_battery()

        if (
            battery is not None
            and battery.percent <= battery_threshold
            and not battery.power_plugged
        ):
            message = f"Battery level is low: {battery.percent}%"

            notification.notify(
                title="Battery Alert",
                message=message,
                app_name=app_name,
                timeout=10,
            )

        def get_disk_usage_in_gb(path="C:\\"):
            usage = psutil.disk_usage(path)

            # Convert to Gb.
            used_gb = convert_bytes_to_gb(usage.used)
            total_gb = convert_bytes_to_gb(usage.total)
            free_gb = convert_bytes_to_gb(usage.free)
            percentage = usage.percent

            return (used_gb, total_gb, free_gb, percentage)

        # Check Disk usage.
        c_usage_gb = get_disk_usage_in_gb()

        if c_usage_gb[-1] >= C_disk_usage_threshold:
            message = f"""
            C:\\ disk usage is high: {c_usage_gb[-1]:.2f}%
            Total Space:{c_usage_gb[1]:.2f} GB
            Used Space: {c_usage_gb[0]:.2f} GB
            Remaining Space: {c_usage_gb[2]:.2f} GB
            """

            notification.notify(
                title="Disk Space Low Alert",
                message=message,
                app_name=app_name,
                timeout=10,
            )

        # Wait for 5 minutes before checking the resources again
        time.sleep(300)

    except Exception as e:
        print("An error occurred:", str(e))
        break
