import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import {v4 as uuidv4} from 'uuid';
import Alert, { AlertColor } from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import Dropzone, { ILayoutProps, IInputProps } from "react-dropzone-uploader";
import { useAppDispatch, useAppSelector } from '../../../app/hooks';
import {RootState} from '../../../app/store';
import ParcelInterface from '../../../models/Parcel';
import {
    setSelectedParcels,
    triggerMapEvent,
    toggleParcelSelectionMode
} from '../../../reducers/MapState';
import '../../../assets/styles/RDU.styles.scss';
import './index.scss';
import { MapEvents } from '../../../models/Map';
import LinearProgressWithLabel from "../../../components/LinearProgressWithLabel";

interface UploaderInterface {
    open: boolean;
    onClose: () => void;
}

const PENDING_STATUS = 'PENDING'
const PROCESSING_STATUS = 'PROCESSING'
const DONE_STATUS = 'DONE'
const ERROR_STATUS = 'ERROR'

const ALLOWABLE_FILE_TYPES = [
    'application/geo+json',
    'application/geopackage+sqlite3',
    'application/zip',
    'application/json',
    'application/x-zip-compressed',
    'application/vnd.google-earth.kml+xml',
    '.gpkg',
    '.kml'
]

const UPLOAD_FILE_URL = '/api/upload/boundary-file/'
const REMOVE_FILE_URL = '/api/upload/boundary-file/remove/'
const PROCESS_FILE_URL = '/api/upload/boundary-file/'

const CustomInput = (props: IInputProps) => {
    const {
      className,
      labelClassName,
      labelWithFilesClassName,
      style,
      labelStyle,
      labelWithFilesStyle,
      getFilesFromEvent,
      accept,
      multiple,
      disabled,
      content,
      withFilesContent,
      onFiles,
      files,
    } = props
  
    return (
    <Grid container flexDirection={'column'}>
        <Grid item>
            <span className='CloudUploadIcon'/>
        </Grid>
        <Grid item className='CenterItem'>
            <label>
                <span>Drag & drop files or </span><span className='BrowseLink'>Browse</span>
                <input
                className={className}
                style={style}
                type="file"
                accept={accept}
                multiple={multiple}
                disabled={disabled}
                onChange={async e => {
                    const target = e.target
                    const chosenFiles = await getFilesFromEvent(e)
                    onFiles(chosenFiles)
                    //@ts-ignore
                    target.value = null
                }}
                />
            </label>
        </Grid>
        <Grid item className='CenterItem'>
            <Typography variant='subtitle2' sx={{fontWeight: 400}}>Supported formats: zip, json, geojson, gpkg, kml (CRS 4326)</Typography>
        </Grid>
    </Grid>
      
    )
  }

