"""
Example script for submitting reference files to CRDS.
This will allow users to test submissions manually.
"""

import glob
import time

from wfi_reference_pipeline.config.config_access import get_data_files_config
from wfi_reference_pipeline.utilities.manifest import (
    make_manifest,
    print_manifest,
    print_meta_fields_together,
)
from wfi_reference_pipeline.utilities.submit_files_to_crds import WFISubmit

# NOTE: These are the variables to change
# Change to True to complete submission info (you should also manualy update the submission information below if update_dict == True)
update_dict = True
# Gather new files based on the pattern in the config file, update to grab the file(s) you are looking for that exist inside the rfp_output_dir_root.
filter_for_file = "*mask2_WFI01.asdf"
# Check manifest of meta data before submitting, and Certify files with CRDS command.
check_files = True
# Boolean switch to make sure no one delivers anything on the fly by just running this without looking at it.
actually_submit_to_crds = False


# Load configuration settings
rfp_output_dir_root = get_data_files_config()["rfp_output_dir_root"]

# Get your files and sort them
new_files = glob.glob(
    rfp_output_dir_root + filter_for_file
)
new_files.sort()


# Initialize the WFISubmit instance
# The server selection is set to 'test' for testing. All Roman CRDS submissions should go to 'test'.
# All TVAC CRDS submissions should go to 'tvac'
submission = WFISubmit(new_files, server="test")

# User has to modify the following entries in the submission dictionary in order for submission to be a success.
if update_dict:
    submission.submission_dict["instrument"] = "WFI"
    submission.submission_dict["deliverer"] = "NAME OF USER"
    submission.submission_dict["other_email"] = "USER_EMAIL@stsci.edu"
    submission.submission_dict["file_type"] = "MASK"
    submission.submission_dict["useafter_matches"] = "N/A"
    submission.submission_dict["compliance_verified"] = "N/A"
    submission.submission_dict["calpipe_version"] = "N/A"
    submission.submission_dict["replacing_badfiles"] = "No"
    submission.submission_dict["jira_issue"] = "RTB-000"
    submission.submission_dict["table_rows_changed"] = "N/A"
    submission.submission_dict["modes_affected"] = (
        "Both WFI Imaging WIM and Spectral WSM modes."
    )
    submission.submission_dict["change_level"] = (
        "MODERATE"  # allowed entries - TRIVIAL, SEVERE, MODERATE
    )
    submission.submission_dict["correctness_testing"] = (
        "Files were made with latest versions of roman data models and"
        "roman attribute dictionary."
    )
    submission.submission_dict["additional_considerations"] = (
        "New Additional Considerations"
    )
    submission.submission_dict["description"] = (
        "New MASK reference files identifying GSFC derived optical bad pixels from TVAC data."
    )

# Update the submission form
submission.update_crds_submission_form()

# Check manifest of meta data before submitting, and Certify files with CRDS command.
if check_files:
    # Check manifest of meta data before submitting.
    meta_manifest = make_manifest(new_files)

    # This below will print the meta for each file.
    print_manifest(meta_manifest)

    # This will print the meta by each key in the meta for every file.
    print_meta_fields_together(meta_manifest)

    # Certify files with CRDS command.
    submission.certify_reference_files()

# Boolean switch to make sure no one delivers anything on the fly by just running this without looking at it.
if actually_submit_to_crds:
    # Start timing the submission process
    start_time = time.time()
    print("Start Time:", start_time)
    submission.submit_to_crds()
    # Measure elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("End Time:", end_time)
    print("Elapsed Time:", elapsed_time)
