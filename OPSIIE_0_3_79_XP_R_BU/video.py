import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import logging
from pathlib import Path
import os
from utils import get_random_expression, ensure_directory_exists, clean_filename
from colorama import Fore, Style
import webbrowser

# Dictionary of available video models
VIDEO_MODELS = {
    "modelscope": "damo-vilab/text-to-video-ms-1.7b",
    "zeroscope": "cerspense/zeroscope_v2_576w",
    "videogen": "VideoCrafter/videogen-1",
    "tuneavideo": "tuneavideo/stable-diffusion-v1-5-video"
}

# At the top of the file, after imports
_video_generator = None

class VideoGenerator:
    def __init__(self):
        self.default_params = {
            "num_frames": 24,
            "height": 256,
            "width": 256,
            "num_inference_steps": 20,
            "guidance_scale": 7.5,
        }
        
        # Initialize with default model
        self.current_model = "modelscope"
        self.initialize_pipeline()
        
        # Create results directory
        self.results_dir = ensure_directory_exists(os.path.join(os.path.dirname(__file__), 'outputs', 'videos'))

    def initialize_pipeline(self):
        """Initialize or update the pipeline with the current model"""
        try:
            # Only use fp16 variant for modelscope
            if self.current_model == "modelscope":
                self.pipe = DiffusionPipeline.from_pretrained(
                    VIDEO_MODELS[self.current_model],
                    torch_dtype=torch.float16,
                    variant="fp16"
                )
            else:
                self.pipe = DiffusionPipeline.from_pretrained(
                    VIDEO_MODELS[self.current_model],
                    torch_dtype=torch.float16
                )
                
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
                
            logging.info(f"Successfully initialized model: {self.current_model}")
            return True
        except Exception as e:
            logging.error(f"Error initializing model: {str(e)}")
            return False

    def change_model(self, model_name):
        """Change the current video model"""
        if model_name not in VIDEO_MODELS:
            return False, f"Model '{model_name}' not found. Available models: {', '.join(VIDEO_MODELS.keys())}"
        
        self.current_model = model_name
        success = self.initialize_pipeline()
        
        if success:
            return True, f"Successfully changed model to {model_name}"
        else:
            return False, f"Failed to initialize model {model_name}"

    def generate_video(self, prompt, **kwargs):
        """Generate video based on text prompt and optional parameters"""
        try:
            # Merge default parameters with any provided kwargs
            params = self.default_params.copy()
            params.update(kwargs)
            
            logging.info(f"Generating video for prompt: {prompt}")
            
            # Generate the video
            video_frames = self.pipe(
                prompt,
                num_frames=params["num_frames"],
                height=params["height"],
                width=params["width"],
                num_inference_steps=params["num_inference_steps"],
                guidance_scale=params["guidance_scale"]
            ).frames[0]
            
            # Save the video
            output_path = os.path.join(self.results_dir, clean_filename(prompt, 'mp4'))
            export_to_video(video_frames, str(output_path))
            
            # Autoplay the video
            webbrowser.open(output_path)
            
            logging.info(f"Video saved to {output_path}")
            return True, str(output_path)

        except Exception as e:
            logging.error(f"Error generating video: {str(e)}")
            return False, str(e)

def handle_video_command(message):
    """Handle the /video command"""
    global _video_generator
    
    try:
        # Initialize the generator only once
        if _video_generator is None:
            _video_generator = VideoGenerator()
        
        # Check if it's a model change command
        if "model" in message:
            model_name = message.replace("/video model", "").strip()
            
            if not model_name:
                return f"Current video model is: {_video_generator.current_model}. Available models: {', '.join(VIDEO_MODELS.keys())}"
            
            success, message = _video_generator.change_model(model_name)
            return message
        
        # Handle regular video generation
        prompt = message.replace("/video", "").strip()
        
        if not prompt:
            return "Please provide a description for the video you want to generate."
        
        # Display dreaming message
        print(Fore.LIGHTCYAN_EX + "OPSIIE is dreaming... do not disturb.")
        print(Fore.LIGHTGREEN_EX + get_random_expression())
        
        success, result = _video_generator.generate_video(prompt)
        
        if success:
            print(Fore.LIGHTYELLOW_EX + f"\nVideo specimen generated and saved to: {result}")
            return f"Video generated successfully!"
        else:
            return f"Error generating video: {result}"
        
    except Exception as e:
        return f"Error processing command: {str(e)}"

def main():
    """
    Main test loop for the Video Generation functionality.
    """
    print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
    print(Fore.LIGHTGREEN_EX + """
    ╔═══════════════════════════════════════════╗
    ║     Video Generation Agent Test Loop      ║
    ╚═══════════════════════════════════════════╝
    """)
    print(Fore.LIGHTCYAN_EX + "═" * 80)
    print(Fore.LIGHTYELLOW_EX + "\nType '/video help' for available commands")
    print(Fore.LIGHTCYAN_EX + "═" * 80)
    
    while True:
        try:
            command = input(f"\n{Fore.GREEN}Enter command: {Style.RESET_ALL}")
            
            # Check for exit command
            if command.lower() in ['exit', 'quit', 'q']:
                print(f"{Fore.LIGHTGREEN_EX}[SYSTEM] Exiting Video Generation Interface...{Style.RESET_ALL}")
                break
                
            # Handle empty input
            if not command.strip():
                continue
                
            result = handle_video_command(command)
            print(result)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTGREEN_EX}[SYSTEM] Exiting Video Generation Interface...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    main()