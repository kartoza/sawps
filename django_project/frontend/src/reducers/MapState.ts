import {createSlice, PayloadAction} from "@reduxjs/toolkit";

export interface MapStateInterface {
    isMapReady: boolean;
    selectionMode: string; // none, property, parcel, digitise, parcelJSON
}

const initialState: MapStateInterface = {
    isMapReady: false,
    selectionMode: 'property'
}

export const MapStateSlice = createSlice({
    name: 'MapState',
    initialState,
    reducers: {
        setMapReady: (state, action: PayloadAction<boolean>) => {
            state.isMapReady = action.payload
        },
        setMapMode: (state, action: PayloadAction<string>) => {
            state.selectionMode = action.payload
        }
    }
})

export const {
    setMapReady,
    setMapMode
} = MapStateSlice.actions

export default MapStateSlice.reducer;