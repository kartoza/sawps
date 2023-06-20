import React, { useState } from 'react';
import Grid from "@mui/material/Grid";
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';

interface UploaderInterface {
    open: boolean;
    onClose: () => void;
}

export default function Uploader(props: UploaderInterface) {
    const { open, onClose } = props;

    const handleClose = () => {
        onClose();
      };

    return (
        <Dialog onClose={handleClose} open={open} className='Uploader'>
            <DialogTitle>Upload</DialogTitle>
            <Grid container flexDirection={'column'}>
                <Grid item>
                    {/* drag and drop zone */}
                </Grid>
            </Grid>
        </Dialog>
    )

}

