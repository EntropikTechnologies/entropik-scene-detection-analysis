from entropik_scene_detection_analysis.main import ProcessMedia
# media_path - Path to video path
detect_scene = ProcessMedia(media_path="/Users/uzair/Downloads/Ajio.webm")
print(detect_scene.get_scene_detection_analysis())
