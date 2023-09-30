# the raw dicom data and how to grab relevant data from it
import pydicom


def is_rs_file(filepath: str) -> bool:
    '''Checks if a file is a DICOM file and if it contains the data to make a cylinder'''
    try:
        dataset = pydicom.read_file(filepath)
        # finding the contour data
        referenced_roi = list(filter(lambda s:
                                     ("surface" in s.ROIObservationLabel.lower()),
                                     dataset.RTROIObservationsSequence))[0].ReferencedROINumber
        contour_data = list(filter(lambda s:
                                   (s.ReferencedROINumber == referenced_roi),
                                   dataset.ROIContourSequence))[0].ContourSequence[0].ContourData
    except:
        print(f"Invalid RS DICOM file: {filepath}")
        return False
    else:
        return True


def is_rp_file(filepath: str) -> bool:
    '''Checks if a file is a DICOM file and if it contains the data for needle channels'''
    try:
        dataset = pydicom.read_file(filepath)
        # finding the contour data
        channels = dataset.ApplicationSetupSequence[0].ChannelSequence
        if len(channels) < 1:
            return False
    except:
        print(f"Invalid RP DICOM file: {filepath}")
        return False
    else:
        return True