from PIL import Image

def get_webp_disposal(image):
    # Check if the image is animated
    if hasattr(image, "is_animated") and image.is_animated:
        # Retrieve the disposal method
        disposal_method = image.info.get("disposal_method")
        return disposal_method

def get_webp_duration(image):
    duration = image.info.get("duration")
    if duration is None:
        duration = 0
    return duration

def resize_webp_image(image, max_size, method):
    # Calculate the new size while maintaining the aspect ratio
    width, height = image.size
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_width = int(width * (max_size / height))
        new_height = max_size

    # Resize the image animation with the new size
    resized_image = image.resize((new_width, new_height), method)
    return resized_image

def compress_webp(image,output_path, skip_interval=0, max_size=100, quality=50, method=Image.LANCZOS):
    if image is None:
        print("image none")
        return
    frames = []
    durations = []

    # handle animated webp
    if hasattr(image, "is_animated") and image.is_animated:
        # Iterate over each frame
        for frame in range(0, image.n_frames):
            image.seek(frame)
            # Skip frames if necessary
            is_border_frame = (frame == 0 or frame == image.n_frames - 1) 
            skip_frame = skip_interval > 0 and frame % (skip_interval) == 0 and not is_border_frame

            if skip_frame:
                frame_time= get_webp_duration(image)
                durations[-1] += frame_time
                # print("skipping frame", frame, "duration:", duration, "frame time:", frame_time)
            else:
                resized_image = resize_webp_image(image, max_size, method)
                frames.append(resized_image)
                durations.append(get_webp_duration(image))

        print("------------------")
        print("frames before:", image.n_frames)
        print("frames after:", len(frames))
        print(f"frame reduction: {100 - (len(frames) / image.n_frames) * 100:0,.2f}%")
    else:
        resized_image = resize_webp_image(image, max_size, method)
        frames.append(resized_image)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], format="WebP", loop=0,
                   quality=quality, thumbnail=None, disposal=2, optimize=True,
                   duration=durations, method=6, minimize_size=True)


def load_webp(input_path):
    with Image.open(input_path) as image:
        return image

methods = {
    "NEAREST": Image.NEAREST,
    "LANCZOS": Image.LANCZOS,
    "BILINEAR": Image.BILINEAR,
    "BICUBIC": Image.BICUBIC,
    "BOX": Image.BOX,
}


if __name__ == "__main__":
    print("This file is not meant to be run directly.")
