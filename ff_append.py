# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │            Append two files together with a re-encoding of codecs            │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯
import sys
import argparse
import subprocess


def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser.add_argument('-f', '--first',     type=str, required=True,          help='The name of the first input file.')
    parser.add_argument('-s', '--second',   type=str, default="ff_append.mp4", help='The name of the second input file.')
    parser.add_argument('-o', '--output',   type=str, required=True,          help='The name of the output file.')
    parser.add_argument('-C', '--config',    type=str, default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str, default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    args = parser.parse_args()
    return args



def launch_command(args):
    print("ff_append.py - Re-encoding and Appending videos.")
    command = ["ffmpeg", "-v", args.loglevel, "-i", args.first, "-i", args.second,
            "-filter_complex", "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]",
            "-map", "[v]", "-map", "[a]", args.output]
    result = subprocess.run(command)
    if result.returncode == 0:
        print("✅ {}".format(args.output))
    else:
        print("❌ Error: {}".format(args.output))


def main():
    args = get_params()
    launch_command(args)




if __name__ == '__main__':
    main()
