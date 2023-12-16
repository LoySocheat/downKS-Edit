import os
import time
from colorama import Fore, init
from moviepy.editor import VideoFileClip, AudioFileClip, afx, vfx, CompositeVideoClip, ImageClip
from rich.console import Console

init(autoreset=True)
console = Console()

def get_clip_list(file_list):
    clip_list_input = []
    for file in file_list:
        if file.endswith(".mp4") or file.endswith(".MP4") or file.endswith(".mkv"):
            clip_list_input.append(file)
    return clip_list_input

def get_music_list(music_folder):
    if os.path.exists(music_folder):
        music_files = os.listdir(music_folder)
        return music_files
    else:
        return None
    
def add_logo(clip, logo_path, logo_position=('right', 'bottom'), logo_size=(100, 100)):
    logo = ImageClip(logo_path, transparent=True)
    logo = logo.resize(width=logo_size[0], height=logo_size[1])
    logo = logo.set_position(logo_position).set_duration(clip.duration)
    video_with_logo = CompositeVideoClip([clip, logo])
    return video_with_logo

def custom_edit_video(input_path, question_color, saturation_factor, r_factor, g_factor, b_factor,
                       question_flip, question_speed, speedf, question_music, music_path,
                       question_size, rotate_factor, zoom_factor, output_path, xxx):
    clip = VideoFileClip(input_path)

    # Apply RGB adjustments to each pixel
    if question_color.lower() == "yes":
        def rgb_shift_filter(image):
            adjusted_image = image.copy()
            adjusted_image[:, :, 0] = adjusted_image[:, :, 0] * r_factor
            adjusted_image[:, :, 1] = adjusted_image[:, :, 1] * g_factor
            adjusted_image[:, :, 2] = adjusted_image[:, :, 2] * b_factor
            return adjusted_image.clip(0, 255).astype(int)

        rgb_shifted_clip = clip.fl_image(rgb_shift_filter)
        clip = rgb_shifted_clip.fx(vfx.colorx, saturation_factor)

    # Flip
    if question_flip.lower() == "yes":
        clip = clip.fx(vfx.mirror_x)

    # Speed
    if question_speed.lower() == "yes":
        clip = clip.fx(vfx.speedx, speedf)

    # Music
    if question_music.lower() == "yes" and music_path and os.path.exists(music_path):
        audioclip = AudioFileClip(music_path)
        new_audioclip = afx.audio_loop(audioclip, duration=clip.duration)
        clip = clip.set_audio(new_audioclip)

    # Size Video
    if question_size.lower() == "yes":
        clip = clip.fx(vfx.rotate, rotate_factor)
        original_width, original_height = clip.size
        new_width = int(original_width / zoom_factor)
        new_height = int(original_height / zoom_factor)
        x_position = (original_width - new_width) / 2
        y_position = (original_height - new_height) / 2
        clip = clip.crop(x_position, y_position, x_position + new_width, y_position + new_height)
        
    # if logo_path:
    #     clip = add_logo(clip, logo_path, logo_position, logo_size)

    clip.write_videofile(output_path, verbose=False, logger=None, codec='libx264', audio_codec="aac", preset=xxx)
    clip.close()

