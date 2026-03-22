"""
SHOT STRUCTURE ENGINE - Professional Cinematography
Automatically assigns shot types, camera angles, and framing based on emotion and context
"""
from loguru import logger
from config import Config


class ShotStructureEngine:
    """Professional shot selection and composition engine"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        
        # Shot type definitions with emotional impact
        self.shot_types = {
            "EXTREME_WIDE_SHOT": {
                "purpose": "establish_location_context",
                "emotional_impact": "isolation_smallness_epic_scale",
                "duration_range": (4, 6),
                "when_to_use": ["opening_scenes", "location_change", "epic_moments"],
                "camera_distance": "far_away",
                "subject_size": "very_small_in_frame"
            },
            "WIDE_SHOT": {
                "purpose": "show_full_scene_action",
                "emotional_impact": "context_environment_activity",
                "duration_range": (3, 5),
                "when_to_use": ["scene_establishing", "group_interactions", "action_sequences"],
                "camera_distance": "full_body_visible",
                "subject_size": "complete_in_frame"
            },
            "MEDIUM_LONG_SHOT": {
                "purpose": "balance_subject_environment",
                "emotional_impact": "narrative_flow_context_with_focus",
                "duration_range": (3, 4),
                "when_to_use": ["walking_shots", "entrance_exit", "casual_conversations"],
                "camera_distance": "knees_up",
                "subject_size": "majority_of_frame"
            },
            "MEDIUM_SHOT": {
                "purpose": "dialogue_interaction",
                "emotional_impact": "personal_connection_engagement",
                "duration_range": (2, 4),
                "when_to_use": ["conversations", "interviews", "explanations"],
                "camera_distance": "waist_up",
                "subject_size": "upper_body_focused"
            },
            "MEDIUM_CLOSE_UP": {
                "purpose": "focus_on_expression_reaction",
                "emotional_impact": "intimacy_emotional_connection",
                "duration_range": (2, 3),
                "when_to_use": ["emotional_dialogue", "reactions", "important_revelations"],
                "camera_distance": "chest_up",
                "subject_size": "face_and_shoulders_dominant"
            },
            "CLOSE_UP": {
                "purpose": "intense_emotion_detail",
                "emotional_impact": "intimacy_intensity_vulnerability",
                "duration_range": (2, 3),
                "when_to_use": ["emotional_peaks", "critical_moments", "realizations"],
                "camera_distance": "head_only",
                "subject_size": "face_fills_frame"
            },
            "EXTREME_CLOSE_UP": {
                "purpose": "maximum_intensity_micro_expression",
                "emotional_impact": "raw_emotion_unbearable_intimacy",
                "duration_range": (1, 2),
                "when_to_use": ["climax_moments", "life_changing_revelations", "tears"],
                "camera_distance": "eyes_mouth_or_detail",
                "subject_size": "single_feature_dominates"
            },
            "OVER_SHOULDER_SHOT": {
                "purpose": "conversation_perspective",
                "emotional_impact": "involvement_observer_feeling",
                "duration_range": (3, 4),
                "when_to_use": ["two_person_dialogue", "confrontations", "teaching_moments"],
                "camera_distance": "behind_one_person",
                "subject_size": "other_person_focused"
            },
            "POINT_OF_VIEW_SHOT": {
                "purpose": "audience_becomes_character",
                "emotional_impact": "immersion_empathy_understanding",
                "duration_range": (2, 4),
                "when_to_use": ["character_perspective", "discovery_moments", "shocking_reveals"],
                "camera_distance": "through_character_eyes",
                "subject_size": "what_character_sees"
            }
        }
        
        # Emotion to shot mapping
        self.emotion_shot_map = {
            "joy": ["MEDIUM_SHOT", "CLOSE_UP", "WIDE_SHOT"],
            "sadness": ["CLOSE_UP", "MEDIUM_CLOSE_UP", "EXTREME_CLOSE_UP"],
            "anger": ["MEDIUM_SHOT", "CLOSE_UP", "OVER_SHOULDER_SHOT"],
            "fear": ["CLOSE_UP", "POINT_OF_VIEW_SHOT", "EXTREME_CLOSE_UP"],
            "surprise": ["MEDIUM_SHOT", "CLOSE_UP", "WIDE_SHOT"],
            "love": ["MEDIUM_CLOSE_UP", "CLOSE_UP", "OVER_SHOULDER_SHOT"],
            "pride": ["MEDIUM_SHOT", "WIDE_SHOT", "MEDIUM_LONG_SHOT"],
            "gratitude": ["MEDIUM_CLOSE_UP", "CLOSE_UP", "MEDIUM_SHOT"],
            "hope": ["WIDE_SHOT", "MEDIUM_SHOT", "MEDIUM_LONG_SHOT"],
            "determination": ["MEDIUM_SHOT", "CLOSE_UP", "MEDIUM_CLOSE_UP"],
            "nostalgia": ["WIDE_SHOT", "MEDIUM_LONG_SHOT", "MEDIUM_SHOT"],
            "sangharsh": ["MEDIUM_SHOT", "CLOSE_UP", "WIDE_SHOT"],
            "vatsalya_bhavna": ["MEDIUM_CLOSE_UP", "CLOSE_UP", "OVER_SHOULDER_SHOT"],
            "shraddha": ["MEDIUM_SHOT", "WIDE_SHOT", "MEDIUM_CLOSE_UP"],
            "tyaag": ["CLOSE_UP", "MEDIUM_CLOSE_UP", "MEDIUM_SHOT"],
            "karuna": ["CLOSE_UP", "MEDIUM_CLOSE_UP", "EXTREME_CLOSE_UP"],
            "bhakti": ["MEDIUM_SHOT", "CLOSE_UP", "WIDE_SHOT"],
            "desh_bhakti": ["WIDE_SHOT", "MEDIUM_SHOT", "MEDIUM_LONG_SHOT"],
            "parivaar_prem": ["MEDIUM_SHOT", "OVER_SHOULDER_SHOT", "MEDIUM_CLOSE_UP"]
        }
        
        # Scene style to shot preferences
        self.style_shot_preferences = {
            "educational": {
                "primary": "MEDIUM_SHOT",
                "secondary": "CLOSE_UP",
                "avoid": ["EXTREME_CLOSE_UP"]
            },
            "story": {
                "primary": "MEDIUM_CLOSE_UP",
                "secondary": "CLOSE_UP",
                "variety": True
            },
            "news": {
                "primary": "MEDIUM_SHOT",
                "secondary": "WIDE_SHOT",
                "formal": True
            },
            "vlog": {
                "primary": "CLOSE_UP",
                "secondary": "MEDIUM_SHOT",
                "handheld_feel": True
            },
            "documentary": {
                "primary": "WIDE_SHOT",
                "secondary": "MEDIUM_SHOT",
                "observational": True
            }
        }
    
    def assign_shot_structure(self, scenes: list, soul_data: dict = None, style: str = "educational") -> list:
        """
        Assign shot types to all scenes based on emotion, soul, and style
        
        Args:
            scenes: List of scene dictionaries
            soul_data: Emotional core from Soul Extractor
            style: Video style (educational/story/news/vlog)
            
        Returns:
            Enhanced scenes with shot structure
        """
        self.logger.info(f"🎬 Assigning shot structure to {len(scenes)} scenes")
        
        enhanced_scenes = []
        
        for i, scene in enumerate(scenes):
            try:
                # Get scene emotion
                emotion = scene.get("emotion", "neutral")
                
                # Determine primary shot type
                if soul_data and "powerful_moment" in soul_data:
                    # Check if this is the powerful moment
                    is_powerful = self._is_powerful_moment(scene, i, len(scenes))
                    if is_powerful:
                        shot_type = "CLOSE_UP"  # Maximum impact
                    else:
                        shot_type = self._get_shot_for_emotion(emotion, style)
                else:
                    shot_type = self._get_shot_for_emotion(emotion, style)
                
                # Get shot details
                shot_details = self.shot_types.get(shot_type, self.shot_types["MEDIUM_SHOT"])
                
                # Calculate duration
                duration_min, duration_max = shot_details["duration_range"]
                estimated_duration = scene.get("duration_estimate", 3)
                
                # Clamp duration within range
                final_duration = max(duration_min, min(duration_max, estimated_duration))
                
                # Create enhanced scene
                enhanced_scene = {
                    **scene,
                    "shot_type": shot_type,
                    "shot_purpose": shot_details["purpose"],
                    "emotional_impact": shot_details["emotional_impact"],
                    "camera_distance": shot_details["camera_distance"],
                    "subject_size": shot_details["subject_size"],
                    "duration_estimate": final_duration,
                    "scene_number": i + 1
                }
                
                enhanced_scenes.append(enhanced_scene)
                
            except Exception as e:
                self.logger.error(f"Shot assignment failed for scene {i}: {e}")
                # Fallback to medium shot
                scenes[i]["shot_type"] = "MEDIUM_SHOT"
                scenes[i]["shot_purpose"] = "default_safe_choice"
                enhanced_scenes.append(scenes[i])
        
        self.logger.success(f"✅ Shot structure assigned to {len(enhanced_scenes)} scenes")
        return enhanced_scenes
    
    def _get_shot_for_emotion(self, emotion: str, style: str) -> str:
        """Get best shot type for given emotion"""
        
        # Get style preferences
        style_prefs = self.style_shot_preferences.get(style, self.style_shot_preferences["educational"])
        
        # Get emotion-based shots
        emotion_shots = self.emotion_shot_map.get(emotion, self.emotion_shot_map["neutral"])
        
        # Find intersection with style preferences
        for preferred_shot in [style_prefs["primary"], style_prefs["secondary"]]:
            if preferred_shot in emotion_shots:
                return preferred_shot
        
        # If no intersection, use emotion's first choice
        return emotion_shots[0] if emotion_shots else "MEDIUM_SHOT"
    
    def _is_powerful_moment(self, scene: dict, index: int, total_scenes: int) -> bool:
        """Detect if this scene is likely the powerful moment"""
        
        # Simple heuristic: middle of video + high emotion intensity
        middle_third = total_scenes // 3 <= index <= 2 * total_scenes // 3
        
        # Check for intense emotions
        intense_emotions = ["sadness", "anger", "love", "sangharsh", "tyaag", "karuna"]
        is_emotional = scene.get("emotion", "neutral") in intense_emotions
        
        # Check for dialogue intensity
        text = scene.get("text", "")
        is_short_powerful = len(text.split()) < 15 and any(word in text.lower() for word in ["love", "death", "sacrifice", "jeet", "haar"])
        
        return middle_third and (is_emotional or is_short_powerful)
    
    def get_shot_sequence(self, scene_type: str, emotion_flow: list) -> list:
        """
        Generate dynamic shot sequence for a scene
        
        Args:
            scene_type: Type of scene (dialogue/action/monologue)
            emotion_flow: List of emotions through the scene
            
        Returns:
            List of shot changes with timestamps
        """
        
        shot_sequence = []
        
        if scene_type == "dialogue":
            # Classic shot-reverse-shot pattern
            shot_sequence = [
                {"time": 0.0, "shot": "MEDIUM_SHOT", "description": "Establish both characters"},
                {"time": 2.0, "shot": "OVER_SHOULDER_SHOT", "description": "Speaker 1"},
                {"time": 4.0, "shot": "OVER_SHOULDER_SHOT", "description": "Speaker 2 reaction"},
                {"time": 6.0, "shot": "MEDIUM_CLOSE_UP", "description": "Key response"},
                {"time": 8.0, "shot": "CLOSE_UP", "description": "Emotional peak"}
            ]
        
        elif scene_type == "emotional_monologue":
            # Slow push-in pattern
            shot_sequence = [
                {"time": 0.0, "shot": "MEDIUM_LONG_SHOT", "description": "Start distant"},
                {"time": 3.0, "shot": "MEDIUM_SHOT", "description": "Moving closer"},
                {"time": 6.0, "shot": "MEDIUM_CLOSE_UP", "description": "Intimate"},
                {"time": 9.0, "shot": "CLOSE_UP", "description": "Full emotion"},
                {"time": 12.0, "shot": "EXTREME_CLOSE_UP", "description": "Peak intensity"}
            ]
        
        elif scene_type == "action":
            # Dynamic cutting pattern
            shot_sequence = [
                {"time": 0.0, "shot": "WIDE_SHOT", "description": "Establish action space"},
                {"time": 1.5, "shot": "MEDIUM_SHOT", "description": "Action begins"},
                {"time": 3.0, "shot": "CLOSE_UP", "description": "Critical detail"},
                {"time": 4.0, "shot": "WIDE_SHOT", "description": "Result/consequence"},
                {"time": 5.5, "shot": "MEDIUM_SHOT", "description": "Reaction"}
            ]
        
        return shot_sequence
    
    def generate_shot_list_for_video(self, enhanced_scenes: list) -> str:
        """Generate professional shot list document"""
        
        shot_list = []
        shot_list.append("="*60)
        shot_list.append("SHOT LIST - PROFESSIONAL VIDEO PRODUCTION")
        shot_list.append("="*60)
        shot_list.append("")
        
        for scene in enhanced_scenes:
            scene_num = scene.get("scene_number", "?")
            shot_type = scene.get("shot_type", "UNKNOWN")
            purpose = scene.get("shot_purpose", "N/A")
            emotion = scene.get("emotion", "neutral")
            duration = scene.get("duration_estimate", 0)
            
            shot_list.append(f"SCENE {scene_num}:")
            shot_list.append(f"  Shot Type: {shot_type}")
            shot_list.append(f"  Purpose: {purpose}")
            shot_list.append(f"  Emotion: {emotion}")
            shot_list.append(f"  Duration: {duration}s")
            shot_list.append(f"  Camera Distance: {scene.get('camera_distance', 'N/A')}")
            shot_list.append(f"  Subject Size: {scene.get('subject_size', 'N/A')}")
            shot_list.append("")
        
        return "\n".join(shot_list)


# Test function
def test_shot_structure():
    """Test shot structure engine"""
    engine = ShotStructureEngine()
    
    # Mock scenes
    test_scenes = [
        {"text": "Introduction", "emotion": "neutral", "duration_estimate": 5},
        {"text": "Happy moment", "emotion": "joy", "duration_estimate": 4},
        {"text": "Sad revelation", "emotion": "sadness", "duration_estimate": 6},
        {"text": "Angry confrontation", "emotion": "anger", "duration_estimate": 5},
        {"text": "Hopeful conclusion", "emotion": "hope", "duration_estimate": 4}
    ]
    
    print("\n🎬 Testing Shot Structure Engine")
    print("="*60)
    
    # Test with educational style
    enhanced = engine.assign_shot_structure(test_scenes, style="educational")
    
    print("\nEducational Style:")
    for scene in enhanced:
        print(f"  Scene {scene['scene_number']}: {scene['shot_type']} ({scene['emotional_impact']})")
    
    # Test with story style
    enhanced_story = engine.assign_shot_structure(test_scenes, style="story")
    
    print("\nStory Style:")
    for scene in enhanced_story:
        print(f"  Scene {scene['scene_number']}: {scene['shot_type']} ({scene['emotional_impact']})")
    
    # Generate shot list
    print("\n" + "="*60)
    print(engine.generate_shot_list_for_video(enhanced))
    
    print("\n✅ Shot Structure Engine test complete!")


if __name__ == "__main__":
    test_shot_structure()
