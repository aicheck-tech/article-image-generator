import torch
from torch import nn
import clip
from PIL import Image


class ClipClassification(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        for param in self.model.parameters():
            param.requires_grad = False
        self.classification_head = ClassificationHead(num_classes=2).to(self.device)

    def forward(self, text: torch.Tensor, image: torch.Tensor) -> torch.Tensor:
        image_features = self.model.encode_image(image.to(self.device))
        text_features = self.model.encode_text(text.to(self.device))
        joint = torch.cat([image_features, text_features], dim=1)
        return self.classification_head(joint)

    def tokenize(self, text: str) -> torch.Tensor:
        return clip.tokenize(text, truncate=True)

    def convert_img(self, image: Image) -> torch.Tensor:
        return self.preprocess(image).unsqueeze(0)


class ClassificationHead(nn.Module):
    def __init__(self, num_classes: int = 2) -> torch.Tensor:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x.to(torch.float32))


class DeepConcatenationModel(nn.Module):
    """
    Concatenates the text and image features after passing them through a few layers
    Not used yet, but might be useful in the future.
    """
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

    def forward(self, text: torch.Tensor, img: torch.Tensor) -> torch.Tensor:
        text_vector = self.text_layer(text)
        img_vector = self.img_layer(img)
        return torch.cat([text_vector, img_vector], dim=1)


def load_classifiear() -> ClipClassification:
        classifier = ClipClassification()
        classifier.eval()
        # classifier.load_state_dict(torch.load("model.pth"))
        return classifier