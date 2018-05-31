
from argparse import ArgumentParser, ArgumentError, Action
import json
from os.path import exists, dirname, abspath
from pyiiif.pres_api.twodotone.records import Manifest, Sequence, Annotation, ImageResource, Canvas
from urllib.parse import urlparse
import requests
from sys import stdout

__version__ = "1.0.0"

def ConvertRecordIntoObject(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(ConvertRecordIntoObject, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, args, values, option_strings=None):
        if exists(values):
            try:
                setattr(self, self.dest, Manifest.load(values))
            except:
                msg = "the IIIF record is not a valid IIIF record; could not be loaded"
                raise ArgumentError(self, msg)
        else:
            msg = "{} does not exist on-disk; cannot load file".format(values)
            raise ArgumentError(self, msg)
        
def main():
    arguments = ArgumentParser(description="A CLI application to make it easy to add your first sequence of images to a IIIF record",
                               epilog="Version " + __version__)
    record_arg = arguments.add_argument("record", action='store', type=str, help="The path to the IIIF record that you want to extend")
    img_file_arg = arguments.add_argument("image_file", type=str, action="store", help="The location of the list of IIIF image links to ")
    arguments.add_argument("-o", "--output", action="store", type=str, help="Optional path to save the new extended record. Default is stdout")
    try:
        parsed_args = arguments.parse_args()
        are_there_images = False
        if not exists(parsed_args.image_file):
            raise ArgumentError(img_file_arg, "the file must exist on disk to be read")
        
        if not exists(parsed_args.record):
            raise ArgumentError(record_arg, "the file must exist on disk to be read")
        img_links = [x.strip() for x in open(parsed_args.image_file, 'r', encoding="utf-8").readlines()]
        data = json.load(open(parsed_args.record, 'r', encoding="utf-8"))

        m = Manifest.load(json.dumps(data))
        old_sequence = m.sequences
        for n_sequence in old_sequence:
            for n_canvas in n_sequence.canvases:
                try:
                    n_canvas.images
                    are_there_images = True
                except ValueError:
                    pass
        new_sequence = Sequence("http://example.org/foo")
        canvases = []
        count = 1
        for n_link in img_links:
           img_data = requests.get(n_link).json()
           height, width = img_data['height'], img_data['width']
           new_canvas = Canvas("http://example.org/biz" + str(count))
           new_canvas.label = "Image {}".format(count)
           new_canvas.height = height
           new_canvas.width = width
           new_annotation = Annotation("http://example.org/bar{}".format(count), new_canvas.id)
           url_object = urlparse(n_link)
           new_img = ImageResource(url_object.scheme, url_object.netloc, '', url_object.path, "image/jpeg")
           new_annotation.resource = new_img
           new_canvas.images = [new_annotation]
           canvases.append(new_canvas)
           count += 1
        new_sequence.canvases = canvases
        if are_there_images:
            m.sequences = [new_sequence] + old_sequence
        else:
            m.sequences = [new_sequence]
        string = json.dumps(m.to_dict(), indent=4)
        if parsed_args.output and exists(dirname(abspath(parsed_args.output))) and not exists(abspath(parsed_args.output)):
            with open(parsed_args.output, 'w+', encoding="utf-8") as wf:
                wf.write(string)
        else:
            stdout.write(string)
        return 0
    except KeyboardInterrupt:
        return 131