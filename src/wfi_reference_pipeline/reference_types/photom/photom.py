"""
See https://innerspace.stsci.edu/spaces/RI/pages/295761371/RFP+-+Modules+and+Algorithm+Development for more details
"""

import logging
import numpy as np
import roman_datamodels.stnode as rds


from ..reference_type import ReferenceType


class {RefType}(ReferenceType):
    """
    Class RefType inherits the ReferenceType() base class methods
    where static meta data for all reference file types are written.

    rfp_{ref_type} = RefType(meta_data, ref_type_data=)
    rfp_{ref_type}.make_{ref_type}_image()
    rfp_{ref_type}.generate_outfile()
    """

    def __init__(
        self,
        meta_data,
        file_list=None,
        ref_type_data=None,
        bit_mask=None,
        outfile="roman_{ref_type}.asdf",
        clobber=False,
    ):
        """
        The __init__ method initializes the class with proper input variables needed by the ReferenceType()
        file base class.

        Parameters
        ----------
        meta_data: Object; default = None
            Object of meta information converted to dictionary when writing reference file.
        file_list: List of strings; default = None
            List of file names with absolute paths. Intended for primary use during automated operations.
        ref_type_data: numpy array; default = None
            Input data cube. Intended for development support file creation or as input
            for reference file types not generated from a file list.
        bit_mask: 2D integer numpy array, default = None
            A 2D data quality integer mask array to be applied to reference file.
        outfile: string; default = roman_mask.asdf
            File path and name for saved reference file.
        clobber: Boolean; default = False
            True to overwrite outfile if outfile already exists. False will not overwrite and exception
            will be raised if duplicate file found.
        ---------

        See reference_type.py base class for additional attributes and methods.
        """

        # Access methods of base class ReferenceType
        super().__init__(
            meta_data=meta_data,
            file_list=file_list,
            ref_type_data=ref_type_data,
            bit_mask=bit_mask,
            outfile=outfile,
            clobber=clobber
        )

        # Default meta creation for module specific ref type.
        if not isinstance(meta_data, WFIMeta{RefType}):
            raise TypeError(
                f"Meta Data has reftype {type(meta_data)}, expecting WFIMeta{RefType}"
            )
        if len(self.meta_data.description) == 0:
            self.meta_data.description = "Roman WFI {ref_type} reference file."

        logging.debug(f"Default {ref_type} reference file object: {outfile} ")

