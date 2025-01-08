from phockup import Phockup
import re
import os
import platform
from src.exif import Exif
from src.date import Date
from magika import Magika
import pathlib


class Filckup(Phockup):
    def __init__(self, input_dir, output_dir, **args):
        self.magika = Magika()
        super().__init__(input_dir, output_dir, **args)

    def get_file_type(self, mimetype):
        """
        Check if given file_type is image or video
        Return None if other
        Use mimetype to determine if the file is an image or video.
        """
        for result, mimetypes in CATEGORIES.items():
            if mimetype in mimetypes:
                return result
        patternImage = re.compile('^(image/.+|application/vnd.adobe.photoshop)$')
        if patternImage.match(mimetype):
            return 'image'
        patternAudio = re.compile('^(audio/.*')
        if patternAudio.match(mimetype):
            return 'audio'
        patternVideo = re.compile('^(video/.*)$')
        if patternVideo.match(mimetype):
            return 'video'
        return None

    def get_file_name_and_path(self, filename):
        """
        Returns target file name and path
        """
        exif_data = Exif(filename).data()
        target_file_type = None

        if exif_data and 'MIMEType' in exif_data:
            target_file_type = self.get_file_type(exif_data['MIMEType'])

        date = None
        if target_file_type in ['image', 'video', 'audio']:
            date = Date(filename).from_exif(exif_data, self.timestamp, self.date_regex,
                                            self.date_field)
            output = self.get_output_dir(date)
            target_file_name = self.get_file_name(filename, date)
            if not self.original_filenames:
                target_file_name = target_file_name.lower()
        else:
            output = self.get_output_dir([])
            target_file_name = os.path.basename(filename)

        target_file_path = os.path.sep.join([output, target_file_name])
        return output, target_file_name, target_file_path, target_file_type, date


    def get_file_name_and_path(self, filename):
        """
        Returns target file name and path
        """
        target_file_type = None
        exif_data = None

        guess = self.magika.identify_path(pathlib.Path(filename))
        if guess:
            target_file_type = guess.output.group
        else:
            exif_data = Exif(filename).data()

            if exif_data and 'MIMEType' in exif_data:
                target_file_type = self.get_file_type(exif_data['MIMEType'])

        date = None
        if target_file_type in ['image', 'video', 'audio']:
            if exif_data is None:
                exif_data = Exif(filename).data()
            date = Date(filename).from_exif(exif_data, self.timestamp, self.date_regex,
                                            self.date_field)
            output = self.get_output_dir(date, target_file_type)
            target_file_name = self.get_file_name(filename, date)
            if not self.original_filenames:
                target_file_name = target_file_name.lower()
        else:
            date = Date(filename).from_timestamp()
            output = self.get_output_dir(date, target_file_type)
            target_file_name = os.path.basename(filename)

        target_file_path = os.path.sep.join([output, target_file_name])
        return output, target_file_name, target_file_path, target_file_type, date
