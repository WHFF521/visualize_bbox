import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import os
import ast


config = {
    'csvpath': 'train.csv',
    'image_dir': './train',
    'image_id_col': 'image_id',
    'bbox_col': 'bbox'
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvpath', type=str, help='Path to CSV file')
    parser.add_argument('--image', type=str, help='Path to image folder')
    args = parser.parse_args()
    # 使用 config 中的默认值填补未传入的参数
    args.csvpath = args.csvpath or config['csvpath']
    args.image = args.image or config['image_dir']
    return args

def draw_image(ax, image, bboxes):
    ax.clear()
    ax.imshow(image)
    for bbox in bboxes:
        x, y, w, h = bbox
        rect = patches.Rectangle((x,y), w, h, linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)

def visualize(csv_path,image_folder):
    df = pd.read_csv(csv_path)
    df['bbox'] = df['bbox'].apply(ast.literal_eval)

    image_ids = df['image_id'].unique()
    idx = [0]

    fig, ax = plt.subplots(1)

    def update():
        ax.clear()
        image_id = image_ids[idx[0]]
        image_path = os.path.join(image_folder,image_id+'.jpg')
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return 
        image = plt.imread(image_path)
        image_id_col = config['image_id_col']
        bbox_col = config['bbox_col']
        bboxes = df[df[image_id_col] == image_id][bbox_col].tolist()
        draw_image(ax, image, bboxes)
        ax.set_title(f"{image_id} ({idx[0]+1}/{len(image_ids)})")
        fig.canvas.draw()
    
    def on_key(event):
        if event.key == 'right':
            idx[0] = (idx[0] + 1) % len(image_ids)
            update()
        elif event.key == 'left':
            idx[0] = (idx[0] - 1) % len(image_ids)
            update()
        elif event.key == 'escape':
            plt.close()
    fig.canvas.mpl_connect('key_press_event', on_key)
    update()
    plt.show()

if __name__ == '__main__':
    args = parse_args()
    visualize(args.csvpath, args.image)