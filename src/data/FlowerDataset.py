from glob import glob
from os import path
from typing import Optional

import numpy as np
import torch
from torch.utils.data import Dataset


class FlowerDataset(Dataset):
    """
    Flower dataset
    """

    def __init__(self, flowers_path: str, size: str, split: Optional[str] = "train"):
        """
        Constructs a Dataset from PyTorch tensors located at `flowers_path`.

        Args
            flowers_path : str
                Path to folder containing .pt files.
            size : str
                Image size, e.g., 224x224
            split : str
                `test` or `train`
        """
        files = glob(path.join(flowers_path, split, size, f"{size}-*.pt"))
        self.split = split
        self.ids = []
        self.images = []
        self.classes = []

        for file in files:
            t = torch.load(file)
            self.ids += t["ids"]
            self.images += t["images"]
            if split != "test":
                self.classes += t["classes"]

        self.images = torch.from_numpy(np.array(self.images))  # N x H? x W? x C
        self.images = self.images.permute(0, 3, 1, 2)  # N x C x H? x W?
        if self.split != "test":
            self.classes = torch.from_numpy(np.array(self.classes))

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, idx):
        if self.split == "test":
            return self.images[idx], None
        return self.images[idx], self.classes[idx]