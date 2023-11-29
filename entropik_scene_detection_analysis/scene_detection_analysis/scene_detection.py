from typing import Any
import os
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

    def process_frame_data(self) -> list[dict[str, int]]:
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
            logging.info("Scene detection analysis results are consolidated and processed successfully.")
            return frame_results
        except Exception as e:
            raise ErrorHandler("ENT-DS-ESDA-03", "Scene detection algorithm failed while consolidating the results")
            return None


if __name__ == "__main__":
    media_path = os.path.join("/Users/uzair/Downloads", "Ajio.webm")
    x = SceneDetection(media_path)
    results = x.process_frame_data()
    print("detected_scenes_results:", results)
