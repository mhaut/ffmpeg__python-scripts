# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │            Append two files together with a re-encoding of codecs            │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯

import sys
import argparse
import subprocess
import numpy as np
import concurrent.futures
from utils import vifp
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import cv2
from skimage import metrics
import math


def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()

def calculate_ssim(img1, img2, border=0):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    h, w = img1.shape[:2]
    img1 = img1[border:h-border, border:w-border]
    img2 = img2[border:h-border, border:w-border]

    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1[:,:,i], img2[:,:,i]))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')


def calculate_psnr(im1, im2, border=0):
    if not im1.shape == im2.shape:
        raise ValueError('Input images must have the same dimensions.')
    h, w = im1.shape[:2]
    im1 = im1[border:h-border, border:w-border]
    im2 = im2[border:h-border, border:w-border]

    im1 = im1.astype(np.float64)
    im2 = im2.astype(np.float64)
    mse = np.mean((im1 - im2)**2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))



def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser.add_argument('-f', '--first',     type=str, required=True,          help='The name of the first input file.')
    parser.add_argument('-s', '--second',   type=str, default="ff_append.mp4", help='The name of the second input file.')
    parser.add_argument('-o', '--output',   type=str, required=True,          help='The name of the output file LOG.')
    parser.add_argument('-C', '--config',    type=str, default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str, default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-p', '--parallel_process', type=int,  default=1,     help='Set the number parallel process.')

    args = parser.parse_args()
    return args


def read_video(pathvideo):
    cap = cv2.VideoCapture(pathvideo)
    frameCount  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps         = int(cap.get(cv2.CAP_PROP_FPS))
    buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
    for fc in range(frameCount):
        ret, buf[fc] = cap.read()
        if ret == False: break
    cap.release()
    return buf, fps


def save_video(pathoutput, numpy_array, fps, size):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # codec
    out = cv2.VideoWriter(pathoutput, fourcc, fps, (size[1], size[0]))
    for frame in numpy_array:
        out.write(frame)
    out.release()


def diff_videos(args):
    video1, fpsv1 = read_video(args.first)
    video2, fpsv2 = read_video(args.second)
    assert video1.shape == video2.shape, "Videos have different dimensions."
    videoD = np.abs(video1-video2)
    save_video(args.output, videoD, fpsv1, (video1.shape[1], video1.shape[2]))


def calculate_psnr_ffmpeg(args):
    cmd = ['ffmpeg', '-i', args.first, '-i', args.second, '-lavfi', 'psnr', '-f', 'null', '-']
    result = subprocess.run(cmd, check=True)
    if result.returncode == 0:
        print("✅ {}".format(args.output))
    else:
        print("❌ Error: {}".format(args.output))


def calculate_ssim_ffmpeg(args):
    cmd = ['ffmpeg', '-i', args.first, '-i', args.second, '-lavfi', 'ssim', '-f', 'null', '-']
    result = subprocess.run(cmd, check=True)
    if result.returncode == 0:
        print("✅ {}".format(args.output))
    else:
        print("❌ Error: {}".format(args.output))


def calculate_vmaf_ffmpeg(args):
    cmd = ['ffmpeg', '-i', args.first, '-i', args.second, '-lavfi', 'libvmaf="model_path=vmaf_models/vmaf_v0.6.1.json:psnr=1:ssim=1"', '-f', 'null', '-']
    result = subprocess.run(cmd, check=True)
    if result.returncode == 0:
        print("✅ {}".format(args.output))
    else:
        print("❌ Error: {}".format(args.output))




def process_frame_metric(f1, f2):
    psnr = calculate_psnr(f1, f2)
    ssim = calculate_ssim(f1, f2)
    vif  = vifp.vifp_mscale(f1, f2)
    return [psnr, ssim, vif]

def process_frame_stats(f1):
    avg = np.average(f1)
    std = np.std(f1)
    max = np.max(f1)
    min = np.min(f1)
    return [avg, std, max, min]

def calculate_metrics(args):
    video1, fpsv1 = read_video(args.first)
    video2, fpsv2 = read_video(args.second)
    assert video1.shape == video2.shape, "Videos have different dimensions."
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel_process) as executor:
        futures = [executor.submit(process_frame_metric, f1, f2) for f1,f2 in zip(video1, video2)]
        metrics = np.array([future.result() for future in concurrent.futures.as_completed(futures)])
    return metrics

def calculate_stats(args):
    video1, fpsv1 = read_video(args.first)
    video2, fpsv2 = read_video(args.second)
    assert video1.shape == video2.shape, "Videos have different dimensions."
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel_process) as executor:
        futures = [executor.submit(process_frame_stats, f1) for f1 in video1]
        stats = np.array([future.result() for future in concurrent.futures.as_completed(futures)])
    return stats



def draw_metrics(metrics):
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
    axes[0].plot(metrics[:,0], color='red')
    axes[0].set_title('PSNR')
    axes[1].plot(metrics[:,1], color='blue')
    axes[1].set_title('SSIM')
    axes[2].plot(metrics[:,2], color='green')
    axes[2].set_title('VIF')
    plt.tight_layout()
    plt.show()



def draw_stats(stats):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))
    axes[0,0].plot(stats[:,0], color='red')
    axes[0,0].set_title('Average')
    axes[0,1].plot(stats[:,1], color='blue')
    axes[0,1].set_title('Standard Deviation')
    axes[1,0].plot(stats[:,2], color='green')
    axes[1,0].set_title('Maximum')
    axes[1,1].plot(stats[:,3], color='green')
    axes[1,1].set_title('Minimum')
    plt.tight_layout()
    plt.show()


def main():
    args = get_params()
    # diff_videos(args)
    calculate_psnr_ffmpeg(args)
    calculate_ssim_ffmpeg(args)
    # calculate_vmaf_ffmpeg(args)
    metrics = calculate_metrics(args)
    print(np.average(metrics, axis=0))
    draw_metrics(metrics)
    metrics = calculate_stats(args)
    print(np.average(metrics, axis=0))
    draw_stats(metrics)





if __name__ == '__main__':
    main()
