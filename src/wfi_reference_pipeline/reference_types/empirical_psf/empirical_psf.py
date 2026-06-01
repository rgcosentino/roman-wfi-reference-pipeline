from roman_datamodels.datamodels import EpsfRefModel

from ..reference_type import ReferenceType
from wfi_reference_pipeline.resources.wfi_meta_empirical_psf import (
    WFIMetaEPSF,
)


class EmpiricalPSF(ReferenceType):

    def __init__(
        self,
        meta_data,
        psf,
        extended_psf=None,
        psf_noipc=None,
        extended_psf_noipc=None,
        outfile="roman_epsf_file.asdf",
        clobber=False,
    ):

        super().__init__(
            meta_data=meta_data,
            ref_type_data=psf,
            outfile=outfile,
            clobber=clobber,
        )

        if not isinstance(meta_data, WFIMetaEPSF):

            raise TypeError(
                f"Meta Data has reftype "
                f"{type(meta_data)}, "
                f"expecting WFIMetaEPSF"
            )

        self.meta = meta_data
        self.outfile = outfile
        self.psf = psf
        self.extended_psf = extended_psf
        self.psf_noipc = psf_noipc
        self.extended_psf_noipc = (
            extended_psf_noipc
        )

        self._update_meta_data()

    # --------------------------------------------------------
    # Metadata handling
    # --------------------------------------------------------
    def _update_meta_data(self):

        self.meta.pixel_x = list(
            self.meta.pixel_x
        )

        self.meta.pixel_y = list(
            self.meta.pixel_y
        )

        self.meta.spectral_type = list(
            self.meta.spectral_type
        )

        self.meta.defocus = list(
            self.meta.defocus
        )

    # --------------------------------------------------------
    # Build ASDF tree and populate data model
    # --------------------------------------------------------
    def populate_datamodel_tree(self):

        epsf_datamodel_tree = EpsfRefModel()
        epsf_datamodel_tree["meta"] = self.meta.export_asdf_meta()
        epsf_datamodel_tree["psf"] = self.psf

        if self.extended_psf is not None:
            epsf_datamodel_tree[
                "extended_psf"
            ] = self.extended_psf

        if self.psf_noipc is not None:
            epsf_datamodel_tree[
                "psf_noipc"
            ] = self.psf_noipc

        if self.extended_psf_noipc is not None:
            epsf_datamodel_tree[
                "extended_psf_noipc"
            ] = self.extended_psf_noipc

        return epsf_datamodel_tree
    
    def calculate_error(self):
        """
        Abstract method not applicable.
        """
        pass

    def update_data_quality_array(self):
        """
        Abstract method not utilized.
        """
        pass