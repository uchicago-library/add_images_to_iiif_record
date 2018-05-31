# add_images_to_iiif

## Introduction

This is a command-line application meant to make it simple and fast to add a simple set of IIIF image links to an existing metadata-only IIIF Presentation record. The intended audience is developers working in a library that is beginning to integrate IIIF into their digital collections and that may have a firm divorce between digital collections files and MARC metadata capture about cultural heritage objects.

## Quickstart

```bash
$ git clone git@github.com:uchicago-library/add_images_to_iiif_record
$ cd add_images_to_iiif_record
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python setup.py install
$ extend_record -h
```

Following these instructions will install the tool to a virtual environment on your system and run the command-line application that you just installed.

## Examples

```bash
>>> extend_record -o extended_iiif_record.json --images [path to a CSV file containing the IIIF imges to add] [path to a IIIF record]
```

Performing this action you will take a IIIF record on-disk, the CSV file containing metadata about IIIF images that you want to add to the existing IIIF record, and generate a new IIIF record with a sequence containing canvases for each of the IIIF images. Finally, the record will be saved to a file called 'extended_iiif_record.json'.

## Authors

- verbalhanglider <tdanstrom@uchicago.edu>