def process_videos(video_folder, output_folder):
    if os.path.exists(video_folder):
        file_list = os.listdir(video_folder)
        clip_list = get_clip_list(file_list)
        
        # Edit color video
        question_color = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Do you want to edit color? (yes/no): {Fore.WHITE}")
        if question_color.lower() == "yes":
            saturation_factor = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter Number Of Saturation Factor (1.0 means no change): {Fore.WHITE}"))
            r_factor = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter Number Of R Factor (1.0 means no change): {Fore.WHITE}"))
            g_factor = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter Number Of G Factor (1.0 means no change): {Fore.WHITE}"))
            b_factor = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter Number Of B Factor (1.0 means no change): {Fore.WHITE}"))
        else:
            saturation_factor = r_factor = g_factor = b_factor = 1.0

        # Edit flip video
        question_flip = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Do you want to flip video? (yes/no): {Fore.WHITE}")
        
        # Edit custom speed
        question_speed = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Do you want to edit speed? (yes/no): {Fore.WHITE}")
        if question_speed.lower() == "yes":
            speedf = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter the Speed Factor (1.0 means no change): {Fore.WHITE}"))
        else:
            speedf = 1.0
            
        question_music = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Do you want to change music background? (yes/no): {Fore.WHITE}")
        if question_music.lower() == "yes":
            while True:
                music_folder = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW}Enter path music folder:{Fore.WHITE} ")
                music_files = get_music_list(music_folder)
                if music_files is not None:
                    break
                else:
                    print("Invalid music folder. Try again.")
                
        question_size = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Do you want to change video size? (yes/no): {Fore.WHITE}")
        if question_size.lower() == "yes":
            rotate_factor = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter Number Of Rotate Factor (0 means no change): {Fore.WHITE}"))
            zoom_factor = eval(input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter Number Of Zoom Factor (1.0 means no change): {Fore.WHITE}"))
        else:
            rotate_factor = 0
            zoom_factor = 1.0
        
        print() 
            
        # Number of files found
        console.log(f"[cyan][File][/cyan] Found [green]{len(clip_list)}[/green] videos")
        time.sleep(1)

        # Process status
        console.log(f'[cyan][File][/cyan] [green]Start processing the video...[/green]\n')
        counter = 0

        # Status or waiting
        with console.status('[cyan]Processing... please wait!', spinner='line') as status:
            if not clip_list:
                pass
            else:
                # Make a new folder with counter += 1 every time it runs.
                while True:
                    counter += 1
                    dir = f"{output_folder}/custom_edit_video/Video{counter}"
                    if os.path.isdir(dir):
                        pass
                    else:
                        os.makedirs(dir)
                        break

            # Process files
            for i, file in enumerate(clip_list):
                if question_music.lower() == "yes":
                    music_index = i % len(music_files)  # Loop through music files
                    music_path = os.path.join(music_folder, music_files[music_index])
                else:
                    music_path = None
                    
                output = f"{dir}/{file[:-4]}_custom_edit_video.mp4"
                limit = str(f'{file:60.60}')

                # Check if output exists in the folder. If exists then skip else process
                if os.path.exists(output):
                    console.log(f'[cyan][File][/cyan] [green]{limit}[/green] already exists, skip...')
                    # Function skip
                    clip_list.remove(file)
                else:
                    start = time.time()
                    custom_edit_video(os.path.join(video_folder, file), question_color, saturation_factor, r_factor, g_factor, b_factor,
                                       question_flip, question_speed, speedf, question_music, music_path, question_size, rotate_factor, zoom_factor, output, "ultrafast")
                    console.log(f'[cyan][File][/cyan] [green]{limit}[/green]')
                    end = time.time()
                    console.print(f"{Fore.CYAN}[Programs] {Fore.GREEN}[Status] {Fore.WHITE}Processed:{Fore.YELLOW} %.2fs" % (end - start))
                    console.print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Status] {Fore.WHITE}Has been created.\n")

            console.print(f"{Fore.YELLOW}[Programs] {Fore.MAGENTA}[Saved] {Fore.GREEN}{dir}{Fore.WHITE}")
            time.sleep(1)
            console.log(f'[cyan][File][/cyan] Processed [green]{len(clip_list)}[/green] videos successfully.')
            time.sleep(0.5)
            print(input(f"{Fore.CYAN}[Programs] {Fore.YELLOW}[Status] {Fore.WHITE}Press enter to continue.."))

    else:
        print('Check Your Path!!!')

video_folder = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter your video folder:{Fore.WHITE} ")
output_folder = input(f"{Fore.WHITE}[{Fore.MAGENTA}?{Fore.WHITE}] {Fore.YELLOW} Enter output folder:{Fore.WHITE} ")
process_videos(video_folder, output_folder)