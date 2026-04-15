import re
import os

class ImageMapper:
    def __init__(self):
        pass

    def map_images_to_observations(self, reasoned_data: dict, extracted_images: list) -> dict:
        """
        Maps extracted image paths to the area_wise_observations in the reasoned data.
        In a real-world scenario, this might use BLIP (Image Captioning) or compare the area text.
        For this prototype, we'll do a simple mapping based on availability and "Not Available" fallback.
        """
        # Make a copy to avoid mutating original during iteration
        updated_data = dict(reasoned_data)
        areas = updated_data.get("area_wise_observations", [])
        
        # Flatten image list from both Inspection and Thermal (if we grouped them previously)
        # Assuming extracted_images is a list of dicts: [ {"page": 1, "path": "...", "source": "Inspection"}, ...]
        
        available_images = list(extracted_images)
        
        for area_obs in areas:
            # Simple heuristic: Just map one image per area if available, else "Image Not Available"
            # Since we don't have BLIP configured, we will pop the first available image or map based on source.
            if available_images:
                img = available_images.pop(0)
                area_obs["image_path"] = img["path"]
            else:
                area_obs["image_path"] = "Image Not Available"
                
        updated_data["area_wise_observations"] = areas
        return updated_data
