import torch
from torch import nn
import clip
from PIL import Image


class Clip_classification(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        for param in self.model.parameters():
            param.requires_grad = False
        self.classification_head = Classification_head(2).to(self.device)

    def forward(self, text: torch.Tensor, image: torch.Tensor) -> None:
        image_features = self.model.encode_image(image.to(self.device))
        text_features = self.model.encode_text(text.to(self.device))
        joint = torch.cat([image_features, text_features], dim=1)
        x = self.classification_head(joint)
        return x

    def tokenize(self, text) -> torch.Tensor:
        return clip.tokenize(text)

    def convert_img(self, path: str) -> torch.Tensor:
        image = self.preprocess(Image.open(path)).unsqueeze(0)  # type: ignore
        return image


class Classification_head(nn.Module):
    def __init__(self, num_classes=2) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024, 512).to(torch.float16),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256).to(torch.float16),
            nn.ReLU(),
            nn.Linear(256, 128).to(torch.float16),
            nn.ReLU(),
            nn.Linear(128, num_classes).to(torch.float16)
        )

    def forward(self, x):
        x = self.layers(x)
        return x


# Not used yet
class DeepConcatenationModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.text_layer = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 768),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(768, 1024),
            )
        self.img_layer = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 768),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(768, 1024),
            )

    def forward(self, text, img):
        text = self.text_layer(text)
        img = self.img_layer(img)
        x = torch.cat([text, img], dim=1)
        return x
