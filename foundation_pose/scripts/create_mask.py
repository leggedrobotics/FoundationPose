import os
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
from segment_anything import sam_model_registry, SamPredictor


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(
        pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25
    )
    ax.scatter(
        neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25
    )


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))


def get_first_image_path(img_dir):
    first_image = sorted(os.listdir(img_dir))[0]
    return first_image, os.path.join(img_dir, first_image)


def onclick(event, points):
    print(f"Click at: {event.xdata}, {event.ydata}. Point added. Total points: {len(points)}")
    points.append((event.xdata, event.ydata))


# out_dir = "out"
out_dir = "/home/arjun/Desktop/mech/inhand_cube/markers/letters/FoundationPose/demo_data/cube"
image_dir = os.path.join(out_dir, "rgb")
image_name, image_path = get_first_image_path(image_dir)
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

points = []

plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis('on')
plt.connect('button_press_event', lambda event: onclick(event, points=points))
plt.show()

sam_checkpoint = "/home/arjun/Desktop/mech/inhand_cube/markers/letters/sam/weights/sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

print("Predicting...")
predictor = SamPredictor(sam)
predictor.set_image(image)
input_points = np.array(points)
input_labels = np.ones(input_points.shape[0])
masks, scores, logits = predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=False,
)

for i, (mask, score) in enumerate(zip(masks, scores)):
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    show_mask(mask, plt.gca())
    show_points(input_points, input_labels, plt.gca())
    plt.title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
    plt.axis('off')
    plt.show()

# Save the best masks
mask_id = np.argmax(scores)
best_mask = masks[mask_id]
subfolder_mask = os.path.join(out_dir, "masks")
if not os.path.exists(subfolder_mask):
    os.makedirs(subfolder_mask)
save_path = os.path.join(subfolder_mask, image_name.replace(".jpg", ".png"))
cv2.imwrite(save_path, (best_mask * 255).astype(np.uint8))
print(f"Best mask saved at: {save_path}")
