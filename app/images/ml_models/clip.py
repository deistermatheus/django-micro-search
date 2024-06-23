from PIL import Image
from torch.linalg import vector_norm
from torch import div, flatten
from transformers import CLIPProcessor, CLIPModel

MODEL = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
PROCESSOR = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
EMBEDDING_SIZE = MODEL.projection_dim


def embed_image(image):
    image_data = Image.open(image)

    image_inputs = PROCESSOR(images=image_data, return_tensors="pt", padding=True)

    image_embeds = MODEL.get_image_features(**image_inputs)
    normed_image_embeds = div(image_embeds, vector_norm(image_embeds))

    return flatten(normed_image_embeds).tolist()
