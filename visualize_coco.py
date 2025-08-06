import os
import json
import cv2
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class CocoVisualizer:
    def __init__(self, json_path, image_dir):
        self.image_dir = image_dir
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        with open(json_path, 'r') as f:
            coco = json.load(f)

        self.images = {img['id']: img for img in coco['images']}
        self.categories = {cat['id']: cat['name'] for cat in coco['categories']}

        # 按 image_id 分组 annotations
        self.ann_by_image = {}
        for ann in coco['annotations']:
            self.ann_by_image.setdefault(ann['image_id'], []).append(ann)

        self.image_ids = sorted(self.images.keys())
        self.index = 0

        self.show_image()

    def show_image(self):
        self.ax.clear()
        image_info = self.images[self.image_ids[self.index]]
        file_name = image_info['file_name']
        image_path = os.path.join(self.image_dir, file_name)

        img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        self.ax.imshow(img)

        anns = self.ann_by_image.get(image_info['id'], [])
        for ann in anns:
            x, y, w, h = ann['bbox']
            cat_id = ann['category_id']
            label = self.categories.get(cat_id, 'unknown')

            rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='lime', facecolor='none')
            self.ax.add_patch(rect)
            self.ax.text(x, y - 5, label, fontsize=10, color='lime',
                         bbox=dict(facecolor='black', alpha=0.5, pad=1))

        self.ax.set_title(f"[{self.index + 1}/{len(self.image_ids)}] {file_name}\n← left, → right, q quit")
        self.ax.axis('off')
        self.fig.canvas.draw_idle()

    def on_key_press(self, event):
        if event.key == 'right':
            self.index = (self.index + 1) % len(self.image_ids)
            self.show_image()
        elif event.key == 'left':
            self.index = (self.index - 1) % len(self.image_ids)
            self.show_image()
        elif event.key == 'q':
            plt.close(self.fig)

def main():
    parser = argparse.ArgumentParser(description='交互式可视化 COCO 格式数据集，支持 ←/→/q 键控制')
    parser.add_argument('--json', required=True, help='COCO 格式标注文件路径')
    parser.add_argument('--image-dir', required=True, help='图片文件夹路径')
    args = parser.parse_args()

    vis = CocoVisualizer(args.json, args.image_dir)
    plt.show()

if __name__ == '__main__':
    main()

# python visualize_coco.py --json D:\datasets\global-wheat-detection\cocolabels\val.json --image-dir D:\datasets\global-wheat-detection\train