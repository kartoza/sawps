import React, {useState, useEffect} from 'react';
import Grid from '@mui/material/Grid';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import WarningIcon from '@mui/icons-material/Warning';
import './index.scss';

export enum AlertType {
    none = 'none',
    success = 'success',
    error = 'error',
    warning = 'warning'
}

interface FeedbackAlertDialogInterface {
    type: AlertType,
    alertDialogTitle: string,
    alertDialogDescription: string,
    alertClosed?: () => void,
    actionButtonText?: string
}

const getIcon = (type: AlertType) => {
    if (type === AlertType.error) {
        return <ErrorIcon style={{fontSize: 60}} />
    } else if (type === AlertType.warning) {
        return <WarningIcon style={{fontSize: 60}} />
    }
    return <CheckCircleIcon style={{fontSize: 60}} />
}

export default function FeedbackAlertDialog(props: FeedbackAlertDialogInterface) {
    const [open, setOpen] = useState<boolean>(false);

    useEffect(() => {
        if (props.type === AlertType.none) {
            setOpen(false)
        } else {
            setOpen(true)
        }
    }, [props.type])

    const handleClose = () => {
        if (props.alertClosed) {
            props.alertClosed()
        }
        setOpen(false)
    }

    return (<div>
            <Dialog
                open={open}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
                disableEscapeKeyDown
                className='FeedbackAlertDialog'
            >
                <DialogTitle id="alert-dialog-title">
                    { props.alertDialogTitle }
                </DialogTitle>
                <DialogContent>
                    <Grid container flexDirection={'row'} spacing={2} justifyContent={'flex-start'} alignItems={'center'}>
                        <Grid item className={props.type}>
                            {getIcon(props.type)}
                        </Grid>
                        <Grid item>
                            <DialogContentText>
                                {props.alertDialogDescription}
                            </DialogContentText>
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button variant='contained' onClick={handleClose}>
                        {props.actionButtonText ? props.actionButtonText : `OK`}
                    </Button>
                </DialogActions>
            </Dialog>
        </div>);
}