export default function Uploader(props: UploaderInterface) {
    const dispatch = useAppDispatch()
    const { open, onClose } = props;
    const [session, setSession] = useState('')
    const [loading, setLoading] = useState(false)
    const dropZone = useRef(null)
    const [alertMessage, setAlertMessage] = useState('')
    const [alertTitle, setAlertTitle] = useState('')
    const [alertSeverity, setAlertSeverity] = useState<AlertColor>('success')
    const [savingBoundaryFiles, setSavingBoundaryFiles] = useState(false)
    const [totalFile, setTotalFile] = useState(0)
    const uploadMode = useAppSelector((state: RootState) => state.uploadState.uploadMode)
    const [requestStatus, setRequestStatus] = useState(PENDING_STATUS)
    const [requestProgress, setRequestProgress] = useState(0)
    const [requestSubmitted, setRequestSubmitted] = useState(false)

    const showAlertMessage = (severity: AlertColor, message: string, title?: string) => {
        setAlertSeverity(severity)
        setAlertMessage(message)
        if (title) {
            setAlertTitle(title)
        } else {
            setAlertTitle(severity === 'error' ? 'Error': 'Success')
        }
    }

    const hideAlertMessage = () => {
        setAlertTitle('')
        setAlertMessage('')
        setAlertSeverity('success')
    }

    useEffect(() => {
        if (open) {
            setSession(uuidv4())
            hideAlertMessage()
            setSavingBoundaryFiles(false)
            setTotalFile(0)
            setRequestStatus(PENDING_STATUS)
            setRequestProgress(0)
            setRequestSubmitted(false)
        }
    }, [open])

    // @ts-ignore
    const _csrfToken = csrfToken || '';

    // specify upload params and url for your files
    // @ts-ignore
    const getUploadParams = ({file, meta}) => {
        if (loading) return null
        const body = new FormData()
        body.append('file', file)
        body.append('meta_id', meta.id)
        body.append('session', meta.session)
        body.append('uploadDate', meta.lastModifiedDate)
        const headers = {
            'Content-Disposition': 'attachment; filename=' + meta.name,
            'X-CSRFToken': _csrfToken
        }
        return {url: UPLOAD_FILE_URL, body, headers}
    }

    // called every time a file's `status` changes
    // @ts-ignore
    const handleChangeStatus = (file, status) => {
        let {meta, f, xhr} = file
        meta.session = session
        if (status === 'preparing') {
            hideAlertMessage()
        }
        if (status === 'done') {
            setTotalFile(totalFile + 1)
        }
        if (status === 'removed') {
            const dropZoneCurrent = dropZone.current;
            if (!dropZoneCurrent) {
                showAlertMessage('error', 'Unable to remove the layer file, Please try again!')
                // exit if ref dropZone is not found
                return;
            }

            fetch(REMOVE_FILE_URL, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': _csrfToken
                },
                body: JSON.stringify({
                    'meta_id': meta.id,
                    'session': session
                })
            }).then( response => {
                if (response.ok) {
                    if (totalFile - 1 < 0) {
                        setTotalFile(0)
                    } else {
                        setTotalFile(totalFile - 1)
                    }
                } else {
                    showAlertMessage('error', 'Could not remove the layer, please try again later')
                }
            }).catch(
                error => {
                    console.error('Error calling layer-remove api :', error)
                    showAlertMessage('error', 'Could not remove the layer, please try again later')
                }
            )
        }
        if (status === 'error_upload') {
            setTimeout(() => {
                file.remove()
                let  error = ''
                try {
                    let response = JSON.parse(xhr.response)
                    error = response.detail
                } catch (error) {
                    error = 'There is unexpected error during upload! Please try again later'
                }
                showAlertMessage('error', error)
            }, 300)
        }
    }

    const handleClose = (event: any, reason: any) => {
        if (reason && (reason == 'backdropClick' || reason == 'escapeKeyDown'))
            return;
        onClose();
    };

    const saveBoundaryFiles = () => {
        setLoading(true)
        axios.get(`${PROCESS_FILE_URL}${session}/search/`).then((response) => {
            setLoading(false)
            setSavingBoundaryFiles(true)
            dispatch(setSelectedParcels([]))
            setRequestSubmitted(true)
        }).catch((error) => {
            setLoading(false)
            console.log(error)
        })
    }

    const getStatus = () => {
        axios.get(`${PROCESS_FILE_URL}${session}/status/`).then((response) => {
            if (response.data) {
                let _status = response.data['status']
                let _progress = response.data['progress']
                setRequestProgress(_progress)
                setRequestStatus(_status)
                if (_status === DONE_STATUS) {
                    setSavingBoundaryFiles(false)
                    let _parcels = response.data['parcels'] as ParcelInterface[]
                    dispatch(setSelectedParcels(_parcels))
                    dispatch(toggleParcelSelectionMode(uploadMode))
                    // trigger map zoom to bbox
                    let _bbox = response.data['bbox']
                    if (_bbox && _bbox.length === 4) {
                        let _bbox_str = _bbox.map(String)
                        _bbox_str.push(session)
                        dispatch(triggerMapEvent({
                            'id': uuidv4(),
                            'name': MapEvents.BOUNDARY_FILES_UPLOADED,
                            'date': Date.now(),
                            'payload': _bbox_str
                        }))
                    }
                    let _usedParcelsMessage = ''
                    if (response.data['used_parcels'].length > 0) {
                        let _sliced = response.data['used_parcels'].slice(0, 5)
                        let _usedParcels = _sliced.join(', ')
                        if (response.data['used_parcels'].length > 5) {
                            _usedParcels += ` and ${(response.data['used_parcels'].length - 5)} more`
                        }
                        _usedParcelsMessage = `Following parcel has already been used by another property: ${_usedParcels}.`
                        if (response.data['used_parcels'].length > 1) {
                            _usedParcelsMessage = `Following parcels have already been used by another property: ${_usedParcels}.`
                        }
                    }
                    let _addedParcelMessage = `${_parcels.length === 1 ? '1 parcel has' : _parcels.length + ' parcels have'} been added to the selection.`
                    if (_parcels.length > 0 && _usedParcelsMessage === '') {
                        // success
                        showAlertMessage('success', _addedParcelMessage)
                    } else if (_parcels.length > 0 && _usedParcelsMessage !== '') {
                        // warning
                        let _warnMessage = _addedParcelMessage + '\r\nWarning: ' + _usedParcelsMessage
                        showAlertMessage('warning', _warnMessage, 'Search is finished with warning')
                    } else if (_usedParcelsMessage !== '') {
                        // error
                        showAlertMessage('error', _usedParcelsMessage)
                        setRequestSubmitted(false)
                    } else {
                        // empty parcels
                        showAlertMessage('error', 'There is no matching parcel has been found.')
                        setRequestSubmitted(false)
                    }
                } else if (_status === ERROR_STATUS) {
                    setSavingBoundaryFiles(false)
                    showAlertMessage('error', 'Unable to process the files, Please try again or contact the Administrators!')
                    setRequestSubmitted(false)
                } else if (_status === PROCESSING_STATUS) {
                    showAlertMessage('info', '', 'Processing the uploaded files in background...')
                }
            }
        }).catch((error) => {
            console.log(error)
        })
    }

    useEffect(() => {
        if (savingBoundaryFiles) {
            const interval = setInterval(() => {
                getStatus()
            }, 3000);
            return () => clearInterval(interval);
        }
    }, [savingBoundaryFiles])

    const CustomLayout = ({ input, previews, submitButton, dropzoneProps, files, extra: { maxFiles } }: ILayoutProps) => {
        return (
            <Grid container flexDirection={'column'} rowSpacing={2} className='uploader-container'>
                <Grid item>
                    <div {...dropzoneProps}>
                        {input}
                    </div>
                </Grid>
                <Grid item>
                    <Grid container flexDirection={'column'}>
                        <Grid item>
                            <Typography sx={{ fontSize: 14 }} color='text.secondary' gutterBottom>
                                Uploaded Files
                            </Typography>
                        </Grid>
                        <Grid item className='UploadedFilesPreview'>
                            {previews}
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        )
    }

    return (
        <Dialog onClose={handleClose} open={open} className='Uploader'>
            <DialogTitle>Upload</DialogTitle>
            <Grid container flexDirection={'column'} className='UploaderContent' rowSpacing={2}>
                <Grid item flex={1}>
                    { alertTitle ?
                        <Alert className='UploadAlertMessage' style={{ width: '100%', textAlign: 'left' }} severity={alertSeverity}>
                            <AlertTitle>{ alertTitle }</AlertTitle>
                            <p className="display-linebreak">
                                { alertMessage }
                            </p>
                            { requestSubmitted && requestStatus === PROCESSING_STATUS ? <LinearProgressWithLabel value={requestProgress} /> : null}
                        </Alert> : null }
                    <Dropzone
                        ref={dropZone}
                        disabled={loading || savingBoundaryFiles || requestSubmitted}
                        InputComponent={CustomInput}
                        maxFiles={5}
                        getUploadParams={getUploadParams}
                        onChangeStatus={handleChangeStatus}
                        accept={ALLOWABLE_FILE_TYPES.join(', ')}
                        LayoutComponent={CustomLayout}
                        canRemove={!requestSubmitted}
                    />
                </Grid>
                <Grid item>
                    { requestSubmitted && requestStatus === DONE_STATUS ? 
                        <Grid container flexDirection={'row'} justifyContent={'space-between'} spacing={2}>
                            <Grid item>
                                <Button variant='outlined' onClick={() => onClose()}>CLOSE</Button>
                            </Grid>
                        </Grid>
                    :
                        <Grid container flexDirection={'row'} justifyContent={'space-between'} spacing={2}>
                            <Grid item>
                                <Button variant='outlined' disabled={loading || savingBoundaryFiles} onClick={() => onClose()}>CANCEL</Button>
                            </Grid>
                            <Grid item>
                                { savingBoundaryFiles ? (
                                    <Button variant='contained' disabled={true}><CircularProgress size={16} sx={{marginRight: '5px' }}/> PROCESSING FILES...</Button>
                                ) : (
                                    <Button variant='contained' disabled={loading || savingBoundaryFiles || totalFile === 0} onClick={saveBoundaryFiles}>UPLOAD FILES</Button>
                                )}
                            </Grid>
                        </Grid>
                    }
                </Grid>
            </Grid>
        </Dialog>
    )

}

