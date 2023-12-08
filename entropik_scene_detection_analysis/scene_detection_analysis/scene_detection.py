from typing import Any
import os
import re
from PIL import Image
import imagehash
import numpy as np
from scenedetect import detect, AdaptiveDetector
import scenedetect.frame_timecode
import logging
from entropik_scene_detection_analysis.common.error_handler import ErrorHandler
logging.basicConfig(filename='scene_detection_analysis.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



PRECISION = 3


def convert_timestamp_to_milliseconds(timestamp: str) -> int:
    try:
        hours, minutes, rest = timestamp.split(':')
        seconds, milliseconds = map(int, rest.split('.'))
        total_milliseconds = (int(hours) * 3600 + int(minutes) * 60 + seconds) * 1000 + milliseconds
        return total_milliseconds
    except ValueError as e:
        logging.info(f"Error converting timestamp: {e}")
        return 0


class SceneDetection:
    def __init__(self, media_path: str):
        if not os.path.exists(media_path):
            raise ErrorHandler("ENT-DS-ESDA-01", "The media path or file name is not valid.")
        self.media_path = media_path
        logging.info(f"The input media file path is : {self.media_path}")

    def get_scenes_from_media(self) -> Any:
        try:
            # logger.info(f"Input file is located at :{self.media_path}")
            scene_lists = detect(self.media_path,
                                 AdaptiveDetector(adaptive_threshold=2, min_content_val=5.0, window_width=1))
            logging.info("Scenes Detection Successful.")
            return scene_lists
        except Exception as e:
            logging.info(f"Error getting scenes from media: {e}")
            raise ErrorHandler("ENT-DS-ESDA-02", "Scenes extraction from media is failed.")

    def calculate_hash_similarity(self, image1, image2):
        # Convert images to numpy arrays
        array1 = np.array(image1)
        array2 = np.array(image2)

        # Calculate hash similarity
        hash1 = imagehash.average_hash(Image.fromarray(array1))
        hash2 = imagehash.average_hash(Image.fromarray(array2))

        # Normalized Hamming distance
        similarity = 1.0 - (hash1 - hash2) / max(len(hash1.hash), len(hash2.hash))

        # Ensure the similarity score is within [0, 1]
        similarity = max(0, similarity)
        similarity = min(1, similarity)

        return similarity

    def process_images_in_directory(self, directory_path):
        # Get a list of image files in the directory
        image_files = [f for f in os.listdir(directory_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        image_files.sort()  # Sort files for consistent order

        # Iterate through pairs of consecutive images
        for i in range(len(image_files) - 1):
            current_image_path = os.path.join(directory_path, image_files[i])
            next_image_path = os.path.join(directory_path, image_files[i + 1])

            # Load images
            current_image = Image.open(current_image_path)
            next_image = Image.open(next_image_path)

            # Calculate hash similarity score
            similarity_score = self.calculate_hash_similarity(current_image, next_image)

            # Delete one of the images if similarity score is >= 0.75
            if similarity_score >= 0.75:
                os.remove(current_image_path)

    def get_frame_numbers_from_directory(self, directory_path):
        # Get a list of image files in the directory
        image_files = [f for f in os.listdir(directory_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # Extract frame numbers from filenames
        frame_numbers = [self.get_frame_number_from_filename(filename) for filename in image_files]

        # Filter out None values (in case some filenames don't match the pattern)
        frame_numbers = [frame_number for frame_number in frame_numbers if frame_number is not None]

        return frame_numbers

    def get_frame_number_from_filename(self, filename):
        try:
            # Extract frame number using a regular expression
            match = re.search(r'frame_scene_(\d+)\.jpg', filename)
            if match:
                return int(match.group(1))
            else:
                raise ErrorHandler("ENT-DS-ESDA-04", "Frame number not found in filename.")
        except Exception as e:
            logging.error(f"Error extracting frame number from filename: {e}")
            raise ErrorHandler("ENT-DS-ESDA-05", "Error extracting frame number from filename.")

    def process_frame_data(self, target_path) -> list[dict[str, int]]:
        try:
            scenes_list = self.get_scenes_from_media()
            data = [
                [convert_timestamp_to_milliseconds(scene.get_timecode(precision=PRECISION, use_rounding=True)),
                 scene.get_frames()]
                for scenes in scenes_list
                for scene in scenes
            ]
            frame_results = [
                {"start_time": data[i][0], "end_time": data[i + 1][0], "frame_number": data[i + 1][1]}
                for i in range(0, len(data) - 1, 2)
            ]
            for frame_info in frame_results:
                frame_number = frame_info['frame_number']
                output_frame_path = os.path.join(target_path, f'frame_scene_{frame_number}.jpg')
                command = f'ffmpeg -hide_banner -loglevel panic -i {self.media_path} -vf "select=eq(n\,{frame_number}-1)" -vframes 1 {output_frame_path}'
                os.system(command)
            self.process_images_in_directory(target_path)
            directory_frame_numbers = self.get_frame_numbers_from_directory(target_path)

            # Filter based on matching frame numbers
            frame_results = [item for item in frame_results if item['frame_number'] in directory_frame_numbers]

            # Update timestamps in case frames were deleted
            for i, frame_info in enumerate(frame_results[:-1]):
                if frame_results[i]['end_time'] != frame_results[i + 1]['start_time']:
                    frame_results[i + 1]['start_time'] = frame_results[i]['end_time']

            logging.info("Scene detection analysis results are consolidated and processed successfully.")
            return frame_results
        except Exception as e:
            raise ErrorHandler("ENT-DS-ESDA-03", "Scene detection algorithm failed while consolidating the results")
            return None


if __name__ == "__main__":
    media_path = os.path.join("/Users/uzair/Downloads", "Ajio.webm")
    x = SceneDetection(media_path)
    results = x.process_frame_data('/Users/trinija/PycharmProject/scene_detection_package_addition1/entropik-scene-detection-analysis/frames_output')
    print("detected_scenes_results:", results)
