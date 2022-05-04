# This code handles the deidentification of DICOMFiles to replace the typical
# method of Deidentification using DICOM Browser (https://wiki.xnat.org/xnat-tools/dicombrowser)
# This code was written as a replacement method for the
# DICOM deidentification utilized by DISCOVERY clients.
# A link to the previous method utilized can be found discoverystudy.org.

# Begun: 2022-02-15

# The process of this code is decribed below:
# Interact with users to establish DICOM Files they would like to deindentify
# and prompt users to input their site id, patient id, and scan session id.
# Prompt users with a filebrowser in which they can select the parent folder where the scan session.
# Utilize the anon_for_discovery.das file (or a simaler version of it) to dictate which DICOMFields will be identified.
# Replace various fields with data (site ID, patient ID, scan session ID etc.) inputted by the user.
# Create an error log to track any possible issue the user may encounter.

# ver 0.1 begun: 2022-02-15
# Author: Daniel G. Balentine, Martinos Center for Biomedical Imaging, Massachusetts General Hospital
# Email: dbalentine@mgh.harvard.edu (2022)

"""
2022-2-15
general scripting began. filebrowser implemented. .das file reader scripted.
*notes: implement a popup to prompt users to provide specific site and patient information.

2022-3-09
work has been done but just not noted. module create called program.gui which will be the
basic GUI for user input. having issues with error handling.

2022-3-11
Hashing module is being implemented.
Dictionary to_replace module implemented.

2022-3-14
Realign everything with proper 4 space tabs

2022-3-18
Switched code to an object oriented approach.

2022-3-24
Logging module implemented and unit test developed.

2022-4-18
Convert to Pep-8 Style

2022-5-3
Added KeyError handling in deidentify_files() module
Added rename_out_folder module...is this needed? is this the most efficient way to do this?
"""

import pydicom
import os
import hashlib
import shutil


