#!/usr/bin/python3
import cv2
import os
import sys

def script_path(subpath=''):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    if subpath:
        path = os.path.join(path, subpath)
    os.chdir(path)
    return path

def get_files(subpath=''):
    path = script_path(subpath)
    files = [item for item in os.listdir(path) if item.endswith((".jpg", ".png"))]
    files.sort()
    return files

def make_video(images, outvid="video.avi", fps=5, size=None,
               is_color=True, format="XVID"):
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    imNumber = len(images)
    for key, file in enumerate(images):
        print(file)
        img = cv2.imread(file)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
        #print("Progress: {0}%".format((key+1)/imNumber*100), end="\r", flush=True)
    cv2.destroyAllWindows()
    vid.release()
    return vid


if __name__ == "__main__":
    path = script_path()
    args = sys.argv[1:]
    dir = args[0]
    images = get_files(dir)
    if not images:
        print("no images in specified directory...")
        sys.exit()
    videoName = os.path.join(path, "video.avi")
    make_video(images, outvid=videoName, fps=10, is_color=True)
