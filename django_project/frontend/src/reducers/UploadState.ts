import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import { UploadMode } from "../models/Upload";

const DEFAULT_UPLOAD_MODE = UploadMode.None


export interface UploadStateInterface {
    uploadMode: UploadMode;
}

const initialState: UploadStateInterface = {
    uploadMode: DEFAULT_UPLOAD_MODE
}

export const UploadStateSlice = createSlice({
    name: 'UploadState',
    initialState,
    reducers: {
        setUploadState: (state, action: PayloadAction<UploadMode>) => {
            state.uploadMode = action.payload
        }
    }
})

export const {
    setUploadState
} = UploadStateSlice.actions

export default UploadStateSlice.reducer;
