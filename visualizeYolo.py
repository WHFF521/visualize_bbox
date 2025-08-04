import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import os
from PIL import Image

# 配置默认路径
config = {
    'image_dir': r'D:\datasets\DOTASplitHbb\val_split_rate1.0_subsize1024_gap512\images',        # 图片文件夹
    'label_dir': r'D:\datasets\DOTASplitHbb\val_split_rate1.0_subsize1024_gap512\labels-yolo',        # 标签文件夹
    'img_ext': '.png',              # 图片扩展名
    'label_ext': '.txt'             # 标签扩展名
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, help='Path to image folder')
    parser.add_argument('--label', type=str, help='Path to label folder')
    args = parser.parse_args()
    args.image = args.image or config['image_dir']
    args.label = args.label or config['label_dir']
    return args

def read_yolo_label(label_path):
    bboxes = []
    if not os.path.exists(label_path):
        return bboxes
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            cls, x, y, w, h = map(float, parts)
            bboxes.append((int(cls), x, y, w, h))
    return bboxes

def draw_image(ax, image, bboxes, image_w, image_h):
    ax.clear()
    ax.imshow(image)
    for bbox in bboxes:
        cls_id, x_center, y_center, w, h = bbox
        x = (x_center - w / 2) * image_w
        y = (y_center - h / 2) * image_h
        width = w * image_w
        height = h * image_h
        rect = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)
        ax.text(x, y, f'{cls_id}', color='yellow', fontsize=8, verticalalignment='top')
    ax.set_xticks([])
    ax.set_yticks([])

def visualize(image_folder, label_folder):
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(config['img_ext'])])
    if not image_files:
        print("No image files found.")
        return

    idx = [0]
    fig, ax = plt.subplots(1)

    def update():
        ax.clear()
        img_file = image_files[idx[0]]
        img_path = os.path.join(image_folder, img_file)
        label_file = os.path.splitext(img_file)[0] + config['label_ext']
        label_path = os.path.join(label_folder, label_file)

        image = Image.open(img_path).convert('RGB')
        w, h = image.size
        bboxes = read_yolo_label(label_path)

        draw_image(ax, image, bboxes, w, h)
        ax.set_title(f"{img_file} ({idx[0]+1}/{len(image_files)})")
        fig.canvas.draw()

    def on_key(event):
        if event.key == 'right':
            idx[0] = (idx[0] + 1) % len(image_files)
            update()
        elif event.key == 'left':
            idx[0] = (idx[0] - 1) % len(image_files)
            update()
        elif event.key == 'escape':
            plt.close()

    fig.canvas.mpl_connect('key_press_event', on_key)
    update()
    plt.show()

if __name__ == '__main__':
    args = parse_args()
    visualize(args.image, args.label)
