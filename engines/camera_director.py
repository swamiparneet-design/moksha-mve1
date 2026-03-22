"""
CAMERA DIRECTION ENGINE - Professional Cinematography
Controls camera movements, angles, and dynamic framing
"""
from loguru import logger


class CameraDirector:
    """Professional camera movement and direction engine"""
    
    def __init__(self):
        self.logger = logger
        
        # Camera movements with emotional meaning
        self.camera_movements = {
            "SLOW_PUSH_IN": {
                "emotional_effect": "growing_tension_intimacy_focus",
                "when_to_use": ["realization_moments", "emotional_buildup", "important_revelations"],
                "speed": "very_slow_gradual",
                "duration_range": (3, 8)
            },
            "SLOW_PULL_OUT": {
                "emotional_effect": "isolation_reflection_ending",
                "when_to_use": ["scene_endings", "defeat_moments", "character_alone"],
                "speed": "slow_retreating",
                "duration_range": (4, 6)
            },
            "QUICK_PUSH_IN": {
                "emotional_effect": "shock_sudden_realization_intensity",
                "when_to_use": ["shocking_news", "sudden_emotion", "dramatic_moment"],
                "speed": "fast_aggressive",
                "duration_range": (1, 2)
            },
            "PAN_LEFT": {
                "emotional_effect": "transition_discovery_following",
                "when_to_use": ["character_movement", "revealing_new_element", "scene_transition"],
                "speed": "smooth_moderate",
                "duration_range": (2, 4)
            },
            "PAN_RIGHT": {
                "emotional_effect": "progression_forward_movement",
                "when_to_use": ["moving_forward", "following_action", "time_passage"],
                "speed": "smooth_moderate",
                "duration_range": (2, 4)
            },
            "TILT_UP": {
                "emotional_effect": "empowerment_revelation_looking_up",
                "when_to_use": ["character_standing_tall", "seeing_something_grand", "hope"],
                "speed": "slow_uplifting",
                "duration_range": (2, 5)
            },
            "TILT_DOWN": {
                "emotional_effect": "defeat_sadness_heaviness",
                "when_to_use": ["defeated_moments", "looking_down", "sadness"],
                "speed": "slow_heavy",
                "duration_range": (2, 4)
            },
            "RACK_FOCUS": {
                "emotional_effect": "shift_in_attention_realization",
                "when_to_use": ["focus_change", "understanding_dawns", "detail_importance"],
                "speed": "smooth_deliberate",
                "duration_range": (2, 4)
            },
            "HANDHELD_SHAKE": {
                "emotional_effect": "tension_unrest_instability",
                "when_to_use": ["conflict_scenes", "anxiety", "documentary_realism"],
                "speed": "subtle_shake",
                "duration_range": (3, 10)
            },
            "STATIC_LOCKED": {
                "emotional_effect": "stability_formality_contemplation",
                "when_to_use": ["formal_moments", "meditative_scenes", "stable_dialogue"],
                "speed": "no_movement",
                "duration_range": (2, 8)
            },
            "ZOOM_IN": {
                "emotional_effect": "intensification_focus_pressure",
                "when_to_use": ["building_tension", "emphasis", "confrontation"],
                "speed": "gradual_or_fast",
                "duration_range": (2, 6)
            },
            "ZOOM_OUT": {
                "emotional_effect": "release_context_ending",
                "when_to_use": ["scene_conclusion", "emotional_release", "bigger_picture"],
                "speed": "gradual",
                "duration_range": (3, 6)
            }
        }
        
        # Emotion to camera movement mapping
        self.emotion_camera_map = {
            "joy": ["SLOW_PUSH_IN", "PAN_RIGHT", "TILT_UP"],
            "sadness": ["SLOW_PULL_OUT", "TILT_DOWN", "STATIC_LOCKED"],
            "anger": ["QUICK_PUSH_IN", "HANDHELD_SHAKE", "ZOOM_IN"],
            "fear": ["HANDHELD_SHAKE", "QUICK_PUSH_IN", "RACK_FOCUS"],
            "surprise": ["QUICK_PUSH_IN", "RACK_FOCUS", "ZOOM_IN"],
            "love": ["SLOW_PUSH_IN", "RACK_FOCUS", "STATIC_LOCKED"],
            "pride": ["TILT_UP", "SLOW_PUSH_IN", "STATIC_LOCKED"],
            "gratitude": ["SLOW_PUSH_IN", "STATIC_LOCKED", "TILT_UP"],
            "hope": ["TILT_UP", "PAN_RIGHT", "SLOW_PUSH_IN"],
            "determination": ["SLOW_PUSH_IN", "ZOOM_IN", "STATIC_LOCKED"],
            "nostalgia": ["SLOW_PULL_OUT", "PAN_LEFT", "SOFT_FOCUS"],
            "sangharsh": ["HANDHELD_SHAKE", "SLOW_PUSH_IN", "TILT_UP"],
            "tyaag": ["SLOW_PULL_OUT", "STATIC_LOCKED", "TILT_DOWN"],
            "karuna": ["SLOW_PUSH_IN", "CLOSE_UP_HOLD", "STATIC_LOCKED"]
        }
        
        # Scene type preferences
        self.scene_type_camera_prefs = {
            "dialogue": {
                "primary": "STATIC_LOCKED",
                "secondary": "SLOW_PUSH_IN",
                "avoid_quick_movements": True
            },
            "monologue": {
                "primary": "SLOW_PUSH_IN",
                "dynamic": True
            },
            "action": {
                "primary": "HANDHELD_SHAKE",
                "quick_cuts": True
            },
            "contemplative": {
                "primary": "STATIC_LOCKED",
                "long_takes": True
            }
        }
    
    def assign_camera_movements(self, scenes: list, style: str = "educational") -> list:
        """
        Assign camera movements to all scenes
        
        Args:
            scenes: List of scene dictionaries with emotion
            style: Video style
            
        Returns:
            Enhanced scenes with camera directions
        """
        self.logger.info(f"🎥 Assigning camera movements to {len(scenes)} scenes")
        
        enhanced_scenes = []
        
        for i, scene in enumerate(scenes):
            try:
                emotion = scene.get("emotion", "neutral")
                
                # Get primary camera movement for emotion
                camera_options = self.emotion_camera_map.get(emotion, self.emotion_camera_map["neutral"])
                
                # Consider scene position
                if i == 0:
                    # Opening scene - establish with stability
                    primary_camera = "STATIC_LOCKED"
                elif i == len(scenes) - 1:
                    # Ending scene - pull out or static
                    primary_camera = "SLOW_PULL_OUT" if "sadness" in emotion else "STATIC_LOCKED"
                else:
                    # Middle scenes - use emotion-based choice
                    primary_camera = camera_options[0]
                
                # Get movement details
                movement_details = self.camera_movements.get(primary_camera, {})
                
                # Create enhanced scene
                enhanced_scene = {
                    **scene,
                    "camera_movement": primary_camera,
                    "camera_effect": movement_details.get("emotional_effect", "focus_change"),
                    "camera_speed": movement_details.get("speed", "moderate"),
                    "movement_duration": movement_details.get("duration_range", (2, 4)),
                    "scene_number": i + 1
                }
                
                enhanced_scenes.append(enhanced_scene)
                
            except Exception as e:
                self.logger.error(f"Camera assignment failed for scene {i}: {e}")
                scene["camera_movement"] = "STATIC_LOCKED"
                enhanced_scenes.append(scene)
        
        self.logger.success(f"✅ Camera movements assigned to {len(enhanced_scenes)} scenes")
        return enhanced_scenes
    
    def create_dynamic_shot_sequence(self, scene: dict) -> list:
        """
        Create dynamic camera sequence within a single scene
        
        Returns list of camera changes with timing
        """
        
        emotion = scene.get("emotion", "neutral")
        duration = scene.get("duration_estimate", 5)
        
        sequences = []
        
        # Build sequence based on emotion and duration
        if emotion in ["sadness", "nostalgia", "tyaag"]:
            # Slow retreat pattern
            sequences = [
                {"time": 0.0, "movement": "STATIC_LOCKED", "intensity": 0.3},
                {"time": duration * 0.3, "movement": "SLOW_PULL_OUT", "intensity": 0.5},
                {"time": duration * 0.7, "movement": "CONTINUE_PULL_OUT", "intensity": 0.7}
            ]
        
        elif emotion in ["anger", "fear", "sangharsh"]:
            # Tension building pattern
            sequences = [
                {"time": 0.0, "movement": "HANDHELD_SHAKE", "intensity": 0.4},
                {"time": duration * 0.4, "movement": "SLOW_PUSH_IN", "intensity": 0.6},
                {"time": duration * 0.8, "movement": "QUICK_PUSH_IN", "intensity": 0.9}
            ]
        
        elif emotion in ["joy", "hope", "love"]:
            # Uplifting pattern
            sequences = [
                {"time": 0.0, "movement": "SLOW_PUSH_IN", "intensity": 0.5},
                {"time": duration * 0.5, "movement": "TILT_UP", "intensity": 0.7},
                {"time": duration * 0.9, "movement": "HOLD_STATIC", "intensity": 0.6}
            ]
        
        else:
            # Neutral/standard pattern
            sequences = [
                {"time": 0.0, "movement": "STATIC_LOCKED", "intensity": 0.3},
                {"time": duration * 0.6, "movement": "VERY_SLOW_PUSH_IN", "intensity": 0.5}
            ]
        
        return sequences
    
    def generate_camera_direction_script(self, enhanced_scenes: list) -> str:
        """Generate professional camera direction script"""
        
        script_lines = []
        script_lines.append("="*70)
        script_lines.append("CAMERA DIRECTION SCRIPT - PROFESSIONAL PRODUCTION")
        script_lines.append("="*70)
        script_lines.append("")
        
        for scene in enhanced_scenes:
            scene_num = scene.get("scene_number", "?")
            shot_type = scene.get("shot_type", "MEDIUM_SHOT")
            camera_move = scene.get("camera_movement", "STATIC")
            emotion = scene.get("emotion", "neutral")
            
            script_lines.append(f"SCENE {scene_num}:")
            script_lines.append(f"  Shot: {shot_type}")
            script_lines.append(f"  Camera Movement: {camera_move}")
            script_lines.append(f"  Emotional Effect: {scene.get('camera_effect', 'focus')}")
            script_lines.append(f"  Emotion: {emotion}")
            script_lines.append(f"  Duration: {scene.get('duration_estimate', 0)}s")
            
            # Add dynamic sequence if available
            if "dynamic_sequence" in scene:
                script_lines.append(f"  Dynamic Sequence:")
                for step in scene["dynamic_sequence"]:
                    script_lines.append(f"    {step['time']:.1f}s: {step['movement']} (intensity: {step['intensity']})")
            
            script_lines.append("")
        
        return "\n".join(script_lines)


# Test function
def test_camera_director():
    """Test camera director engine"""
    director = CameraDirector()
    
    test_scenes = [
        {"text": "Opening", "emotion": "neutral", "duration_estimate": 4},
        {"text": "Happy news", "emotion": "joy", "duration_estimate": 5},
        {"text": "Sad moment", "emotion": "sadness", "duration_estimate": 6},
        {"text": "Struggle", "emotion": "sangharsh", "duration_estimate": 5},
        {"text": "Hope rises", "emotion": "hope", "duration_estimate": 4}
    ]
    
    print("\n🎥 Testing Camera Director")
    print("="*60)
    
    enhanced = director.assign_camera_movements(test_scenes)
    
    for scene in enhanced:
        print(f"Scene {scene['scene_number']}: {scene['camera_movement']} ({scene['camera_effect']})")
    
    print("\n" + "="*70)
    print(director.generate_camera_direction_script(enhanced))
    
    print("\n✅ Camera Director test complete!")


if __name__ == "__main__":
    test_camera_director()
