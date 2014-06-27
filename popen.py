import subprocess

cmd = subprocess.Popen("livestreamer http://www.twitch.tv/callofduty best")

sleep(10)

cmd.kill()