class DataSet:
    def __init__(self, path, site_ID, participant_ID, scan_session_ID, results, logger):
        self.log = logger
        self.log.logger.info('Backend Initialized')

        # results array to store values that need to go back to front end...results[0] is the number of files.
        self.results = results

        # variables from front end
        self.site_ID = site_ID
        self.participant_ID = participant_ID
        self.scan_session_ID = scan_session_ID
        self.path = path
        # create arrays to store .das values
        self.to_remove = []
        self.to_hash = []

        self.log.logger.info('Site ID : {}'.format(self.site_ID))
        self.log.logger.info('Participant ID : {}'.format(self.participant_ID))
        self.log.logger.info('Scan Session ID : {}'.format(self.scan_session_ID))
        self.log.logger.info('Path to Files : {}'.format(self.path))

        # values to be replaced...key = dicom tag....value = replaced value... form { key : value }
        self.to_replace_dic = {'00080080': self.site_ID,
                               '00100010': self.participant_ID,
                               '00100020': self.participant_ID}

    def das_file_reader(self, filename):
        self.log.logger.info('Reading in the .das file: {}'.format(filename))
        # open .das file
        with open(filename) as f:
            # read in lines
            f.readline()
            for line in f:
                # read in lines beginning with a -, which take the form of "- (****,****)"
                if line[0] == '-':
                    # append values to to_remove array, values now take form "********"
                    value = (line[3]
                             + line[4]
                             + line[5]
                             + line[6]
                             + line[8]
                             + line[9]
                             + line[10]
                             + line[11])
                    self.to_remove.append(value)

                # read in lines begining with a "+", which take form "+ (****,****)"
                if line[0] == "+":
                    # append values to to_hash array, each element now takes form "********"
                    value = (line[3]
                             + line[4]
                             + line[5]
                             + line[6]
                             + line[8]
                             + line[9]
                             + line[10]
                             + line[11])
                    self.to_hash.append(value)

        # close the .das file
        f.close()
        self.log.logger.info('.das file has been read')

    def walk_through_files(self):
        # array to store file paths
        self.file_paths = []
        self.out_file_paths = []

        # out directory path
        self.out_path = self.path
        self.out_path += '_did'

        # create out directory with same structure as original
        if not os.path.exists(self.out_path):
            try:
                os.makedirs(self.out_path)
                self.log.logger.info('Created : {}'.format(self.out_path))
            except:
                self.log.logger.info('Could not create dir: {}'.format(self.out_path))
        dst = self.out_path
        src = os.path.abspath(self.path)
        src_prefix = len(src) + len(os.path.sep)
        # iterate through original directory and copy tree without files
        for root, dirs, files in os.walk(src):
            for dirname in dirs:
                dirpath = os.path.join(dst, root[src_prefix:], dirname)
                if not os.path.exists(dirpath):
                    os.mkdir(dirpath)

        self.log.logger.info('Reading in filenames from path : {}'.format(self.path))

        # loop to walk through each subdirectory
        for (root, dirs, files) in os.walk(self.path):

            # identify each file that exists
            for file in files:

                # makes sure we are grabbing files and not sub directories
                if file != '':

                    # join root name and filename to get full path:
                    # ex. root = 'C:/Desktop/ScanSession/diffusion' , file = 'D00004.dcm'
                    fname = os.path.join(root, file)

                    # append the full file paths to array self.file_paths
                    self.file_paths.append(fname)

                    # append the out file paths to self.out_file_paths

        # append num of files to results array
        self.num_of_files = len(self.file_paths)
        self.results.append(self.num_of_files)
        self.log.logger.info('Finished reading files...found {} files'.format(self.num_of_files))

    def hash_dicom_tag(self, dicom_tag):
        # get value corresponding to the dicom tag
        tag_value = dicom_tag.value
        # hash dicom_tag value
        hash_value = hashlib.sha256(str(tag_value).encode('utf-8')).hexdigest()
        return hash_value

    def deidentify_files(self):
        # store out_files so we know which files were deidentified and created
        self.out_file_bank = []
        # store tags that were actually replaced and removed...for file test...so we don't check
        # tags that were never replaced and throw arbitrary key error
        self.tags_actually_removed = []
        # key: dicom tag, value: replaced
        self.tags_actually_replaced = {}
        # tags that were actually hashed
        self.tags_actually_hashed = []
        self.log.logger.info('Deidentifying {} files.'.format(self.num_of_files))
        # open each file with Pydicom dcmread method
        for file in self.file_paths:
            try:
                self.ds = pydicom.dcmread(file)
            except:

                # self.log.logger.error('Could not read file {} without force'.format(file))
                try:
                    self.ds = pydicom.dcmread(file, force=True)

                except:
                    break
                    # self.log.logger.error('Could not read file {} with force'.format(file))

            # remove values
            for i in self.to_remove:
                try:
                    self.ds[int(i, 16)].value = ''
                    if i not in self.tags_actually_removed:
                        self.tags_actually_removed.append(i)
                except KeyError as e:
                    pass

            # hash values
            for i in self.to_hash:
                try:
                    self.ds[int(i, 16)].value = self.hash_dicom_tag(self.ds[int(i, 16)])
                    if i not in self.tags_actually_hashed:
                        self.tags_actually_hashed.append(i)

                except KeyError as e:
                    pass

            # replace values with user input
            try:
                self.ds[int('00100010', 16)].value = self.participant_ID
                if '00100010' not in self.tags_actually_replaced.keys():
                    self.tags_actually_replaced['00100010'] = self.participant_ID
            except KeyError as e:
                pass

            try:
                self.ds[int('00100020', 16)].value = self.participant_ID
                if '00100020' not in self.tags_actually_replaced.keys():
                    self.tags_actually_replaced['00100020'] = self.participant_ID
            except KeyError as e:
                pass

            try:
                self.ds[int('00080080', 16)].value = self.site_ID
                if '00080080' not in self.tags_actually_replaced.keys():
                    self.tags_actually_replaced['00080080'] = self.site_ID
            except KeyError as e:
                pass

            # value to store where our new path differs from original file path
            diff = 0

            # iterate through each char in old path and new path...
            for i in range(0,len(self.out_path)):
                # find difference between old and new path
                if file[i] != self.out_path[i]:
                    # store that difference
                    diff = i
                    break
            # append '_did' string to old path to get our new file path
            out_file = file[:diff] + '_did' + file[diff:]

            # save files to new folder
            try:
                self.ds.save_as(out_file)
                self.out_file_bank.append(out_file)
            except:
                self.log.logger.info('Could not create file: {}'.format(out_file))

        self.log.logger.info("Deidentification of {} files complete".format(self.num_of_files))

    def file_test(self):
        self.log.logger.info("Beginning of file test...")
        # make sure proper tags were removed
        for file in self.out_file_bank:
            # open new dicom files from _did folder
            try:
                ds = pydicom.dcmread(file)
            except:
                try:
                    ds = pydicom.dcmread(file, force=True)
                except:
                    self.log.logger.error("Could not read dicom file {}".format(file))

            # check removed tags
            for i in self.tags_actually_removed:
                try:
                    ds[int(i, 16)].value == ''
                except:
                    # if you want to raise this as an exception to front end...you could pass a variable into backed and parse
                    # the exception to it.
                    self.log.logger.error("Dicom tag {} was not removed for file {}".format(i,file))

            # check replaced tags
            for i in self.tags_actually_replaced:
                try:
                    ds[int(i,16)].value == self.tags_actually_replaced[i]
                except:
                    self.log.logger.error\
                        ("Replace issue for dicom tag {}, expected {} : recieved {}"\
                         .format(i,self.tags_actually_replaced[i],ds[int(i,16)].value))

        self.log.logger.info('End of file test...')

    def rename_out_folder(self):
        # source is our folder with deidentified files
        src = self.path + '_did'

        # loop to get destination (dst), same path with scan session id as name
        count = 0
        for i in range(len(src)-1,0,-1):
            if src[i] =='/':
                count = i + 1
                break
        print(src[:count])
        dst = src[:count] + self.scan_session_ID

        # rename the folder
        try:
            os.rename(src,dst)
        except FileExistsError as e:
            self.log.logger.info("Cannot create directory, {} already exists".format(dst))


def run(path, site_ID, patient_ID, scansession_ID, results, logger, parent):
    dicom_object = DataSet(path, site_ID, patient_ID, scansession_ID, results, logger)

    #read the .das file
    das_file_path = 'bin/anon_for_discovery.das'
    dicom_object.das_file_reader(das_file_path)

    #walk through the selected folder
    dicom_object.walk_through_files()

    #deidentify the files
    dicom_object.deidentify_files()
    dicom_object.file_test()
    #dicom_object.rename_out_folder()
    if parent == 'test':
        return dicom_object









