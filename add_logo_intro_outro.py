from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from colorama import Fore, init

init(autoreset=True)

def resize_clip(clip, target_size):
    return clip.resize(target_size)

def add_logo(video_clip, logo_path, logo_position, logo_size):
    # Load the logo image with transparency using ImageClip
    logo_clip = ImageClip(logo_path, transparent=True)

    # Resize the logo clip
    logo_clip = resize_clip(logo_clip, logo_size)

    # Set the duration of the logo clip to match the video duration
    logo_clip = logo_clip.set_duration(video_clip.duration)

    # Set the position of the logo
    logo_clip = logo_clip.set_position(logo_position)

    # Composite the video and logo clips
    video_with_logo_clip = CompositeVideoClip([video_clip, logo_clip])

    return video_with_logo_clip

def add_intro_outro(main_video_path, intro_path, outro_path, logo_path, output_path, logo_position, logo_size):
    # Load the main video clip
    main_video_clip = VideoFileClip(main_video_path)

    # Load the intro and outro clips
    intro_clip = VideoFileClip(intro_path)
    outro_clip = VideoFileClip(outro_path)

    # Resize intro and outro clips to match the main video dimensions
    intro_clip = resize_clip(intro_clip, (main_video_clip.w, main_video_clip.h))
    outro_clip = resize_clip(outro_clip, (main_video_clip.w, main_video_clip.h))

    # Add logo to the main video
    main_video_with_logo_clip = add_logo(main_video_clip, logo_path, logo_position, logo_size)

    # Concatenate intro, main video with logo, and outro
    final_clip = concatenate_videoclips([intro_clip, main_video_with_logo_clip, outro_clip])

    # Write the result to a new video file
    final_clip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", preset='ultrafast', fps=30)

    # Close the clips
    main_video_clip.close()
    intro_clip.close()
    outro_clip.close()
    final_clip.close()

# Example usage:
main_video_path = r"F:\videos\test\1.mp4"
intro_path = r"F:\videos\test\2.mp4"  # Replace with the path to your intro video
outro_path = r"F:\videos\test\3.mp4"  # Replace with the path to your outro video
logo_path = r"C:\Users\LOY Socheat\Pictures\LOGO 01-09.png"

# Get user input for logo position and size
logo_position_x = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter horizontal position of the logo (left/center/right): {Fore.WHITE}")
logo_position_y = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter vertical position of the logo (top/center/bottom): {Fore.WHITE}")
logo_size_x = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter width of the logo: {Fore.WHITE}"))
logo_size_y = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter height of the logo: {Fore.WHITE}"))

logo_position = (logo_position_x, logo_position_y)
logo_size = (logo_size_x, logo_size_y)

output_path = "output_video_with_intro_outro_logo.mp4"

# Add user-specified logo position and size
add_intro_outro(main_video_path, intro_path, outro_path, logo_path, output_path, logo_position, logo_size)
