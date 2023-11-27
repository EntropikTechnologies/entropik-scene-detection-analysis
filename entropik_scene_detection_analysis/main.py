from entropik_scene_detection_analysis.scene_detection_analysis.scene_detection import (
    SceneDetection,
)


class ProcessMedia:
    """
    This class ProcessMedia process the media data and extract the scene detection analysis.
    """

    def __init__(self, media_path: str):
        self.media_path = media_path

    def get_scene_detection_analysis(self):
        """
        Extracts scene detection analysis from the media file.

        Returns:
        dict: A dictionary containing the scene detection analysis results.
        """
        scene_detection = SceneDetection(self.media_path)
        scene_detection_results = scene_detection.process_frame_data()
        return scene_detection_results


if __name__ == "__main__":
    process_scenes = ProcessMedia(media_path="/Users/uzair/Downloads/Ajio.webm")
    results = process_scenes.get_scene_detection_analysis()
    print("results: ", results)
