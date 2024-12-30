from phockup import Phockup
import re
import os
from src.exif import Exif
from src.date import Date

CATEGORIES = {
    'documents': ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                  'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                  'text/plain', 'text/csv'],
    'media': ['image/jpeg', 'image/png', 'image/gif', 'audio/mpeg', 'video/mp4', 'video/x-msvideo'],
    'executables': ['application/x-msdownload', 'application/x-executable', 'application/x-sh'],
    'archives': ['application/zip', 'application/x-rar-compressed', 'application/x-tar'],
    'game_assets': ['application/octet-stream'],  # Placeholder for game assets
}

class Filckup(Phockup):
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
