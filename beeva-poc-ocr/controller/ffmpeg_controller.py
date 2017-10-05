import os
import subprocess


class FFmpegController(object):
    def __init__(self, settings):
        self.__settings = settings

    def generate_frames_from_video(self, video_path, output_path, fr_threshold):
        vid_name = os.path.splitext(os.path.basename(video_path))[0]
        out_folder_abspath = os.path.join(os.path.abspath(output_path), vid_name)
        if not os.path.exists(out_folder_abspath):
            os.mkdir(out_folder_abspath)
        out_abspath_with_frame_name = os.path.join(out_folder_abspath, self.__settings.FRAME_NAME_PATTERN)
        cmd = self.__settings.FFMPEG_CMD.format(self.generate_quoted_path(os.path.abspath(video_path)), fr_threshold,
                                                self.generate_quoted_path(out_abspath_with_frame_name))
        try:
            exit_code = subprocess.check_call(cmd, shell=True)
            if exit_code == 0:
                return out_folder_abspath
            else:
                return None
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def generate_quoted_path(path):
        return "\"{}\"".format(path)
