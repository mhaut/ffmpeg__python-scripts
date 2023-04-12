# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │          Trim a group of videos from the start / end proportionally          │
# │                       to fit a specified video length.                         │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯

# Explanation:

# You need to make a instagram video with a hard limit of 60 seconds length.
# You have 4 clips that make up a total duration of 80 seconds.
# - 2x 30s clip
# - 1x 15s clip
# - 1x 5s clip
# This script will proporionally cut an equal percentage from the start and end
# of each clip to trim 80sec down to 60sec.
# To remove those 20sec, we could easily remove 5sec from each clip equally, but
# that would completely remove the single last 5 second clip. Instead we do it
# proporionally.

# The Example Maths:

# The Full duration of all clips is 80sec = 100%
# Which means 1sec = 1.25% (100%/80)

# Multiply 1.25 by 30, means 30seconds = 37.5%
# The file breakdown would be:
# Seconds:    30sec | 30sec | 15sec  | 5sec  = 80sec
# Percent:    37.5% | 37.5% | 18.75% | 6.25% = 100%

# The 20 second cut means we need to remove 1.25*20= 25%
# Now use the percentage breakdown for each clip across 20seconds.

# 20 seconds / 100 (%) = 0.2
# 0.2 * 37.5% (first clip)  = 7.5 seconds
# 0.2 * 37.5% (second clip) = 7.5 seconds
# 0.2 * 18.75% (third clip) = 3.75 seconds
# 0.2 * 6.25% (fourth clip) = 1.25 seconds

# Just to confirm: 7.5 + 7.5 + 3.25 + 1.25 = 20 (seconds)

# Conclusion:

# - Clip one needs to remove 7.5 seconds. Divide by 2 for start and end means 3.75sec off both start and end.
# - Clip two needs to remove 7.5 seconds. Divide by 2 for start and end means 3.75sec off both start and end.
# - Clip three needs to remove 3.75 seconds. Divide by 2 for start and end means 1.875sec off both start and end.
# - Clip four needs to remove 1.25 seconds. Divide by 2 for start and end means 0.625sec off both start and end.

# We have calculated the proportionate amount to remove off each clip by
# measuring the file duration against the full duration.

# The final file will be 60 seconds in total

import os
import sys
import glob
import argparse
import subprocess



def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser.add_argument('-i', '--input',    type=str, nargs='+', required=True, help='The name of an input file(s) (can be a wildcard).')
    parser.add_argument('-o', '--output',   type=str,  required=True, help='The name of the output file.')
    parser.add_argument('-d', '--duration',   type=float, default=10,   help='Maximum duration of clips')

    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args


def convert_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)

def launch_command(args):
    print("ff_concat.py - Running video concatenation.")

    with open('./mylist.txt', 'w') as file:
        for pattern in args.input:
            file.write("file '{}'\n".format(pattern))
    input_files = sum([glob.glob(pattern) for pattern in args.input], [])



    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]


    durations = []
    for inpfil in input_files:
        # , '2>&1'
        command2 = ['-i', inpfil]#, '|', 'grep', "'Duration'", '|', 'cut', '-d', '" "', '-f', '4', '|', 'sed', 's/,//']

        try:
            process = subprocess.Popen(command + command2, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            output = process.communicate()[0]
            result = output.decode()
            duration_index = result.find('Duration')
            duration = result[duration_index+10:duration_index+21]
            durations.append(float(convert_to_seconds(duration)))
        except:
            print("❌ Error reading file " + inpfil)
            exit()


    total_duration = sum(durations)
    limit = args.duration / total_duration

    dur_final = 0
    if limit < 1:
        with open("./mylistInt.txt", "w") as f:
            for idf, (inpfil, duration) in enumerate(zip(input_files, durations)):
                fname = "./intermediate" + str(idf) + ".mp4"
                f.write("file '" + fname+"'\n")
                offset = (duration - (duration*limit)) / 2
                dur_final += round(duration-offset) - round(offset)
                command2 = ["-v", args.loglevel, "-i", inpfil, "-ss", str(round(offset)), "-to", str(round(duration-offset)), "-c", "copy", fname]
                # print(command + command2)
                result = subprocess.run(command + command2)
                if result.returncode == 0:
                    print("✅ {}".format(fname))
                else:
                    print("❌ Error creating file " + fname)
                    exit()

    command += ["-v", args.loglevel,"-f", "concat", "-safe", "0", "-i", "./mylistInt.txt", "-c", "copy", args.output]
    print(command)
    result = subprocess.run(command)
    if result.returncode == 0:
        result = subprocess.run("rm ./mylist.txt ./mylistInt.txt ./intermediate*.mp4", shell=True, stdout=subprocess.PIPE)
        if result.returncode == 0:
            print("✅ {}".format(args.output))
        else:
            print("✅ {}".format(args.output))
            print("❌ Error removing file(s) mylist.txt and/or ./mylistInt.txt")
    else:
        print("❌ Error: {}".format(args.output))


def main():
    args = get_params()
    launch_command(args)




if __name__ == '__main__':
    main()
