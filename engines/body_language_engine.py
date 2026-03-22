"""
BODY LANGUAGE ENGINE - Professional Non-Verbal Communication
Complete body animation system for realistic human movement
Production-ready with cultural authenticity
"""
import random
from pathlib import Path
from loguru import logger
from config import Config


class BodyLanguageEngine:
    """Professional body language and gesture engine"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logger
        
        # Idle animation states (constant subtle movement)
        self.idle_animations = {
            "breathing": {
                "chest_movement": 0.02,  # 2% scale change
                "shoulder_rise": 0.015,
                "frequency_hz": 0.25,  # One breath every 4 seconds
                "variation": 0.3  # 30% natural variation
            },
            "weight_shift": {
                "hip_sway": 0.03,
                "frequency_seconds": 2.5,
                "direction_randomize": True
            },
            "micro_movements": {
                "head_tilt": 0.01,
                "finger_twitch": 0.005,
                "eye_dart_probability": 0.1  # 10% chance per second
            }
        }
        
        # Haryanvi/Indian specific gestures
        self.indian_gestures = {
            "namaste": {
                "hands_position": "joined_at_chest",
                "head_bow": 0.15,
                "emotional_context": ["greeting", "respect", "gratitude", "namaste"],
                "cultural_significance": "traditional_indian_greeting"
            },
            "hand_on_heart": {
                "hand_position": "right_hand_over_heart",
                "head_tilt": 0.1,
                "emotional_context": ["honesty", "sincerity", "vatsalya_bhavna", "promise"],
                "cultural_significance": "showing_sincerity"
            },
            "palm_up_open": {
                "hand_position": "palm_facing_up_open",
                "arm_angle": 0.3,
                "emotional_context": ["kya_karein", "helplessness", "questioning", "surrender"],
                "cultural_significance": "typical_indian_gesture"
            },
            "finger_point": {
                "finger": "index_extended",
                "arm_extension": 0.6,
                "emotional_context": ["anger", "accusation", "emphasis", "direction"],
                "cultural_significance": "direct_confrontation",
                "intensity_variants": ["gentle_point", "aggressive_point"]
            },
            "chin_stroke": {
                "hand_position": "thumb_index_on_chin",
                "emotional_context": ["thinking", "contemplation", "decision_making"],
                "cultural_significance": "elder_wisdom_gesture"
            },
            "forehead_touch": {
                "fingertips": "touching_forehead",
                "eyes_closed": True,
                "emotional_context": ["realization", "regret", "memory", "prayer"],
                "cultural_significance": "deep_thought_or_respect"
            },
            "dismissive_wave": {
                "hand_motion": "side_to_side_wrist_flick",
                "emotional_context": ["dismissal", "arre_chhod", "not_important"],
                "cultural_significance": "typical_haryanvi_dismissal"
            },
            "blessing_hand": {
                "hand_position": "raised_palm_forward",
                "slight_upward_motion": True,
                "emotional_context": ["blessing", "protection", "elder_to_younger"],
                "cultural_significance": "aashirwaad"
            }
        }
        
        # Emotional body postures
        self.emotion_postures = {
            "joy": {
                "chest": "open_expanded",
                "shoulders": "back_down",
                "spine": "straight_tall",
                "head": "tilted_slightly_up",
                "energy_level": 0.8,
                "movement_quality": "light_bouncy"
            },
            "sadness": {
                "chest": "collapsed_inward",
                "shoulders": "slumped_forward",
                "spine": "curved_hunched",
                "head": "looking_down",
                "energy_level": 0.3,
                "movement_quality": "heavy_slow"
            },
            "anger": {
                "chest": "tense_puffed",
                "shoulders": "raised_tight",
                "spine": "rigid_forward",
                "head": "thrust_forward",
                "jaw": "clenched",
                "fists": "tight",
                "energy_level": 0.9,
                "movement_quality": "sharp_aggressive"
            },
            "fear": {
                "chest": "tight_constricted",
                "shoulders": "raised_hunched",
                "spine": "curved_away",
                "head": "pulled_back",
                "arms": "close_to_body",
                "energy_level": 0.7,
                "movement_quality": "tense_jerky"
            },
            "love": {
                "chest": "soft_open",
                "shoulders": "relaxed",
                "spine": "gentle_curve",
                "head": "tilted_toward_subject",
                "arms": "open_receptive",
                "energy_level": 0.6,
                "movement_quality": "warm_flowing"
            },
            "pride": {
                "chest": "out_proud",
                "shoulders": "back_confident",
                "spine": "straight_tall",
                "head": "held_high",
                "chin": "slightly_up",
                "energy_level": 0.75,
                "movement_quality": "dignified_controlled"
            },
            "sangharsh": {
                "chest": "determined_forward",
                "shoulders": "set_strong",
                "spine": "rigid_determined",
                "jaw": "set_firm",
                "fists": "lightly_clenched",
                "energy_level": 0.85,
                "movement_quality": "driven_powerful"
            },
            "tyaag": {
                "chest": "soft_resigned",
                "shoulders": "slightly_slumped",
                "spine": "gentle_curve",
                "head": "accepting",
                "expression": "peaceful_sad",
                "energy_level": 0.4,
                "movement_quality": "gentle_released"
            }
        }
        
        # Walk cycles for full-body shots
        self.walk_cycles = {
            "confident_walk": {
                "stride_length": 0.8,
                "speed": 1.2,
                "posture": "upright_chest_out",
                "arm_swing": "moderate",
                "head_position": "level_looking_ahead",
                "when_to_use": ["entrance_scenes", "determined_moments", "success"]
            },
            "tired_walk": {
                "stride_length": 0.5,
                "speed": 0.7,
                "posture": "slightly_hunched",
                "shoulder_movement": "dragging",
                "head_position": "looking_down",
                "when_to_use": ["after_struggle", "defeat", "long_day"]
            },
            "nervous_walk": {
                "stride_length": 0.4,
                "speed": 1.0,
                "posture": "uncertain_shifting",
                "arm_position": "close_to_body",
                "head_movement": "darting_around",
                "when_to_use": ["anxiety", "first_time", "uncertainty"]
            },
            "angry_walk": {
                "stride_length": 0.9,
                "speed": 1.5,
                "posture": "stiff_aggressive",
                "arm_swing": "minimal_tense",
                "head_position": "fixed_forward",
                "when_to_use": ["storming_off", "confrontation", "frustration"]
            },
            "joyful_walk": {
                "stride_length": 0.7,
                "speed": 1.3,
                "posture": "light_bouncy",
                "arm_swing": "free_expressive",
                "head_movement": "looking_around_smiling",
                "when_to_use": ["celebration", "good_news", "relief"]
            }
        }
    
    def generate_body_language(self, scene: dict) -> dict:
        """
        Generate complete body language for a scene
        
        Args:
            scene: Scene dictionary with emotion and context
            
        Returns:
            Complete body language specification
        """
        self.logger.debug(f"💃 Generating body language for scene {scene.get('scene_number', '?')}")
        
        emotion = scene.get("emotion", "neutral")
        shot_type = scene.get("shot_type", "MEDIUM_SHOT")
        cultural_context = scene.get("cultural_context", "indian")
        
        # Get base posture for emotion
        posture_data = self.emotion_postures.get(emotion, self.emotion_postures["neutral"])
        
        # Determine if gesture is appropriate for this shot type
        should_add_gesture = self._should_add_gesture(shot_type, emotion)
        
        # Select appropriate gesture
        gesture = None
        if should_add_gesture:
            gesture = self._select_gesture(scene, emotion, cultural_context)
        
        # Add idle animation baseline
        idle_state = self._generate_idle_animation(posture_data)
        
        # Create body language specification
        body_spec = {
            "base_posture": posture_data,
            "gesture": gesture,
            "idle_animation": idle_state,
            "energy_level": posture_data.get("energy_level", 0.5),
            "movement_quality": posture_data.get("movement_quality", "neutral"),
            "cultural_authenticity": cultural_context == "indian",
            "shot_appropriate": self._adapt_for_shot_type(shot_type, posture_data)
        }
        
        return body_spec
    
    def _should_add_gesture(self, shot_type: str, emotion: str) -> bool:
        """Determine if gesture should be added based on shot and emotion"""
        
        # Gestures visible in medium shots and closer
        visible_shots = ["MEDIUM_SHOT", "MEDIUM_CLOSE_UP", "CLOSE_UP", "WIDE_SHOT"]
        
        if shot_type not in visible_shots:
            return False
        
        # Some emotions naturally include gestures
        gesture_emotions = ["anger", "joy", "love", "pride", "sangharsh", "dismissive"]
        
        return emotion in gesture_emotions
    
    def _select_gesture(self, scene: dict, emotion: str, cultural_context: str) -> dict:
        """Select culturally appropriate gesture"""
        
        text = scene.get("text", "").lower()
        
        # Check for keyword triggers in dialogue
        for gesture_name, gesture_data in self.indian_gestures.items():
            for keyword in gesture_data["emotional_context"]:
                if keyword in text:
                    self.logger.debug(f"👋 Gesture triggered by keyword: {keyword}")
                    return {
                        "type": gesture_name,
                        **gesture_data,
                        "trigger": "dialogue_keyword"
                    }
        
        # Fallback to emotion-based selection
        compatible_gestures = []
        for gesture_name, gesture_data in self.indian_gestures.items():
            if emotion in gesture_data["emotional_context"]:
                compatible_gestures.append((gesture_name, gesture_data))
        
        if compatible_gestures:
            selected = random.choice(compatible_gestures)
            return {
                "type": selected[0],
                **selected[1],
                "trigger": "emotion_based"
            }
        
        # No gesture
        return None
    
    def _generate_idle_animation(self, posture_data: dict) -> dict:
        """Generate subtle idle animation based on posture"""
        
        energy = posture_data.get("energy_level", 0.5)
        
        # Scale idle animation intensity by energy level
        idle_spec = {
            "breathing_rate": self.idle_animations["breathing"]["frequency_hz"] * (0.5 + energy),
            "breathing_depth": self.idle_animations["breathing"]["chest_movement"] * energy,
            "sway_frequency": self.idle_animations["weight_shift"]["frequency_seconds"] / energy,
            "micro_movement_intensity": self.idle_animations["micro_movements"]["head_tilt"] * energy
        }
        
        return idle_spec
    
    def _adapt_for_shot_type(self, shot_type: str, posture_data: dict) -> dict:
        """Adapt body language for specific shot type"""
        
        adaptations = {
            "EXTREME_WIDE_SHOT": {
                "exaggerate_posture": 1.5,  # 50% more pronounced for visibility
                "gesture_size": "large",
                "focus": "full_body_silhouette"
            },
            "WIDE_SHOT": {
                "exaggerate_posture": 1.3,
                "gesture_size": "medium_large",
                "focus": "full_body_visible"
            },
            "MEDIUM_LONG_SHOT": {
                "exaggerate_posture": 1.1,
                "gesture_size": "medium",
                "focus": "knees_up"
            },
            "MEDIUM_SHOT": {
                "exaggerate_posture": 1.0,  # Natural
                "gesture_size": "natural",
                "focus": "waist_up_arms_visible"
            },
            "MEDIUM_CLOSE_UP": {
                "exaggerate_posture": 0.9,  # Slightly subtler
                "gesture_size": "small_precise",
                "focus": "chest_up_hands_may_be_visible"
            },
            "CLOSE_UP": {
                "exaggerate_posture": 0.0,  # Posture not visible
                "gesture_size": "face_frame_only",
                "focus": "facial_expression_primary"
            },
            "EXTREME_CLOSE_UP": {
                "exaggerate_posture": 0.0,
                "gesture_size": "not_visible",
                "focus": "single_feature_micro_expression"
            }
        }
        
        return adaptations.get(shot_type, adaptations["MEDIUM_SHOT"])
    
    def generate_walk_cycle(self, scene_context: str, emotion: str) -> dict:
        """Generate walk cycle for moving scenes"""
        
        # Detect walk type from context
        context_lower = scene_context.lower()
        
        if any(word in context_lower for word in ["walk", "enter", "approach", "stride"]):
            if emotion in ["joy", "hope", "pride"]:
                walk_type = "confident_walk"
            elif emotion in ["sadness", "tyaag", "defeat"]:
                walk_type = "tired_walk"
            elif emotion in ["fear", "nervous"]:
                walk_type = "nervous_walk"
            elif emotion in ["anger", "frustration"]:
                walk_type = "angry_walk"
            else:
                walk_type = "confident_walk"
        else:
            # No walking needed
            return None
        
        walk_data = self.walk_cycles.get(walk_type, self.walk_cycles["confident_walk"])
        
        return {
            "type": walk_type,
            **walk_data,
            "trigger": "movement_detected"
        }
    
    def create_full_body_spec(self, scenes: list) -> list:
        """
        Process all scenes and add complete body language specifications
        
        Args:
            scenes: List of scene dictionaries
            
        Returns:
            Enhanced scenes with body language specs
        """
        self.logger.info(f"💃 Adding body language to {len(scenes)} scenes")
        
        enhanced_scenes = []
        
        for i, scene in enumerate(scenes):
            try:
                # Generate body language
                body_spec = self.generate_body_language(scene)
                
                # Check if walk cycle needed
                walk_cycle = self.generate_walk_cycle(
                    scene.get("text", ""),
                    scene.get("emotion", "neutral")
                )
                
                # Combine all body elements
                full_body_spec = {
                    "body_language": body_spec,
                    "walk_cycle": walk_cycle,
                    "scene_number": scene.get("scene_number", i + 1)
                }
                
                # Merge with original scene
                enhanced_scene = {
                    **scene,
                    **full_body_spec
                }
                
                enhanced_scenes.append(enhanced_scene)
                
            except Exception as e:
                self.logger.error(f"Body language generation failed for scene {i}: {e}")
                # Add minimal body data as fallback
                scene["body_language"] = {
                    "base_posture": self.emotion_postures.get("neutral"),
                    "gesture": None,
                    "idle_animation": self._generate_idle_animation(self.emotion_postures["neutral"])
                }
                enhanced_scenes.append(scene)
        
        self.logger.success(f"✅ Body language added to {len(enhanced_scenes)} scenes")
        return enhanced_scenes
    
    def export_animation_ready_format(self, enhanced_scenes: list) -> list:
        """
        Convert body language specs to animation-ready format
        For integration with LivePortrait or other animation systems
        
        Returns:
            List of animation parameters ready for rendering
        """
        
        animation_specs = []
        
        for scene in enhanced_scenes:
            body_spec = scene.get("body_language", {})
            
            # Extract key animation parameters
            spec = {
                "scene_id": scene.get("scene_number"),
                "duration": scene.get("duration_estimate", 5),
                
                # Posture parameters
                "spine_rotation": body_spec.get("base_posture", {}).get("spine", "neutral"),
                "shoulder_position": body_spec.get("base_posture", {}).get("shoulders", "relaxed"),
                "chest_expansion": body_spec.get("base_posture", {}).get("chest", "normal"),
                
                # Head parameters
                "head_tilt": body_spec.get("base_posture", {}).get("head", "level"),
                "head_orientation": "forward",
                
                # Gesture parameters (if present)
                "gesture_active": body_spec.get("gesture") is not None,
                "gesture_type": body_spec.get("gesture", {}).get("type", "none"),
                "hand_position": body_spec.get("gesture", {}).get("hand_position", "rest"),
                
                # Idle animation
                "breathing_active": True,
                "breathing_rate": body_spec.get("idle_animation", {}).get("breathing_rate", 0.25),
                "micro_movements": True,
                
                # Energy and quality
                "energy_level": body_spec.get("energy_level", 0.5),
                "movement_quality": body_spec.get("movement_quality", "neutral")
            }
            
            animation_specs.append(spec)
        
        return animation_specs


# Test function
def test_body_language_engine():
    """Test body language engine with sample scenes"""
    engine = BodyLanguageEngine()
    
    test_scenes = [
        {"scene_number": 1, "emotion": "neutral", "text": "Introduction", "shot_type": "MEDIUM_SHOT"},
        {"scene_number": 2, "emotion": "joy", "text": "We won! Great news!", "shot_type": "CLOSE_UP"},
        {"scene_number": 3, "emotion": "sadness", "text": "He left forever.", "shot_type": "MEDIUM_CLOSE_UP"},
        {"scene_number": 4, "emotion": "anger", "text": "How could you do this?", "shot_type": "MEDIUM_SHOT"},
        {"scene_number": 5, "emotion": "sangharsh", "text": "I will fight till the end.", "shot_type": "WIDE_SHOT"},
        {"scene_number": 6, "emotion": "tyaag", "text": "Take it. It's yours.", "shot_type": "CLOSE_UP"},
        {"scene_number": 7, "emotion": "love", "text": "Main tumse pyaar karti hoon.", "shot_type": "MEDIUM_CLOSE_UP"}
    ]
    
    print("\n💃 Testing Body Language Engine")
    print("="*70)
    
    enhanced = engine.create_full_body_spec(test_scenes)
    
    for scene in enhanced:
        print(f"\nScene {scene['scene_number']} ({scene['emotion']}):")
        body = scene.get('body_language', {})
        print(f"  Posture: {body.get('base_posture', {}).get('chest', 'N/A')}")
        print(f"  Energy: {body.get('energy_level', 0)}")
        print(f"  Movement: {body.get('movement_quality', 'N/A')}")
        
        gesture = body.get('gesture')
        if gesture:
            print(f"  Gesture: 👋 {gesture.get('type', 'N/A')}")
        else:
            print(f"  Gesture: None")
    
    print("\n" + "="*70)
    print("✅ Body Language Engine test complete!")


if __name__ == "__main__":
    test_body_language_engine()
